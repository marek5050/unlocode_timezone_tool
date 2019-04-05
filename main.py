import dateutil.parser
from timezonefinder import TimezoneFinder
from pytz import timezone
import pytz
from datetime import datetime
utc = pytz.utc
import mySQL
from dotenv import load_dotenv
load_dotenv()
import os
CONFIG = {"MYSQL_EP": os.getenv("MYSQL_EP", None)}


tf = TimezoneFinder()


# def get_timezone(coordinates):
#     result = tf.closest_timezone_at(lat=coordinates[0], lng=coordinates[1])  # correct but much slower
#     return result


def get_row(unlocode):
    global CONFIG

    if "MYSQL_EP" not in CONFIG:
        return "no connection string"

    try:
        engine, session = mySQL.start_mysql_session(CONFIG)
        """if session is None:
            return "bad connection string"
            """

        rs = session.query(mySQL.UNLocode).filter(mySQL.UNLocode.id==unlocode).first() #('SELECT * FROM unlocode_list_with_gps WHERE id LIKE "%s"' %unlocode)
        return rs

    except Exception as e:
        return "bad connection string: %s" %e


def get_timezone(row_from_db):
    return tf.closest_timezone_at(lat=row_from_db.lat, lng=row_from_db.lng)


def get_local_time(target, timestamp = datetime.now()):
    """
    returns a location's time zone offset from UTC in minutes.
    """

    if isinstance(timestamp,datetime) == False:
        if isinstance(timestamp,int): ### Convert from Unix Epoch to Datetime
            timestamp = datetime.fromtimestamp(timestamp, pytz.utc)
        else: ### Parse IS8601 to Datetime
            timestamp = dateutil.parser.parse(timestamp)

    tz_target = timezone(tf.closest_timezone_at(lat=target["lat"], lng=target["lng"]))
    # ATTENTION: tz_target could be None! handle error case
    if tz_target is None:
        return timestamp

    target_timezone = timestamp.astimezone(tz_target)

    return target_timezone.isoformat()
