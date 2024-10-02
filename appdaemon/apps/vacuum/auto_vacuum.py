import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta

class AutoVacuum(hass.Hass):
    
    def initialize(self):
        self.last_cleaned = {}
        self.do_not_disturb = self.args["do_not_disturb"]
        self.mqtt_topic_prefix = self.args["mqtt_topic_prefix"]
        
        # Dictionary voor alle areas met hun relevante gegevens (vacuum, state, empty)
        self.zones = {}

        # Initialiseer alle areas en luister naar de alarmstatus
        for item, config in self.args["zones"].items():

            # Maak een entry in de dictionary voor dit area met de attributen vacuum, state en empty
            self.zones[item] = {
                "zone": item # Naam van de zone (voor loggingdoeleinden)
                "vacuum": config["vacuum"],  # Naam van de stofzuiger
                "state": None,  # Status van de stofzuiger
                "area": config["area"]
                "area_cleaned": 0 # aantal cm schoongemaakt sinds leegmaken opvangbakje
                "empty_vacuum": False  # Stofzuigerbak is in het begin leeg
                "last_clean": datetime(2024, 1, 1) # Initiele vroegere datum
                "clean_interval": config["clean_interval"]
                "do_not_disturb": config["do_not_disturb"]
                "segments": config["segments"]
            }
            
            zone = self.zones[item]
            # Subscribe naar de MQTT van de stofzuiger
            self.mqtt_subscribe(f"{self.mqtt_topic_prefix}/zone["vacuum"]")

            # Luister naar de status van de stofzuiger
            self.listen_event(self.vacuum_status_message, "MQTT_MESSAGE", topic=f"{self.mqtt_topic_prefix}/{zone["vacuum"]}/StatusStateAttribute/status")

            # Luister naar een verandering in de total cleaned area
            self.listen_event(self.update_cleaned_area, "MQTT_MESSAGE", topic=f"{self.mqtt_topic_prefix}/{zone["vacuum"]}/TotalStatisticsCapability/area")

        # Luister naar de statusverandering van het alarm
        self.listen_state(self.occupancy_triggered, "alarm_control_panel.huis")

    def occupancy_triggered(self, entity, attribute, old, new, kwargs):
        if new is "armed_away":
            # Loop door alle gebieden heen
            for item in self.zones.items():
                zone = self.zones[item]

                # Kijk of er moet worden gestofzuigd
                now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                last_clean = zone["last_clean"].replace(hour=0, minute=0, second=0, microsecond=0)
                if (now - last_clean).days < zone["clean_interval"]:
                    self.log(f"[{zone["zone"]}] schoonmaakinterval nog niet overschreden, stofzuiger niet gestart.")
                    continue

                # Kijk of er mag worden gestofzuigd
                if zone["do_not_disturb"] and self.now_is_between(self.do_not_disturb[0], self.do_not_disturb[1]):
                    self.log(f"[{zone["zone"]}] Do Not Disturb actief, stofzuiger niet gestart.")
                    continue
                
                # Controleer de status van de stofzuiger
                vacuum_state = self.get_state(zone)
                if vacuum_state == "docked":
                    # Start de stofzuiger als hij in de dock staat
                    self.start_vacuum(zone)
                    self.log(f"[{zone["zone"]}] Stofzuiger {zone["vacuum"]} is gestart.")

                else:
                    self.log(f"[{area}] Stofzuiger is niet in dock. Huidige status: {zone["state"]}.")
        
        else:
            # Check of een vacuum geleegd moet worden.
            # Laat het naar de goede locatie gaan
            pass

    def start_vacuum(self, zone):
        if zone["segments"]:
            topic = f"{self.mqtt_topic_prefix}/{zone["vacuum"]}/MapSegmentationCapability/clean/set"
            payload = '{"segment_ids": ["17", "16", "18"], "iterations": 2}'

        else:
        # Domme aansturing door gewoon te starten met schoonmaken
            topic = f"{self.mqtt_topic_prefix}/{zone["vacuum"]}/BasicControlCapability/operation/set"
            payload = '{"operation": "START"}'  # Payload voor starten van de stofzuiger

        self.mqtt_publish(topic, payload, qos=1)  # Verzend het MQTT-bericht



    def vacuum_status_message(self, entity, attribute, old, new, kwargs):
        # Als de status-message verandert naar 'docked'


        # Plus de valetudo/snuffel/CurrentStatisticsCapability/area bij de self.areas etc op
        # Maar alleen als 

            # Zet eventueel emty_vacuum op True
        pass

