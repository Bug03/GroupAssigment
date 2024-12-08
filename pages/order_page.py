import time
from selenium.webdriver.common.by import By

class OrderPage():

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_order_page(self):
        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        order_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(2)")
        order_btn.click()
        time.sleep(3)

    def search_phone_order(self, order_id):
        phone_field = self.driver.find_element(By.CSS_SELECTOR,"body > section > div > div > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        phone_field.send_keys(order_id)
        time.sleep(1)

    def navigate_to_filter(self):
        filter_btn = self.driver.find_element(By.CSS_SELECTOR,"body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(1) > td:nth-child(5) > div > div > select")
        filter_btn.click()
        time.sleep(1)

    def 