import appdaemon.plugins.hass.hassapi as hass

class RoomLighting(hass.Hass):
    """
    RoomLighting class: Automatisering voor verlichting op basis van beweging en lux-waarde.

    Deze AppDaemon-applicatie schakelt de verlichting in of uit op basis van beweging en de hoeveelheid omgevingslicht. 
    Het houdt rekening met een instelbare lux-drempelwaarde en een uitschakelvertraging.
    """

    def initialize(self):
        """
        Initialiseer de RoomLighting-app voor een kamer.

        Haalt alle benodigde parameters op uit de configuratie en luistert naar veranderingen in 
        de bewegingssensor en lux-sensor om de verlichting te automatiseren.

        Configuratieparameters:
        - room_name: Naam van de ruimte (bijv. 'Woonkamer').
        - motion_sensor: Entiteit voor de bewegingssensor (bijv. 'binary_sensor.motion_sensor').
        - light_sensor: Entiteit voor de lux-sensor (bijv. 'sensor.light_sensor').
        - light_threshold: Entiteit (input_number) voor de lux-drempelwaarde (bijv. 'input_number.light_threshold').
        - light_delay: Entiteit (input_number) voor de uitschakelvertraging in seconden (bijv. 'input_number.light_delay').
        - lights: Entiteit of groep van entiteiten voor de verlichting (bijv. 'light.living_room').

        Standaardwaarden:
        - default_light_delay: 300 seconden (5 minuten).
        """
        self.room_name = self.args.get("room_name")
        self.lights = self.args.get("lights")
        self.motion_sensor = self.args.get("motion_sensor")
        self.light_sensor = self.args.get("light_sensor")
        self.light_threshold_entity = self.args.get("light_threshold")
        self.light_delay_entity = self.args.get("light_delay")  # Dit is nu een entiteit zoals 'input_number.light_delay'
        self.default_light_delay = 300  # Standaard 5 minuten

        self.motion_timer = None
        self.lux_timer = None

        # Luister naar veranderingen in beweging en lux-waarde
        self.listen_state(self.motion_detected, self.motion_sensor)
        self.listen_state(self.lux_changed, self.light_sensor)

    def get_light_delay(self):
        """
        Haalt de uitschakelvertraging op vanuit de input_number-entiteit, of gebruikt de standaardwaarde.

        Returns:
            int: De uitschakelvertraging in seconden.
        """
        if self.light_delay_entity:
            delay = self.get_state(self.light_delay_entity)
            if delay is not None:
                return int(float(delay))  # Zorg dat het omgezet wordt naar een integer
        return self.default_light_delay

    def motion_detected(self, entity, attribute, old, new, kwargs):
        """
        Callback voor wanneer beweging gedetecteerd wordt door de bewegingssensor.

        Parameters:
            entity (str): De entiteit die de trigger veroorzaakt.
            attribute (str): Het attribuut dat is gewijzigd.
            old (str): De oude status van de sensor.
            new (str): De nieuwe status van de sensor.
        """
        if new == "on":  # Beweging gedetecteerd
            lux = float(self.get_state(self.light_sensor))
            threshold = float(self.get_state(self.light_threshold_entity))
            if lux < threshold:  # Te weinig daglicht
                self.log(f"Lampen aan in {self.room_name} vanwege beweging en onvoldoende licht")
                self.turn_on(self.lights)

            # Annuleer de uitschakeltimer als die actief is
            if self.motion_timer:
                self.cancel_timer(self.motion_timer)
                self.motion_timer = None
        else:  # Geen beweging meer gedetecteerd
            # Start timer om lampen uit te schakelen na de ingestelde vertraging
            light_delay = self.get_light_delay()
            self.motion_timer = self.run_in(self.turn_off_lights, light_delay)

    def lux_changed(self, entity, attribute, old, new, kwargs):
        """
        Callback voor wanneer de lux-waarde verandert.

        Parameters:
            entity (str): De entiteit die de trigger veroorzaakt.
            attribute (str): Het attribuut dat is gewijzigd.
            old (str): De oude lux-waarde.
            new (str): De nieuwe lux-waarde.
        """
        new_lux = float(new)
        threshold = float(self.get_state(self.light_threshold_entity))

        # Monitor of de lux-waarde gedurende de ingestelde delay boven/onder de drempel blijft
        light_delay = self.get_light_delay()
        if new_lux < threshold:
            if not self.lux_timer:
                self.lux_timer = self.run_in(self.check_lux_below_threshold, light_delay)
        else:
            if not self.lux_timer:
                self.lux_timer = self.run_in(self.check_lux_above_threshold, light_delay)

    def check_lux_below_threshold(self, kwargs):
        """
        Controleert na de delay of de lux-waarde nog steeds onder de drempel ligt en schakelt zo nodig de verlichting in.

        Parameters:
            kwargs (dict): Eventuele extra argumenten (niet gebruikt).
        """
        current_lux = float(self.get_state(self.light_sensor))
        threshold = float(self.get_state(self.light_threshold_entity))
        if current_lux < threshold and self.get_state(self.motion_sensor) == "on":
            self.log(f"Lampen aan in {self.room_name} vanwege afgenomen daglicht")
            self.turn_on(self.lights)

        # Reset de lux timer
        self.lux_timer = None

    def check_lux_above_threshold(self, kwargs):
        """
        Controleert na de delay of de lux-waarde nog steeds boven de drempel ligt en schakelt zo nodig de verlichting uit.

        Parameters:
            kwargs (dict): Eventuele extra argumenten (niet gebruikt).
        """
        current_lux = float(self.get_state(self.light_sensor))
        threshold = float(self.get_state(self.light_threshold_entity))
        if current_lux > threshold:
            self.log(f"Lampen uit in {self.room_name} vanwege toegenomen daglicht")
            self.turn_off(self.lights)

        # Reset de lux timer
        self.lux_timer = None

    def turn_off_lights(self, kwargs):
        """
        Schakelt de verlichting uit als er geen beweging meer gedetecteerd wordt.

        Parameters:
            kwargs (dict): Eventuele extra argumenten (niet gebruikt).
        """
        if self.get_state(self.motion_sensor) == "off":
            self.log(f"Lampen uit in {self.room_name} vanwege inactiviteit")
            self.turn_off(self.lights)
