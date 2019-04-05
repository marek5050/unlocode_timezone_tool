import unittest
import main


class Coordinates():
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

class TestStringMethods(unittest.TestCase):
    def setUp(self):
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
        self.assertTrue("+11:00"in returnvalue["current_time"])

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


    ### Tests for daylight savings in San Francisco -> DST -8 -> -7 Mar3-Nov3
    def test_DaylightSavings1Epoch(self):
        unlocode = "USSFO"
        timestampInEpoch = int(int("1549367920000")/1000)

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
        timestampInEpoch = int(int("1554465520000")/1000)

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


    #def test_attempt1(self):





if __name__ == '__main__':
    unittest.main()