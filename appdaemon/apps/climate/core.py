class AutoClimate:
    def __init__(self, config):
        """
        Initialize the AutoClimate class with the given configuration.
        
        Args:
            config (dict): Configuration dictionary from YAML.
        """
        self.house_presence = config.get('house_presence')
        self.zones = self.parse_zones(config.get('zones', {}))

    def parse_zones(self, zones_config):
        """
        Parse zone configurations and return structured data.

        Args:
            zones_config (dict): Zones configuration from YAML.

        Returns:
            dict: Parsed zones with their respective configurations.
        """
        zones = {}
        for name, details in zones_config.items():
            zones[name] = {
                'thermostat': details.get('thermostat'),
                'room_presence': details.get('room_presence'),
                'default_target_temp': details.get('default_target_temp', 20),
                'time_schedules': self.parse_schedules(details.get('time_schedules', [])),
                'savings_mode': self.parse_savings_mode(details.get('savings_mode', []))
            }
        return zones
