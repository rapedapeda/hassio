import appdaemon.plugins.hass.hassapi as hass

class AlarmTrigger(hass.Hass):
    """
    AppDaemon-app voor het triggeren van het alarm op basis van sensorstatussen.
    """

    def initialize(self):
        """
        Initialiseert de app door:
        - Luisteren naar statusveranderingen van gespecificeerde sensor-groepen
        """
        self.sensor_configurations = self.args.get("sensor_configurations", {})

        for group, required_states in self.sensor_configurations.items():
            self.listen_state(self.check_sensors, group, any=True)

    def check_sensors(self, entity, attribute, old, new, kwargs):
        """
        Controleert de status van de sensors en activeert het alarm indien nodig.
        """
        alarm_state = self.get_state("alarm_control_panel.huis")
        
        for group, required_states in self.sensor_configurations.items():
            if entity.startswith(group):
                if any(state in required_states for state in [alarm_state]) and new == 'on':
                    self.call_service("alarm_control_panel/alarm_trigger", entity_id="alarm_control_panel.huis")
