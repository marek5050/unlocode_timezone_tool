import base64
import unittest
import main
import os

class Coordinates():
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        ep = os.getenv("MYSQL_EP", None)
        if ep is not None:
            enc = base64.b64decode(ep)
            if enc is not None:
                main.CONFIG = {"MYSQL_EP": enc.decode("utf-8")}
        else:
            main.CONFIG = {"MYSQL_FILE": "dataset/unlocode_list_with_gps.csv"}
        pass

    def test_get_timezone1(self): #unit test 1
        coordinates = Coordinates(-37.31, 145.21)
        tz = main.get_timezone(coordinates)
        self.assertIsNotNone(tz)
        self.assertEqual("Australia/Melbourne", tz)

    def test_get_timezone2(self): #unit test 2
        coordinates = Coordinates(47.42, -3.06)
        tz = main.get_timezone(coordinates)
        self.assertIsNotNone(tz)
        self.assertEqual("Europe/Paris", tz)

    def test_get_timezone3(self): #unit test 3
        coordinates = Coordinates(45.47, 47.32)
        tz = main.get_timezone(coordinates)
        self.assertIsNotNone(tz)
        self.assertEqual("Europe/Astrakhan", tz)

    def test_mainSomething(self):
        unlocode = "AUN7K"

        row_from_db = main.get_row(unlocode)
        self.assertEqual([row_from_db.lat,row_from_db.lng], [-37.31, 145.21])

        timezone = main.get_timezone(row_from_db)
        self.assertEqual(timezone, "Australia/Melbourne")

        returnvalue = row_from_db.__dict__

        returnvalue["timezone"] = timezone
        returnvalue["current_time"] = main.get_local_time(returnvalue)

        print(returnvalue["current_time"])  ## 2019-02-20T10:54:26+11:00
        self.assertTrue("+11:00" in returnvalue["current_time"] or "+10:00" in returnvalue["current_time"])

        return returnvalue


    def test_mainSomething2(self):
        unlocode = "USHOU"

        row_from_db = main.get_row(unlocode)
        self.assertEqual([row_from_db.lat,row_from_db.lng], [29.45, -95.21])

        timezone = main.get_timezone(row_from_db)
        self.assertEqual(timezone, "America/Chicago")

        returnvalue = row_from_db.__dict__

        returnvalue["timezone"] = timezone
        returnvalue["current_time"] = main.get_local_time(returnvalue)

        print(returnvalue["current_time"])  ## 2019-02-20T10:54:26+11:00
        self.assertTrue("-05:00" in returnvalue["current_time"] or "-06:00" in returnvalue["current_time"]) # Added DST

        return returnvalue


    def test_offset(self):

        bergamo = dict({'lat': 45.69, 'lng': 9.67})
        print(main.get_local_time(bergamo))

    def test_get_row(self):
        unlocode = "AUN7K"
        result = main.get_row(unlocode)
        self.assertIsNotNone(result)
        self.assertEqual(result.lat, -37.31)
        self.assertEqual(result.lng, 145.21)

    def test_get_row_file(self):
        unlocode = "AUN7K"
        if "MYSQL_EP" in main.CONFIG:
            del main.CONFIG["MYSQL_EP"]
        main.CONFIG["MYSQL_FILE"]="dataset/unlocode_list_with_gps.csv"
        result = main.get_row(unlocode)
        self.assertIsNotNone(result)
        self.assertEqual(result.lat, -37.31)
        self.assertEqual(result.lng, 145.21)


    ### Tests for daylight savings in San Francisco -> DST -8 -> -7 Mar3-Nov3
    def test_DaylightSavings1Epoch(self):
        unlocode = "USSFO"
        timestampInEpoch = 1549367920000

        row_from_db = main.get_row(unlocode)
        self.assertEqual([row_from_db.lat, row_from_db.lng], [37.77, -122.41])

        timezone = main.get_timezone(row_from_db)
        self.assertEqual(timezone, "America/Los_Angeles")

        returnvalue = row_from_db.__dict__

        returnvalue["timezone"] = timezone
        returnvalue["current_time"] = main.get_local_time(returnvalue,timestampInEpoch)

        # print(returnvalue["current_time"])  ## 2019-02-05T03:58:40-08:00
        self.assertTrue("-08:00" in returnvalue["current_time"])

        return returnvalue

    def test_DaylightSavings2Epoch(self):
        unlocode = "USSFO"
        timestampInEpoch = int("1554465520000")

        row_from_db = main.get_row(unlocode)
        self.assertEqual([row_from_db.lat, row_from_db.lng], [37.77, -122.41])

        timezone = main.get_timezone(row_from_db)
        self.assertEqual(timezone, "America/Los_Angeles")

        returnvalue = row_from_db.__dict__

        returnvalue["timezone"] = timezone
        returnvalue["current_time"] = main.get_local_time(returnvalue,timestampInEpoch)

        # print(returnvalue["current_time"])  ## 2019-04-05T04:58:40-07:00
        self.assertTrue("-07:00" in returnvalue["current_time"])

        return returnvalue



        # 2018 -> -8  then -7 from DST Mar 11, 2018 -> Nov 4 2018
    def test_DaylightSavings1Timestamp(self):
        unlocode = "USSFO"
        timestamp = "2018-02-05T03:58:40-00:00"

        row_from_db = main.get_row(unlocode)
        self.assertEqual([row_from_db.lat, row_from_db.lng], [37.77, -122.41])

        timezone = main.get_timezone(row_from_db)
        self.assertEqual(timezone, "America/Los_Angeles")

        returnvalue = row_from_db.__dict__

        returnvalue["timezone"] = timezone
        returnvalue["current_time"] = main.get_local_time(returnvalue,timestamp)

        # print(returnvalue["current_time"])  ## 2018-02-04T19:58:40-08:00
        self.assertTrue("-08:00" in returnvalue["current_time"])

        return returnvalue

    def test_DaylightSavings2Timestamp(self):
        unlocode = "USSFO"
        timestamp = "2018-03-12T03:58:40-00:00"

        row_from_db = main.get_row(unlocode)
        self.assertEqual([row_from_db.lat, row_from_db.lng], [37.77, -122.41])

        timezone = main.get_timezone(row_from_db)
        self.assertEqual(timezone, "America/Los_Angeles")

        returnvalue = row_from_db.__dict__

        returnvalue["timezone"] = timezone
        returnvalue["current_time"] = main.get_local_time(returnvalue,timestamp)

        # print(returnvalue["current_time"])  ## 2018-03-11T20:58:40-07:00
        self.assertTrue("-07:00" in returnvalue["current_time"])

        return returnvalue


    def test_incorrect_unlocode(self):  #tests for incorrect unlocode input ex. user inputs HOUST instead of USHOU
        unlocode = "HOUST"
        row_from_db = main.get_row(unlocode)
        self.assertIsNone(row_from_db)

    def test_unlocode_total(self):  # tests that there are five characters total
        unlocode = "USHOU"
        row_from_db = main.get_row(unlocode)
        self.assertEqual(len(row_from_db.id), 5)

    def test_unlocode_first_two(self): #tests to make sure the first two characters are letters
        unlocode = "USHOU"
        row_from_db = unlocode[:2]
        self.assertTrue(row_from_db.isalpha())

    def test_unlocode_last_three(self): #tests that the last three are letters or digits
        unlocode = "USHOU"
        row_from_db = unlocode[-3:]
        self.assertTrue(row_from_db.isalnum())

    def test_sql_credentials_missing(self):
        main.CONFIG= {}
        unlocode = "USHOU"
        row_from_db = main.get_row(unlocode)
        self.assertEqual(row_from_db,"no connection string")

    # def test_sql_credentials_incorrect(self):
    #     main.CONFIG= {"MYSQL_EP": "bad string"}
    #     unlocode = "USHOU"
    #     row_from_db = main.get_row(unlocode)
    #     self.assertEqual(row_from_db, "bad connection string")





    #def test_attempt1(self):





if __name__ == '__main__':
    unittest.main()