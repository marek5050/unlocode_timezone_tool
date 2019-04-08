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


class Row():
    def __init__(self, id, country, location, name, lat, lng):
        self.id = id
        self.country = country
        self.location = location
        self.name= name
        try:
            self.lat = float(lat)
            self.lng = float(lng)
        except:
            self.lat = None
            self.lng = None
        

# def get_timezone(coordinates):
#     result = tf.closest_timezone_at(lat=coordinates[0], lng=coordinates[1])  # correct but much slower
#     return result

def read_csv(CONFIG):
    import csv
    if "MYSQL_FILE" not in CONFIG:
        return "No file"

    filename = CONFIG["MYSQL_FILE"]
    db = dict()

    with open(filename) as input_file:
        f1 = csv.DictReader(input_file)
        for row in f1:
            db[row["id"]]=Row(**row)
    return db

def get_row(unlocode):
    global CONFIG

    if "MYSQL_EP" not in CONFIG:
        if "MYSQL_FILE" not in CONFIG:
            return "no connection string"
        elif "MYSQL_FILE" in CONFIG:
            db = read_csv(CONFIG)
            if unlocode in db:
                return db[unlocode]
            else:
                return None

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
            if timestamp > 1054465520000: ## the script complains about milliseconds
                timestamp = int(timestamp/1000)
            timestamp = datetime.fromtimestamp(timestamp, pytz.utc)
        else: ### Parse IS8601 to Datetime
            timestamp = dateutil.parser.parse(timestamp)

    tz_target = timezone(tf.closest_timezone_at(lat=target["lat"], lng=target["lng"]))
    # ATTENTION: tz_target could be None! handle error case
    if tz_target is None:
        return timestamp

    target_timezone = timestamp.astimezone(tz_target)

    return target_timezone.isoformat()
