def absence_duration_exceeds(absence_start, delay_minutes):
    """
    Check if the absence duration exceeds the given delay.

    Args:
        absence_start (datetime): Time the absence began.
        delay_minutes (int): Duration in minutes.

    Returns:
        bool: True if the absence exceeds the duration, False otherwise.
    """
    from datetime import datetime, timedelta
    return datetime.now() >= absence_start + timedelta(minutes=delay_minutes)
