import time
from selenium.webdriver.common.by import By

class CategoryManagementPage():

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_category_page(self):
        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        admin_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(2)")
        admin_btn.click()
        time.sleep(3)

        category_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-sidebar.sidebar-style-2 > ul > li:nth-child(6) > a")
        category_btn.click()
        time.sleep(1)

        menu_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-sidebar.sidebar-style-2 > ul > li:nth-child(6) > ul > li:nth-child(1) > a > span")
        menu_btn.click()
        time.sleep(1)

    def search_category(self, category_name):
        search_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        search_field.send_keys(category_name)
        time.sleep(1)

        search_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > span")
        search_btn.click()

    def navigate_to_add_category_page(self):
        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        admin_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(2)")
        admin_btn.click()
        time.sleep(3)

        category_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-sidebar.sidebar-style-2 > ul > li:nth-child(6) > a")
        category_btn.click()
        time.sleep(1)

        add_category_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-sidebar.sidebar-style-2 > ul > li:nth-child(6) > ul > li:nth-child(2) > a > span")
        add_category_btn.click()
        time.sleep(1)

    def fill_form_add_category(self, category_name):
        icon_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > div > button")
        icon_btn.click()
        time.sleep(3)

        icon_field = self.driver.find_element(By.CSS_SELECTOR,"button[title='fas fa-ad']")
        icon_field.click()
        time.sleep(1)

        name_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_field.send_keys(category_name)
        time.sleep(1)

        status_field = self.driver.find_element(By.CSS_SELECTOR,"#inputState")
        status_field.click()

        online_status = self.driver.find_element(By.CSS_SELECTOR,"#inputState > option:nth-child(1)")
        online_status.click()

        submit_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        submit_btn.click()
        time.sleep(1)

    def get_success_message(self):
        return self.driver.find_element(By.CSS_SELECTOR,"#swal2-title").text
    
    def delete_category(self):
        delete_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(4) > td:nth-child(6) > span > div > a.btn.btn-danger.ml-2.delete-item")
        delete_btn.click()
        time.sleep(1)

        confirm_delete_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled.swal2-default-outline")
        confirm_delete_btn.click()
        time.sleep(1)

    def navigate_to_update_category(self):
        update_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(4) > td:nth-child(6) > span > div > a.btn.btn-primary.ml-2.edit-item")
        update_btn.click()
        time.sleep(1)

    def fill_form_update_category(self, category_name):
        icon_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > div > button")
        icon_btn.click()
        time.sleep(3)

        icon_field = self.driver.find_element(By.CSS_SELECTOR,"button[title='fas fa-ad']")
        icon_field.click()
        time.sleep(1)

        name_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        name_field.send_keys(category_name)
        time.sleep(1)

        status_field = self.driver.find_element(By.CSS_SELECTOR,"#inputState")
        status_field.click()

        online_status = self.driver.find_element(By.CSS_SELECTOR,"#inputState > option:nth-child(1)")
        online_status.click()

        submit_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        submit_btn.click()
        time.sleep(1)


