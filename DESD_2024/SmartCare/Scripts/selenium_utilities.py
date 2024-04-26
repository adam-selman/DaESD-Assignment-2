from time import sleep

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class SeleniumTestSuite:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.driver = self.get_driver()
        self.admin = {"username": "a-a5-wearne", "password": "29936827"}
        self.patient = {"username": "p-d5-victorsajowa", "password": "19043780"}
        self.doctor = {"username": "d-a5-selman", "password": "20049296"}
        self.nurse = {"username": "n-t5-chapman", "password": "19027149"}
        

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
    
    def navigate_to_login(self):
        """
        Navigates to the login page
        """
        self.driver.get({self.base_url})
        self.get_element_by_id("login_button").click()

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
        self.get_element_by_id("logout_button").click()

    def login_as_admin(self):
        """
        Logs in as an admin. Must be used once navigated to the login page
        """
        self.get_element_by_id("login_button").click()
        self.get_element_by_name("username").send_keys(self.admin["username"])
        self.get_element_by_name("password").send_keys(self.admin["password"])
        self.get_element_by_id("login_submit_button").click()

    
    def login_as_patient(self):
        """
        Logs in as a patient. Must be used once navigated to the login page
        """
        self.get_element_by_id("login_button").click()
        self.get_element_by_name("username").send_keys("patient")
        self.get_element_by_name("password").send_keys("patient")
        self.get_element_by_id("login_submit_button").click()

    def login_as_doctor(self):
        """
        Logs in as a doctor. Must be used once navigated to the login page
        """
        self.get_element_by_id("login_button").click()
        self.get_element_by_name("username").send_keys("doctor")
        self.get_element_by_name("password").send_keys("doctor")
        self.get_element_by_id("login_submit_button").click()
    
    def login_as_nurse(self):
        """
        Logs in as a nurse. Must be used once navigated to the login page
        """
        self.get_element_by_id("login_button").click()
        self.get_element_by_name("username").send_keys("nurse")
        self.get_element_by_name("password").send_keys("nurse")
        self.get_element_by_id("login_submit_button").click()
    
    def register_user(self, new_user: dict):
        """
        Registers a user

        Args:
            new_user (dict): Dictionary containing the user details
        """
        self.driver.get(f"{self.base_url}")
        sleep(0.5)
        self.get_element_by_id("register_button").click()
        sleep(0.5)
        self.get_element_by_name("firstname").send_keys(new_user["first_name"])
        self.get_element_by_name("lastname").send_keys(new_user["last_name"])
        self.get_element_by_name("username").send_keys(new_user["username"])
        try:
            self.get_element_by_name("address").send_keys(new_user["address"])
        except:
            pass
        try:
            self.get_element_by_name("dob").send_keys(new_user["date_of_birth"])
        except:
            pass
        try:
            self.get_element_by_name("email").send_keys(new_user["email"])
        except:
            pass
        self.get_element_by_name("password1").send_keys(new_user["password"])
        self.get_element_by_name("password2").send_keys(new_user["password"])
        self.get_element_by_id("register_submit_button").click()
        sleep(1)
