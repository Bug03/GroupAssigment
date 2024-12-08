import time
from selenium.webdriver.common.by import By

class InformationPage():

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_information_page(self):
        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        info_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(1)")
        info_btn.click()
        time.sleep(1)

    def fill_info_form(self, username, email, phone):
        username_field = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(1) > div > form > div.card-body > div > div:nth-child(1) > input").send_keys(username)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(1) > div > form > div.card-body > div > div:nth-child(3) > input").send_keys(email)
        phone_field = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(1) > div > form > div.card-body > div > div:nth-child(5) > input").send_keys(phone)

        submit_info_btn = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(1) > div > form > div.card-footer.text-right > button")
        submit_info_btn.click()
        time.sleep(1)

    def fill_password_form(self, password, new_password, confirm_new_password):
        old_password_field = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(2) > div > form > div.card-body > div > div:nth-child(1) > input").send_keys(password)
        new_password_field = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(2) > div > form > div.card-body > div > div:nth-child(3) > input").send_keys(new_password)
        confirm_new_password_field = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(2) > div > form > div.card-body > div > div:nth-child(5) > input").send_keys(confirm_new_password)

        submit_password_btn = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(2) > div > form > div.card-footer.text-right > button")
        submit_password_btn.click()
        time.sleep(1)

    def get_success_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "#swal2-title").text

    def get_warning_phone_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(1) > div > form > div.card-body > div > div:nth-child(6) > span").text
    
    def get_warning_old_password_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(2) > div > form > div.card-body > div > div:nth-child(2) > span").text
    
    def get_warning_password_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div:nth-child(2) > div > form > div.card-body > div > div:nth-child(4) > span").text