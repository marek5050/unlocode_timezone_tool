import unittest
import main

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_timezone1(self): #unit test 1
        coordinates = [-37.31, 145.21]
        tz = main.get_timezone(coordinates)
        self.assertIsNotNone(tz)
        self.assertEqual("Australia/Melbourne", tz)

    def test_get_timezone2(self): #unit test 2
        coordinates = [47.42, -3.06]
        tz = main.get_timezone(coordinates)
        self.assertIsNotNone(tz)
        self.assertEqual("Europe/Paris", tz)

    def test_get_timezone3(self): #unit test 3
        coordinates = [45.47, 47.32]
        tz = main.get_timezone(coordinates)
        self.assertIsNotNone(tz)
        self.assertEqual("Europe/Astrakhan", tz)

    def test_mainSomething(self):
        unlocode = "AUN7K"

        row_from_db = main.get_row(unlocode)
        self.assertEqual([row_from_db.lat,row_from_db.lng], [-37.31, 145.21])

        timezone = main.get_timezone123(row_from_db)
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

        timezone = main.get_timezone123(row_from_db)
        self.assertEqual(timezone, "America/Chicago")

        returnvalue = row_from_db.__dict__

        returnvalue["timezone"] = timezone
        returnvalue["current_time"] = main.get_local_time(returnvalue)

        print(returnvalue["current_time"])  ## 2019-02-20T10:54:26+11:00
        self.assertTrue("-06:00"in returnvalue["current_time"])

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



    #def test_attempt1(self):





if __name__ == '__main__':
    unittest.main()