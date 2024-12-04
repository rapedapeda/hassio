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
                "state": 'docked',  # Status van de stofzuiger
                "clean_times": config["clean_times"], # Na hoevaak stofzuigen is de opvangbak vol?
                "clean_count": 0, # Aantal sessies sinds leegmaken opvangbakje
                "empty_vacuum": False,  # Stofzuigerbak is in het begin leeg
                "last_clean": datetime(2024, 1, 1), # Initiele vroegere datum
                "clean_interval": config.get("clean_interval", 1),
                "do_not_disturb": config.get("do_not_disturb", None),
                "segments": config.get("segments", None),
                "bin_coordinates": config.get("bin_coordinates", None)
            }
            
            zone = self.zones[item]

            # Push de benodigde sensoren naar HomeAssistant
            self.set_state(f'sensor.{self.mqtt_topic_prefix}_{zone["vacuum"]}_clean_count', state=zone["clean_count"])

            # Luister naar de status van de stofzuiger
            self.listen_event(self.vacuum_status_message, "MQTT_MESSAGE", namespace="mqtt", topic=f'{self.mqtt_topic_prefix}/{zone["vacuum"]}/StatusStateAttribute/status', zone=zone)

        # Luister naar de statusverandering van het alarm
        self.listen_state(self.occupancy_triggered, "alarm_control_panel.huis", namespace="default")

    def occupancy_triggered(self, entity, attribute, old, new, kwargs):
        # Loop door alle gebieden heen
        for zone_name, zone_data in self.zones.items():

            if new == "armed_away":
                # Kijk of er moet worden gestofzuigd
                now = datetime.now().date()
                last_clean = zone_data["last_clean"].date()
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
                    zone_data["last_clean"] = datetime.now()
                    self.log(f'[{zone_name}] Stofzuiger is gestart.')

                else:
                    self.log(f'[{zone_name}] Stofzuiger is niet in dock. Huidige status: {zone_data["state"]}.')
        
            elif new in ['armed_home', 'disarmed', 'armed_night']:
                # Check of een vacuum geleegd moet worden.
                if zone_data["clean_count"] >= zone_data["clean_times"]:
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

        else:
        # Domme aansturing door gewoon te starten met schoonmaken
            topic = f'{self.mqtt_topic_prefix}/{zone_data["vacuum"]}/BasicControlCapability/operation/set'
            payload_data = '{"operation": "START"}'  # Payload voor starten van de stofzuiger
        
        # Zet de Python dictionary om naar een JSON string
        payload = json.dumps(payload_data)
        self.mqtt_publish(topic, payload, qos=1, namespace="mqtt")  # Verzend het MQTT-bericht

        # Update het aantal schoonmaaksessies
        zone_data["clean_count"] += 1
        self.set_state(f'sensor.{self.mqtt_topic_prefix}_{zone_data["vacuum"]}_clean_count', state=zone_data["clean_count"])
    
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
        
        # Reset de counter
        zone_data["clean_count"] = 0
        self.set_state(f'sensor.{self.mqtt_topic_prefix}_{zone_data["vacuum"]}_clean_count', state=zone_data["clean_count"])
        
        self.log(f'[{zone_data["zone"]}] verplaatst naar onderhoudslocatie')

    def vacuum_status_message(self, event, event_data, kwargs):
        # Als de status-message verandert naar 'docked'
        state = event_data.get("payload", None)
        if state == "docked":
            pass
