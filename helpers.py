import datetime

def add_to_hour(hours, minutes, minutes_to_add):
    minutes += minutes_to_add
    hours += minutes / 60
    minutes %= 60
    return (hours, minutes)


def timerange_to_datetime(hour, minutes, duration_minutes):
    '''
    Returns a tuple (event_start, event_end)
    '''
    event_start = hour_to_datetime(hour, minutes)
    event_end = event_start + datetime.timedelta(minutes = duration_minutes)

    return (event_start, event_end)


def hour_to_datetime(hour, minutes):
    """
    Returns a datetime with the passed hour and minutes
    """
    event_date = datetime.date.today()
    event_time = datetime.time(hour, minutes)
    event_start = datetime.datetime.combine(event_date, event_time)
    return event_start
