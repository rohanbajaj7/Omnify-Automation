from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Import Keys for keyboard actions

class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    PIM_MENU = (By.XPATH, "//span[@class='oxd-text oxd-text--span oxd-main-menu-item--name' and text()='PIM']")
    ADD_BUTTON = (By.XPATH, "//button[contains(., 'Add')]")
    FIRST_NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")
    EMPLOYEE_ID = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div/input")
    TOGGLE_SWITCH = (By.XPATH, "//span[contains(@class, 'oxd-switch-input')]")
    USERNAME = (By.XPATH, "//label[text()='Username']/../following-sibling::div/input")
    PASSWORD = (By.XPATH, "//label[text()='Password']/../following-sibling::div/input")
    CONFIRM_PASSWORD = (By.XPATH, "//label[text()='Confirm Password']/../following-sibling::div/input")
    SAVE_BUTTON = (By.XPATH, "//button[contains(., 'Save')]")

    # Actions
    def click_pim_menu(self):
        self.wait.until(EC.element_to_be_clickable(self.PIM_MENU)).click()

    def click_add_button(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON)).click()

    def fill_employee_details(self, first_name, last_name, emp_id):
        self.wait.until(EC.presence_of_element_located(self.FIRST_NAME)).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        
        emp_id_field = self.driver.find_element(*self.EMPLOYEE_ID)
        emp_id_field.click()
        emp_id_field.send_keys(Keys.CONTROL + "a")
        emp_id_field.send_keys(Keys.BACKSPACE)       
        emp_id_field.send_keys(emp_id)                

    def enable_toggle(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.TOGGLE_SWITCH))
        ActionChains(self.driver).move_to_element(toggle).click().perform()

    def fill_login_details(self, username, password):
        self.wait.until(EC.presence_of_element_located(self.USERNAME)).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.CONFIRM_PASSWORD).send_keys(password)

    def click_save(self):
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()
