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


def get_timezone(coordinates):
    result = tf.closest_timezone_at(lat=coordinates[0], lng=coordinates[1])  # correct but much slower
    return result



"""
def mainSomething():

    my_array = [[-37.31, 145.21], [47.42, -3.06], [22.28, 114.18], [54.56, -7.27], [15.09, 74.03], [41.1, 16.69], [36.61, 127.42], [23.55, -106.25], [33.26, -94.25], [45.47, 47.32] ]
    for coordinates in my_array:
            result = tf.closest_timezone_at(lat=coordinates[0], lng = coordinates[1])
            print(result)
"""

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


def get_timezone123(row_from_db):
    return tf.closest_timezone_at(lat=row_from_db.lat, lng=row_from_db.lng)


def get_local_time(target):
    """
    returns a location's time zone offset from UTC in minutes.
    """

    today = datetime.now()
    tz_target = timezone(tf.closest_timezone_at(lat=target["lat"], lng=target["lng"]))
    # ATTENTION: tz_target could be None! handle error case
    today_target = tz_target.localize(today)

    return today_target.isoformat()
