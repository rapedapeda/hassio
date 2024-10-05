import appdaemon.plugins.hass.hassapi as hass
import mqttapi as mqtt
from datetime import datetime, timedelta

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
                "empty_vacuum": False,  # Stofzuigerbak is in het begin leeg
                "last_clean": datetime(2024, 1, 1), # Initiele vroegere datum
                "clean_interval": config.get("clean_interval", 1),
                "do_not_disturb": config.get("do_not_disturb", None),
                "segments": config.get("segments", None)
            }
            
            zone = self.zones[item]

            # Luister naar de status van de stofzuiger
            self.listen_event(self.vacuum_status_message, "MQTT_MESSAGE", namespace="mqtt", topic=f'{self.mqtt_topic_prefix}/{zone["vacuum"]}/StatusStateAttribute/status')

            # Luister naar een verandering in de total cleaned area
            self.listen_event(self.update_cleaned_area, "MQTT_MESSAGE", namespace="mqtt", topic=f'{self.mqtt_topic_prefix}/{zone["vacuum"]}/TotalStatisticsCapability/area')

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
                    
                    # Laat het naar de goede locatie gaan
                    
                    self.log(f'[{zone_name}] Opvangbak stofzuiger vol. Stofzuiger naar schoonmaaklocatie.')
                

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
        topic = f'{self.mqtt_topic_prefix}/{zone_data["vacuum"]}/MapSegmentationCapability/clean/set'
        payload_data = {
            "segment_ids": zone_data["segments"],
            "iterations": 1
        }
        
        # Zet de Python dictionary om naar een JSON string
        payload = json.dumps(payload_data)

    def vacuum_status_message(self, event, event_data, kwargs):
        # Als de status-message verandert naar 'docked'

        # Plus de valetudo/snuffel/CurrentStatisticsCapability/area bij de self.areas etc op
        # Maar alleen als 

            # Zet eventueel emty_vacuum op True
        self.log(f'Event status data: {event_data}')

    def update_cleaned_area(self, event, event_data, kwargs):
        # Als de total cleaned area veranderd
        # Dan hier verschil met vorige berekenen
        # Verschil toevoegen aan de zone["area_cleaned"]
        self.log(f'Event area data: {event_data}')
