import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from pages.login_page import LoginPage
from pages.pim_page import PIMPage

@pytest.mark.usefixtures("setup")
class TestLogin:
    def test_login_and_add_three_employees(self):
        wait = WebDriverWait(self.driver, 20)

        # Login steps
        login_page = LoginPage(self.driver)
        login_page.enter_username("Admin")
        login_page.enter_password("admin123")
        login_page.click_login()

        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.oxd-form-loader")))
        assert "dashboard" in self.driver.current_url.lower()

        pim_page = PIMPage(self.driver)

        # Safe click on PIM menu with retry
        def safe_click_pim_menu():
            tries = 3
            for attempt in range(tries):
                try:
                    element = wait.until(EC.element_to_be_clickable(pim_page.PIM_MENU))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    element.click()
                    return
                except (TimeoutException, ElementClickInterceptedException) as e:
                    print(f"PIM menu click attempt {attempt + 1} failed: {e}")
                    time.sleep(2)
            raise Exception("Failed to click PIM menu after retries")

        # Use safe click on PIM menu
        safe_click_pim_menu()

        # Function to add an employee
        def add_employee(first_name, last_name, emp_id, username, password):
            safe_click_pim_menu()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.oxd-form-loader")))
            pim_page.click_add_button()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.oxd-form-loader")))
            pim_page.fill_employee_details(first_name, last_name, emp_id)
            pim_page.enable_toggle()
            pim_page.fill_login_details(username, password)
            pim_page.click_save()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.oxd-form-loader")))
            time.sleep(2)

        # Add 3 employees
        add_employee("Rohan", "Mishra", "1567", "ronnnn123", "Roh@n12345")
        add_employee("Rahul", "Sharma", "1568", "rahul123", "Rahul@12345")
        add_employee("Amit", "Kumar", "1569", "amit123", "Amit@12345")

        # Go back to employee list
        safe_click_pim_menu()
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.oxd-form-loader")))

        target_employee_ids = {"1567", "1568", "1569"}
        found_ids = set()

        # Scroll and find IDs on page
        def step_wise_scroll_and_find(driver, target_ids, scroll_step=200, pause=1):
            nonlocal found_ids
            max_scroll_attempts = 30
            scroll_attempt = 0

            while scroll_attempt < max_scroll_attempts:
                scroll_attempt += 1
                elements = driver.find_elements(By.CSS_SELECTOR, "div[data-v-6c07a142]")
                page_ids = [el.text.strip() for el in elements if el.text.strip()]

                print(f"Scroll attempt {scroll_attempt}: Visible IDs -> {page_ids}")

                for tid in target_ids:
                    if tid in page_ids and tid not in found_ids:
                        print(f"{tid} found")
                        found_ids.add(tid)

                if found_ids == target_ids:
                    break

                driver.execute_script(f"window.scrollBy(0, {scroll_step});")
                time.sleep(pause)

                current_scroll_pos = driver.execute_script("return window.pageYOffset + window.innerHeight;")
                total_height = driver.execute_script("return document.body.scrollHeight;")

                if current_scroll_pos >= total_height:
                    print("Reached bottom of page during scroll.")
                    break

        # Scroll on current page
        step_wise_scroll_and_find(self.driver, target_employee_ids)

        # Pagination function
        def click_page(page_num):
            next_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.oxd-pagination-page-item--page")
            for btn in next_buttons:
                if btn.text.strip() == str(page_num) and 'disabled' not in btn.get_attribute('class'):
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    btn.click()
                    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.oxd-form-loader")))
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(1)
                    return True
            return False

        current_page = 1
        max_pages = 10
        while found_ids != target_employee_ids and current_page < max_pages:
            current_page += 1
            print(f"Trying to go to page {current_page} for employee search")
            if not click_page(current_page):
                print(f"Page {current_page} not found or disabled, stopping pagination search.")
                break
            step_wise_scroll_and_find(self.driver, target_employee_ids)

        # Report missing IDs
        not_found = target_employee_ids - found_ids
        for nf in not_found:
            print(f"{nf} NOT found")

        # Delete employees one by one with correct input locator
        def delete_employee(emp_id):
            print(f"Deleting employee ID: {emp_id}")
            safe_click_pim_menu()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.oxd-form-loader")))
            emp_id_input = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@data-v-1f99f73c and contains(@class,'oxd-input') and not(@placeholder)]")
            ))
            emp_id_input.click()
            emp_id_input.clear()
            emp_id_input.send_keys(emp_id)
            search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Search']")))
            search_button.click()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.oxd-form-loader")))
            time.sleep(2)
            delete_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.oxd-icon.bi-trash")))
            delete_icon.click()
            time.sleep(1)
            confirm_delete_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes, Delete']")))
            confirm_delete_button.click()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.oxd-form-loader")))
            time.sleep(3)

        # Delete all three employees
        for eid in target_employee_ids:
            delete_employee(eid)

        print("All target employees deleted successfully!")
