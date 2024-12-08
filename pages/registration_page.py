import time
from selenium.webdriver.common.by import By

class RegistrationPage():

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_registration_page(self):
        self.driver.get("http://127.0.0.1:8000")
        time.sleep(2)

        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        registration_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(2)")
        registration_btn.click()
        time.sleep(1)

    def fill_registration_form(self, email, phone, password, confirm_password, username):
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(1) > div.form-group > input").send_keys(email)
        phone_field = self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(2) > div.form-group > input").send_keys(phone)
        password_field = self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(3) > div.form-group > input").send_keys(password)
        confirm_password_field = self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(4) > div.form-group > input").send_keys(confirm_password)
        username_field = self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(5) > div.form-group > input").send_keys(username)

        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(6) > div > div > div > button")
        submit_btn.click()
        time.sleep(1)

    def close_registration_form(self):
        close_btn = self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > span")
        close_btn.click()
        time.sleep(2)

    def close_alert(self):
        sc_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
        sc_btn.click()
        time.sleep(2)
    
    def get_success_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "#swal2-title").text
    
    def get_warning_email_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(1) > div:nth-child(2) > span").text
    
    def get_warning_phone_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(2) > div:nth-child(2) > span").text
    
    def get_warning_password_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(3) > div:nth-child(2) > span").text
    
    def get_warning_username_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "#registerForm > div > div > div > div > div > div > form > div > div:nth-child(5) > div:nth-child(2) > span").text
    
    