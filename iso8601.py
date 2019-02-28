from pytz import timezone
import pytz
from datetime import datetime

utc = pytz.utc

def offset(coordinates):
    """
    returns a location's time zone offset from UTC in minutes.
    """
    today = datetime.now()
    tz_target = timezone(tf.closest_timezone_at(lat=coordinates[0], lng=coordinates[1]))
    # ATTENTION: tz_target could be None! handle error case
    today_target = tz_coordinates.localize(today)
    today_utc = utc.localize(today)
    return (today_utc - today_target).total_seconds() / 60

bergamo = dict({'lat':45.69, 'lng':9.67})
print(offset(bergamo))

