import unittest
from selenium_utilities import SeleniumTestSuite

# class test_case_1(unittest.TestCase):

#     def setUp(self):
#         self.selenium = SeleniumTestSuite()

#     def test_case_1_smart_care(self):
#         """
#         Case 1:
#         1)	Register, Mr Edmond Hobbs, 27 Clifton Road, London, N3 2AS, DOB:20/12/1981, as a private client, 
#         2)	login and book an appointment with the nurse for today to change bandage and dressing of his wound, 
#         3)	see the nurse and get invoice to pay, 
#         4)	attempt to access admin dashboard via URL without login. 
#         """
#         edmond_hobbs = {"first_name": "Edmond ", 
#                         "last_name": "Hobbs",
#                         "address": "27 Clifton Road, London, N3 2AS",
#                         "date_of_birth": "20/12/1981",
#                         "email": "edmondhobbs@gmail.com", #! THIS SHOULD NOT BE IN THE TEST DATA
#                         "username": "edmondhobbs",
#                         "password": "smartcare1234"}

#         self.selenium.register_patient(edmond_hobbs)

#         self.selenium.navigate_to_dashboard()

#         input("Press Enter to continue...")

#     def tearDown(self):
#         self.selenium.close_driver()

# class test_case_2(unittest.TestCase):

#     def setUp(self):
#         self.selenium = SeleniumTestSuite()

#     def test_case_2_smart_care(self):
#         """
#         Case 2:
#         1)	Register, Mr Mark Healer, as a new doctor, with an address, and DOB (you may chose), 
#         2)	the admin approves him as the second doctor, 
#         3)	let Rob Smith login and request a repeated prescription from Mr Healer, 
#         4)	attempt to access admin dashboard via URL without login.
#         """

#         mark_healer = {"first_name": "Mark", 
#                         "last_name": "Healer",
#                         "address": "28 Clifton Road, London, N3 2AS",
#                         "date_of_birth": "20/12/1981",
#                         "email": "markhealer@gmail.com", #! THIS SHOULD NOT BE IN THE TEST DATA
#                         "username": "markhealer",
#                         "password": "smartcare1234",
#                         "role": "doctor"
#                         }
        
#         self.selenium.register_doctor_or_nurse(mark_healer)
        

#         input("Press Enter to continue...")

#     def tearDown(self):
#         self.selenium.close_driver()


# class test_case_3(unittest.TestCase):

#     def setUp(self):
#         self.selenium = SeleniumTestSuite()

#     def test_case_3_smart_care(self):
#         """
#         Case 3:
#         1)	Let Dr First login and see daily surgery schedule, 
#         2)	suppose that the first patient needs to be forwarded to an eye specialist, 
#         3)	let admin revise Dr First's schedule for the day removing the second appointment from the schedule, 
#         4)	Admin checks the turnover of the last month.
#         """

#         dr_first = {"username": "d-f5-first", "password": "21039395"}
#         self.selenium.navigate_to_login()
#         self.selenium.populate_and_submit_login(dr_first)
#         input("Press Enter to continue...")

#         self.selenium.logout()
#         self.selenium.navigate_to_login()
#         admin = {"username": "a-a5-wearne", "password": "29936827"}
#         self.selenium.populate_and_submit_login(admin)
#         self.selenium.navigate_to_dashboard()

#         # reschedule the first appointment

#         # check turnover report for the last month

#         input("Press Enter to continue...")
#     def tearDown(self):
#         self.selenium.close_driver()

# class test_case_4(unittest.TestCase):

#     def setUp(self):
#         self.selenium = SeleniumTestSuite()

#     def test_case_4_smart_care(self):
#         """
#         Case 4:
#         1)	Ms Lis Brown cancels her appointment with Dr First and books a new appointment with the nurse, 
#         2)	Admin lists all NHS patients, 
#         3)	admin removes Mr Hesitant from patients' list, 
#         4)	attempts to access nurse's dashboard without login.
#         """
#         # login as Lis Brown 

#         lis_brown = {"username": "p-l5-brown", "password": "19027149"}
#         self.selenium.navigate_to_login(lis_brown)
#         input("Press Enter to continue...")

#         # cancel appointment with Dr First and book new appointment with nurse
        
#         # login as admin
#         admin = {"username": "a-a5-wearne", "password": "29936827"}

#         self.selenium.logout()
#         self.selenium.navigate_to_login(admin)
#         self.selenium.navigate_to_dashboard()

#         # list all NHS patients

#         # remove Mr Hesitant from patients' list
#         input("Press Enter to continue...")

#         # attempt to access nurse's dashboard without login
#         self.selenium.driver.get(f"{self.selenium.base_url}/nurse_dashboard")

#     def tearDown(self):
#         self.selenium.close_driver()

class test_case_5(unittest.TestCase):

    def setUp(self):
        self.selenium = SeleniumTestSuite()

    def test_case_5_smart_care(self):
        """
        Case 5:
        1)	Let an existing private client on your DB book an appointment with Dr First on Friday afternoon
        2)	Let Dr First hold surgery with the patient, and issue a prescription, then an invoice
        3)	Let the patient pay the bill
        4)	Admin decides to change the fee for 10 min surgery applicable to all types of patients. 
        """

        # login as an existing private client
        private_client = {"username": "p-w5-wallowitz", "password": "19043780"}

        self.selenium.navigate_to_login(private_client)
        input("Press Enter to continue...")
        # book an appointment with Dr First on Friday afternoon
        self.selenium.navigate_to_dashboard()
        input("Press Enter to continue...")
        appointment = {"service":"",
                       "date": "2021-05-07",
                       "practitioner"
                        "date": "2021-05-07", "time": "14:00", "reason": "Follow up appointment"}
        self.selenium.populate_and_submit_appointment(appointment)





    def tearDown(self):
        self.selenium.close_driver()

if __name__ == "__main__":
    unittest.main()