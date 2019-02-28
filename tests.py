import unittest
import main
from dotenv import load_dotenv
import os


class TestCrashTypes(unittest.TestCase):

    def setUp(self):
        main.CONFIG = {"MYSQL_EP": os.getenv("MYSQL_EP", None)}
        pass

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

    def test_sql_credentials_incorrect(self):
        main.CONFIG= {"MYSQL_EP": "bad string"}
        unlocode = "USHOU"
        row_from_db = main.get_row(unlocode)
        self.assertEqual(row_from_db, "bad connection string")













if __name__ == '__main__':
    unittest.main()