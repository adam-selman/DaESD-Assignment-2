import unittest
from selenium_utilities import SeleniumTestSuite

class test_case_1(unittest.TestCase):

    def setUp(self):
        self.selenium = SeleniumTestSuite()

    def test_case_1_smart_care(self):
        """
        Case 1:
        1)	Register, Mr Edmond Hobbs, 27 Clifton Road, London, N3 2AS, DOB:20/12/1981, as a private client, 
        2)	login and book an appointment with the nurse for today to change bandage and dressing of his wound, 
        3)	see the nurse and get invoice to pay, 
        4)	attempt to access admin dashboard via URL without login. 
        """
        edmond_hobbs = {"first_name": "Edmond ", 
                        "last_name": "Hobbs",
                        "address": "27 Clifton Road, London, N3 2AS",
                        "date_of_birth": "20/12/1981",
                        "email": "edmondhobbs@gmail.com", #! THIS SHOULD NOT BE IN THE TEST DATA
                        "username": "edmondhobbs",
                        "password": "smartcare1234"}

        self.selenium.register_user(edmond_hobbs)

        self.selenium.navigate_to_dashboard()

        input("Press Enter to continue...")

    def tearDown(self):
        self.selenium.close_driver()

class test_case_2(unittest.TestCase):

    def setUp(self):
        self.selenium = SeleniumTestSuite()

    def test_case_2_smart_care(self):
        """
        Case 2:
        1)	Register, Mr Mark Healer, as a new doctor, with an address, and DOB (you may chose), 
        2)	the admin approves him as the second doctor, 
        3)	let Rob Smith login and request a repeated prescription from Mr Healer, 
        4)	attempt to access admin dashboard via URL without login.
        """

    mark_healer = {"first_name": "Mark", 
                    "last_name": "Healer",
                    "address": "27 Clifton Road, London, N3 2AS",
                    "date_of_birth": "20/12/1981",
                    "email": "markhealer@gmail.com", #! THIS SHOULD NOT BE IN THE TEST DATA
                    
                    "username": "markhealer",
                    "password": "smartcare1234"}
    def tearDown(self):
        self.selenium.close_driver()

if __name__ == "__main__":
    unittest.main()