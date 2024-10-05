import appdaemon.plugins.hass.hassapi as hass
import mqttapi as mqtt
from datetime import datetime, timedelta
import json

class AutoVacuum(hass.Hass, mqtt.Mqtt):
    
    def initialize(self):
        self.last_cleaned = {}
        self.do_not_disturb = self.args["do_not_disturb"]
        self.mqtt_topic_prefix = self.args["mqtt_topic_prefix"]
        
        # Subscribe naar de MQTT van de stofzuiger
        self.mqtt_subscribe(f'{self.mqtt_topic_prefix}/#', namespace="mqtt")

        # Dictionary voor alle areas met hun relevante gegevens (vacuum, state, empty)
        self.zones = {}

        # Initialiseer alle areas en luister naar de alarmstatus
        for item, config in self.args["zones"].items():

            # Maak een entry in de dictionary voor dit area met de attributen vacuum, state en empty
            self.zones[item] = {
                "zone": item, # Naam van de zone (voor loggingdoeleinden)
                "vacuum": config["vacuum"],  # Naam van de stofzuiger
                "state": 'None',  # Status van de stofzuiger
                "area": config["area"],
                "area_cleaned": 0, # aantal cm schoongemaakt sinds leegmaken opvangbakje
                "total_area_cleaned": 0, # Tijdelijke opslag van de totale area van robot zelf
                "empty_vacuum": False,  # Stofzuigerbak is in het begin leeg
                "last_clean": datetime(2024, 1, 1), # Initiele vroegere datum
                "clean_interval": config.get("clean_interval", 1),
                "do_not_disturb": config.get("do_not_disturb", None),
                "segments": config.get("segments", None),
                "bin_coordinates": config.get("bin_coordinates", None)
            }
            
            zone = self.zones[item]

            # Push de benodigde sensoren naar HomeAssistant
            self.set_value(f'sensor.{self.mqtt_topic_prefix}_{zone["vacuum"]}_opvangbak', zone["area_cleaned"])


            # Luister naar de status van de stofzuiger
            self.listen_event(self.vacuum_status_message, "MQTT_MESSAGE", namespace="mqtt", topic=f'{self.mqtt_topic_prefix}/{zone["vacuum"]}/StatusStateAttribute/status', zone=zone)

            # Luister naar een verandering in de total cleaned area
            self.listen_event(self.update_cleaned_area, "MQTT_MESSAGE", namespace="mqtt", topic=f'{self.mqtt_topic_prefix}/{zone["vacuum"]}/TotalStatisticsCapability/area', zone=zone)

        # Luister naar de statusverandering van het alarm
        self.listen_state(self.occupancy_triggered, "alarm_control_panel.huis", namespace="default")

    def occupancy_triggered(self, entity, attribute, old, new, kwargs):
        # Loop door alle gebieden heen
        for zone_name, zone_data in self.zones.items():

            if new == "armed_away":
                # Kijk of er moet worden gestofzuigd
                now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                last_clean = zone_data["last_clean"].replace(hour=0, minute=0, second=0, microsecond=0)
                if (now - last_clean).days < zone_data["clean_interval"]:
                    self.log(f'[{zone_name}] schoonmaakinterval nog niet overschreden, stofzuiger niet gestart.')
                    continue

                # Kijk of er mag worden gestofzuigd
                if zone_data["do_not_disturb"] and self.now_is_between(self.do_not_disturb[0], self.do_not_disturb[1]):
                    self.log(f'[{zone_name}] Do Not Disturb actief, stofzuiger niet gestart.')
                    continue
                
                # Controleer de status van de stofzuiger
                vacuum_state = zone_data.get("state", "docked")

                if vacuum_state == "docked":
                    # Start de stofzuiger als hij in de dock staat
                    self.start_vacuum(zone_data)
                    self.log(f'[{zone_name}] Stofzuiger is gestart.')

                else:
                    self.log(f'[{zone_name}] Stofzuiger is niet in dock. Huidige status: {zone["state"]}.')
        
            elif new in ['armed_home', 'disarmed', 'armed_night']:
                # Check of een vacuum geleegd moet worden.
                if zone_data["area_cleaned"] >= 3 * zone_data["area"]:
                    self.log(f'[{zone_name}] Opvangbak stofzuiger vol.')
                    if not zone_data["bin_coordinates"]:
                        self.log(f'[{zone_name}] Opvangbak stofzuiger vol. Geen prullenbaklocatie gedefinieerd.', level="warning")
                    else:
                        # Laat het naar de goede locatie gaan
                        self.vacuum_to_location(zone_data)
                

    def start_vacuum(self, zone_data):
        if zone_data["segments"]:
            topic = f'{self.mqtt_topic_prefix}/{zone_data["vacuum"]}/MapSegmentationCapability/clean/set'
            payload_data = {
                "segment_ids": zone_data["segments"],
                "iterations": 1
            }
            
            # Zet de Python dictionary om naar een JSON string
            payload = json.dumps(payload_data)

        else:
        # Domme aansturing door gewoon te starten met schoonmaken
            topic = f'{self.mqtt_topic_prefix}/{zone["vacuum"]}/BasicControlCapability/operation/set'
            payload = '{"operation": "START"}'  # Payload voor starten van de stofzuiger

        self.mqtt_publish(topic, payload, qos=1, namespace="mqtt")  # Verzend het MQTT-bericht

    def vacuum_to_location(self, zone_data):
        topic = f'{self.mqtt_topic_prefix}/{zone_data["vacuum"]}/GoToLocationCapability/go/set'
        payload_data = {
            "coordinates": {
                "x": zone_data["bin_coordinates"][0],
                "y": zone_data["bin_coordinates"][1]
            }
        }
    
        # Zet de Python dictionary om naar een JSON string
        payload = json.dumps(payload_data)  
        self.mqtt_publish(topic, payload, qos=1, namespace="mqtt")
        self.log(f'[{zone_data["zone"]}] verplaatst naar locatie')

    def vacuum_status_message(self, event, event_data, kwargs):
        # Als de status-message verandert naar 'docked'
        state = event_data.get("payload", None)
        if state == "docked":
            
            self.log(f'Event status data: {event_data}')

    def update_cleaned_area(self, event, event_data, kwargs):
        # Als de total cleaned area veranderd
        # Dan hier verschil met vorige berekenen
        # Verschil toevoegen aan de zone["area_cleaned"]
        # Sensor updaten in home-assistant
        zone_data = kwargs.get("zone")

        # Haal de oude en de nieuwe cleaned_area op
        old_cleaned_area = zone_data["total_area_cleaned"]
        new_cleaned_area = event_data.get("payload", 0)

        # Bereken het verschil sinds de laatste update
        difference = new_cleaned_area - old_cleaned_area
        if difference < 0:
            self.log(f"Oppervlakte statistieken van de robot lijken te zijn gereset", level="warning")

        elif difference > 0:
            zone_data['total_area_cleaned'] = new_cleaned_area
            zone_data['area_cleaned'] += difference
            
            self.set_value(f'sensor.{self.mqtt_topic_prefix}_{zone_data["vacuum"]}_opvangbak', zone_data["area_cleaned"])
            self.log(f'[{zone_data["zone"]}] Cleaned_area geupdatet.')
