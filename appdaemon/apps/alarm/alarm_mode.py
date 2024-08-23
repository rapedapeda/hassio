import appdaemon.plugins.hass.hassapi as hass

class AlarmMode(hass.Hass):
    """
    AppDaemon-app voor het beheren van de alarmstatus op basis van aanwezigheid en tijd van de dag.
    """

    def initialize(self):
        """
        Initialiseert de app door:
        - Luisteren naar veranderingen in de aanwezigheidstoestand van alle gedefinieerde personen
        - Planning van callbacks voor zonsondergang en zonsopgang met offsets
        - Voer een initiële controle van de alarmstatus uit
        """
        
        # Verkrijg alle device_tracker entiteiten
        self.trackers = self.get_trackers()
        self.log(f'Trackers: {self.trackers}')
        
        # Dynamisch luisteren naar de aanwezigheidstoestand van elke tracker
        for tracker in self.trackers:
            self.listen_state(self.handle_alarm, tracker)
        
        # Plan callbacks voor zonsondergang en zonsopgang
        self.run_at_sunrise(self.handle_alarm, offset=3600)
        self.run_at_sunset(self.handle_alarm, offset=-3600)  # 15 minuten voor zonsondergang

        # Voer een initiële controle van de alarmstatus uit
        self.handle_alarm()

    def handle_alarm(self, *args, **kwargs):
        """
        Behandelt het instellen van de alarmstatus op basis van aanwezigheid en tijd van de dag.
        """
        night = self.now_is_between("sunset - 01:00:00", "sunrise + 01:00:00")

        if self.noone_home():
            self.call_service("alarm_control_panel/alarm_arm_away", entity_id="alarm_control_panel.huis", code=0000)
        elif self.anyone_home():
            if night:
                self.call_service("alarm_control_panel/alarm_arm_home", entity_id="alarm_control_panel.huis", code=0000)
            else:
                self.call_service("alarm_control_panel/alarm_disarm", entity_id="alarm_control_panel.huis", code=0000)