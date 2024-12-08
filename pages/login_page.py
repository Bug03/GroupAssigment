import time
from selenium.webdriver.common.by import By

class LoginPage():

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_login_page(self):
        self.driver.get("http://127.0.0.1:8000")
        time.sleep(2)

        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        login_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(1)")
        login_btn.click()
        time.sleep(1)

    def fill_login_form(self, email, password):
        username_field = self.driver.find_element(By.CSS_SELECTOR, "#view-product > div > div > form > div:nth-child(3) > input").send_keys(email)
        password_field = self.driver.find_element(By.CSS_SELECTOR, "#view-product > div > div > form > div:nth-child(5) > input").send_keys(password)

        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "#loginAcc")
        submit_btn.click()
        time.sleep(1)

    def close_alert(self):
        sc_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
        sc_btn.click()
        time.sleep(2)
    
    def get_success_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "#swal2-title").text
    
    def get_warning_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "#view-product > div > div > form > div:nth-child(4) > span").text
    
    def get_warning_message_2(self):
        return self.driver.find_element(By.CSS_SELECTOR, "#view-product > div > div > form > div:nth-child(6) > span").text
    
    def logout(self):
        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        logout_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > form > li")
        logout_btn.click()
        time.sleep(1)

    def success_logout(self):
        return self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-top-start.swal2-backdrop-show > div").text