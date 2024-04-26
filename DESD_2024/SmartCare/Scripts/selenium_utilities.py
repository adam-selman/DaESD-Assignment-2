from time import sleep

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class SeleniumTestSuite:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.driver = self.get_driver()

    def install_chromedriver(self):
        """
        Installs a chromedriver if not already installed
        """
        chromedriver_autoinstaller.install()

    def get_driver(self):
        """
        Returns a Chrome driver instance

        Returns:
            Chrome : Chrome driver instance
        """
        self.install_chromedriver()
        return webdriver.Chrome()

    def close_driver(self):
        """
        Closes the Chrome driver instance
        """
        self.driver.close()

    def get_element_by_id(self, element_id: str) -> WebElement:
        """
        Return a single element by its ID

        Args:
            driver (Chrome): Chrome driver instance
            element_id (str): ID of the element to be found

        Returns:
            WebElement: Element found by ID
        """
        return self.driver.find_element(By.ID, element_id)

    def get_element_by_name(self, element_name: str) -> WebElement:
        """
        Return a single element by its name

        Args:
            driver (Chrome): Chrome driver instance
            element_name (str): name value of the element to be found

        Returns:
            WebElement: Element found by ID
        """
        return self.driver.find_element(By.NAME, element_name)

    def get_element_by_class_name(self, element_class_name: str) -> WebElement:
        """
        Return a single element by its class

        Args:
            driver (Chrome): Chrome driver instance
            element_class_name (str): class name of the element to be found

        Returns:
            WebElement: Element found by ID
        """
        return self.driver.find_element(By.CLASS_NAME, element_class_name)

    def get_dropdown_by_id(self, dropdown_id: str) -> Select:
        """
        Return a dropdown element by its ID

        Args:
            driver (Chrome): Chrome driver instance
            dropdown_id (str): ID of the dropdown to be found

        Returns:
            Select: Dropdown element found by ID
        """
        return Select(self.driver.find_element(By.ID, dropdown_id))

    def get_element_group_by_name(self, element_name: str) -> list[WebElement]:
        """
        Return a list of element by their name

        Args:
            driver (Chrome): Chrome driver instance
            element_name (str): name value of the elements to be found

        Returns:
            WebElement: Element found by ID
        """
        return self.driver.find_elements(By.NAME, element_name)

    def get_element_group_by_class_name(self, element_class_name: str) -> list[WebElement]:
        """
        Return an element by its ID

        Args:
            driver (Chrome): Chrome driver instance
            element_class_name (str): class name of the elements to be found
        """

        return self.driver.find_elements(By.CLASS_NAME, element_class_name)
    
    def navigate_to_login(self, credentials: dict):
        """
        Navigates to the login page
        """
        self.driver.get(self.base_url)
        self.get_element_by_id("login_button").click()
        self.get_element_by_id("login_button").click()
        self.get_element_by_name("username").send_keys(credentials["username"])
        self.get_element_by_name("password").send_keys(credentials["password"])
        self.get_element_by_id("login_submit_button").click()

    def navigate_to_dashboard(self):
        """
        Navigates to the dashboard page
        """
        self.driver.get(f"{self.base_url}")
        self.get_element_by_id("navbarDropdownMenuLink").click()
        self.get_element_by_id("dashboard_button").click()

    def logout(self):
        """
        Logs out of the system and returns to the login page.
        """
        self.get_element_by_id("navbarDropdownMenuLink").click()
        self.get_element_by_id("logout_button").click()

    def populate_and_submit_login(self, credentials: dict):
        """
        Logs in a user with their credentials. Must be on the login page.
        """
        self.get_element_by_id("login_button").click()
        self.get_element_by_name("username").send_keys(credentials["username"])
        self.get_element_by_name("password").send_keys(credentials["password"])
        self.get_element_by_id("login_submit_button").click()

    def populate_and_submit_appointment(self, appointment: dict):
        """
        Populates and submits the appointment form

        Args:
            appointment (dict): Dictionary containing the appointment details
        """
        self.get_element_by_name("date").send_keys(appointment["date"])
        self.get_element_by_name("time").send_keys(appointment["time"])
        self.get_element_by_name("reason").send_keys(appointment["reason"])
        self.get_element_by_id("appointment_submit_button").click()

    def register_patient(self, new_patient: dict):
        """
        Registers a patient

        Args:
            new_patient (dict): Dictionary containing the user details
        """
        self.driver.get(f"{self.base_url}")
        sleep(0.5)
        self.get_element_by_id("register_button").click()
        sleep(0.5)
        self.get_element_by_name("firstname").send_keys(new_patient["first_name"])
        self.get_element_by_name("lastname").send_keys(new_patient["last_name"])
        self.get_element_by_name("username").send_keys(new_patient["username"])
        try:
            self.get_element_by_name("address").send_keys(new_patient["address"])
        except:
            pass
        try:
            self.get_element_by_name("dob").send_keys(new_patient["date_of_birth"])
        except:
            pass
        try:
            self.get_element_by_name("email").send_keys(new_patient["email"])
        except:
            pass
        self.get_element_by_name("password1").send_keys(new_patient["password"])
        self.get_element_by_name("password2").send_keys(new_patient["password"])
        self.get_element_by_id("register_submit_button").click()
        sleep(1)

    def register_doctor_or_nurse(self, new_practitioner: dict):
        """
        Registers a patient

        Args:
            new_patient (dict): Dictionary containing the user details
        """
        self.driver.get(f"{self.base_url}/staff_register/")
        sleep(0.5)
        #! self.get_element_by_name("firstname").send_keys(new_practitioner["first_name"])
        #! self.get_element_by_name("lastname").send_keys(new_practitioner["last_name"])
        self.get_element_by_name("username").send_keys(new_practitioner["username"])
        self.get_dropdown_by_id("id_user_type").select_by_visible_text(new_practitioner["role"])
        try:
            self.get_element_by_name("address").send_keys(new_practitioner["address"])
        except:
            pass
        try:
            self.get_element_by_name("dob").send_keys(new_practitioner["date_of_birth"])
        except:
            pass
        try:
            self.get_element_by_name("email").send_keys(new_practitioner["email"])
        except:
            pass
        self.get_element_by_name("password1").send_keys(new_practitioner["password"])
        self.get_element_by_name("password2").send_keys(new_practitioner["password"])
        #! self.get_element_by_id("register_submit_button").click()
        sleep(1)