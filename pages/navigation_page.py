import time
from selenium.webdriver.common.by import By

class NavigationPage():
    
    def __init__(self, driver):
        self.driver = driver
    
    def navigate_to_category(self):
        self.driver.get("http://127.0.0.1:8000")
        time.sleep(2)

        category_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(2) > a")
        category_btn.click()
        time.sleep(1)

    def navigate_to_coffee(self):
        coffee_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(2) > div > ul > li:nth-child(1)")
        coffee_btn.click()
        time.sleep(1)

    def navigate_to_gift(self):
        gift_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(2) > div > ul > li:nth-child(2)")
        gift_btn.click()
        time.sleep(1)

    def navigate_to_prescription(self):
        prescription_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(2) > div > ul > li:nth-child(3)")
        prescription_btn.click()
        time.sleep(1)

    def navigate_to_all_products(self):
        all_products_btn = self.driver.find_element(By.CSS_SELECTOR, "body > footer > div.footer-middle > div > div > div.col-lg-2.col-md-2 > div > ul > li > a")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", all_products_btn)
        time.sleep(3)
        all_products_btn.click()
        time.sleep(1)

        
            
        
        