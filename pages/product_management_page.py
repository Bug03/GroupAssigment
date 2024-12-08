import time
from selenium.webdriver.common.by import By

class ProductManagementPage():

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_product_page(self):
        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        admin_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(2)")
        admin_btn.click()
        time.sleep(3)

        product_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-sidebar.sidebar-style-2 > ul > li:nth-child(7) > a")
        product_btn.click()
        time.sleep(1)

        menu_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-sidebar.sidebar-style-2 > ul > li:nth-child(7) > ul > li:nth-child(1) > a > span")
        menu_btn.click()
        time.sleep(1)

    def search_product(self, product_name):
        search_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        search_field.send_keys(product_name)
        time.sleep(1)

        search_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > span")
        search_btn.click()

    def navigate_to_add_product_page(self):
        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        admin_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(2)")
        admin_btn.click()
        time.sleep(3)

        product_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-sidebar.sidebar-style-2 > ul > li:nth-child(7) > a")
        product_btn.click()
        time.sleep(1)

        add_product_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-sidebar.sidebar-style-2 > ul > li:nth-child(7) > ul > li:nth-child(2) > a > span")
        add_product_btn.click()
        time.sleep(1)

    def fill_form_add_product(self, product_name, price, vol, description, content):
        name_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_field.send_keys(product_name)

        category_field = self.driver.find_element(By.CSS_SELECTOR,"#inputCategory")
        category_field.click()

        category_option = self.driver.find_element(By.CSS_SELECTOR,"#inputCategory > option:nth-child(1)")
        category_option.click()

        price_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(5) > input")
        price_field.send_keys(price)

        vol_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(6) > input")
        vol_field.send_keys(vol)

        description_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(7) > textarea")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", description_field )
        description_field.send_keys(description)

        content_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(8) > div > div.note-editing-area > div.note-editable.card-block")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", content_field)
        content_field.send_keys(content)

        status_field = self.driver.find_element(By.CSS_SELECTOR,"#inputState")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", status_field )
        status_field.click()

        online_status = self.driver.find_element(By.CSS_SELECTOR,"#inputState > option:nth-child(1)")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", online_status )
        online_status.click()

        submit_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        submit_btn.click()
        time.sleep(1)

    def get_success_message(self):
        return self.driver.find_element(By.CSS_SELECTOR,"#swal2-title").text
    
    def delete_product(self):
        delete_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(4) > td:nth-child(6) > span > div > a.btn.btn-danger.ml-2.delete-item")
        delete_btn.click()
        time.sleep(1)

        confirm_delete_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled.swal2-default-outline")
        confirm_delete_btn.click()
        time.sleep(1)

    def navigate_to_update_product(self):
        update_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(4) > td:nth-child(6) > span > div > a.btn.btn-primary.ml-2.edit-item")
        update_btn.click()
        time.sleep(1)

    def fill_form_update_product(self, product_name, price, vol, description, content):
        name_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_field.send_keys(product_name)

        category_field = self.driver.find_element(By.CSS_SELECTOR,"#inputCategory")
        category_field.click()

        category_option = self.driver.find_element(By.CSS_SELECTOR,"#inputCategory > option:nth-child(1)")
        category_option.click()

        price_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(5) > input")
        price_field.send_keys(price)

        vol_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(6) > input")
        vol_field.send_keys(vol)

        description_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(7) > textarea")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", description_field )
        description_field.send_keys(description)

        content_field = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(8) > div > div.note-editing-area > div.note-editable.card-block")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", content_field)
        content_field.send_keys(content)

        status_field = self.driver.find_element(By.CSS_SELECTOR,"#inputState")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", status_field )
        status_field.click()

        online_status = self.driver.find_element(By.CSS_SELECTOR,"#inputState > option:nth-child(1)")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", online_status )
        online_status.click()

        submit_btn = self.driver.find_element(By.CSS_SELECTOR,"#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        submit_btn.click()
        time.sleep(1)


