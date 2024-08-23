import appdaemon.plugins.hass.hassapi as hass

class AlarmMode(hass.Hass):
    """
    AppDaemon-app voor het beheren van de alarmstatus op basis van aanwezigheid en tijd van de dag.
    """

    def initialize(self):
        """
        Initialiseert de app door:
        - Luisteren naar veranderingen in de aanwezigheidstoestand
        - Planning van callbacks voor zonsondergang en zonsopgang met offsets
        - Voer een initiële controle van de alarmstatus uit
        """
        self.log("Hello from AlarmMode")
        # Luister naar veranderingen in de aanwezigheidstoestand
        self.listen_state(self.handle_alarm, "input_boolean.presence_status")

        # Plan callbacks voor zonsondergang en zonsopgang
        self.run_at_sunrise(self.handle_alarm, ofset=3600)
        self.run_at_sunset(self.handle_alarm, offset=-3600)  # 15 minuten voor zonsondergang

        # Voer een initiële controle van de alarmstatus uit
        self.handle_alarm()

    def handle_alarm(self, *args, **kwargs):
        """
        Behandelt het instellen van de alarmstatus op basis van aanwezigheid en tijd van de dag.
        """
        presence_status = self.get_state("input_boolean.presence_status")
        now = self.datetime()
        sun_data = self.get_state("sun.sun", attribute="attributes")
        
        # Verkrijg de tijden van zonsopgang en zonsondergang
        next_rising = self.parse_datetime(sun_data.get("next_rising"))
        next_setting = self.parse_datetime(sun_data.get("next_setting"))

        if presence_status == 'off':
            self.call_service("alarm_control_panel/alarm_arm_away", entity_id="alarm_control_panel.huis")
        elif presence_status == 'on':
            if (next_rising - next_setting).total_seconds() < 0 or (next_setting - now).total_seconds() < 2700:
                self.call_service("alarm_control_panel/alarm_arm_home", entity_id="alarm_control_panel.huis")
            else:
                self.call_service("alarm_control_panel/alarm_disarm", entity_id="alarm_control_panel.huis")

    def sunrise_cb(self, *args, **kwargs):
        """
        Callback functie die wordt aangeroepen bij zonsopgang.
        """
        self.handle_alarm()

    def before_sunset_cb(self, *args, **kwargs):
        """
        Callback functie die wordt aangeroepen 15 minuten vóór zonsondergang.
        """
        self.handle_alarm()
