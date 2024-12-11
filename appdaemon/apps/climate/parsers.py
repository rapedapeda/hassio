# parsers.py

def parse_zones(zones_config):
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
            'time_schedules': parse_schedules(details.get('time_schedules', [])),
            'savings_mode': details.get('savings_mode', [])
        }
    return zones

def parse_schedules(schedules):
    """
    Parse time schedules into structured format.

    Args:
        schedules (list): List of schedule dictionaries.

    Returns:
        list: List of parsed schedule dictionaries.
    """
    parsed = []
    for schedule in schedules:
        days = expand_days(schedule.get('days', ''))
        parsed.append({
            'days': days,
            'start': schedule.get('start'),
            'end': schedule.get('end'),
            'target_temp': schedule.get('target_temp')
        })
    return parsed

def expand_days(days):
    """
    Expand day ranges or groups into individual days.

    Args:
        days (str): Comma-separated days or ranges (e.g., "monday-friday").

    Returns:
        list: List of individual days.
    """
    # Placeholder for day expansion logic
    return days.split(',')
