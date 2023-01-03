from login_gmail_selenium.util.profile import ChromeProfile
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
import common.constants as Constant
from time import sleep
import google_cloud.helper as Helper


class GoogleApiKey:
    def __init__(self):
        self.driver = None
        self.error = None

    def create_project(self, project_name):
        driver = self.driver
        driver.set_window_size(900, 800)
        driver.get("https://cloud.google.com/resource-manager/reference/rest/v3/projects/create?apix_params=%7B%22resource%22%3A%7B%22projectId%22%3A%22" + project_name + "%22%7D%7D")
        sleep(Constant.SHORT_WAIT)
        driver.execute_script("window.scrollBy(0,1530)", "")
        sleep(Constant.SHORT_WAIT)
        window_before = driver.window_handles[0]
        try:
            driver.switch_to.frame(
                driver.find_element(By.CSS_SELECTOR, ".apis-explorer > iframe"))
            driver.find_element(By.ID, "execute").click()
        except:
            self.error = "Cantswitchtoframe"
        try:
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            choose_account = '.JDAKTe > div'
            driver.find_element(By.CSS_SELECTOR, choose_account).click()
            enable = '#submit_approve_access div button'
            WebDriverWait(driver, Constant.LOADING_TIMEOUT).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, enable)))
            driver.find_element(By.CSS_SELECTOR, enable).click()
            driver.switch_to.window(window_before)
        except:
            self.error = "Cantswitchtochooseaccount"
        sleep(Constant.STAND_BY_TIMEOUT)

    def create_key(self, project_name):
        driver = self.driver
        try:
            driver.get(
                "https://console.cloud.google.com/apis/credentials?project=" + project_name)
            create = '_0rif_action-bar-create-button'
            WebDriverWait(driver, Constant.LOADING_TIMEOUT).until(EC.visibility_of_element_located(
                (By.ID, create)))
            driver.find_element(By.ID, create).click()
            driver.execute_script("document.getElementsByClassName('cfc-menu-item-has-note')[0].click()")
            sleep(Constant.STAND_BY_TIMEOUT)
            api_key = driver.execute_script("return document.getElementById('_0rif_mat-input-0').value")
            return str(api_key)
        except:
            self.error = "project_invalid"

    def create_multi_projects(self):
        f = open("accounts.txt", "r")
        for email in f:
            email = email.split(':')
            if Helper.check_number(email[0].split('@')[0]):
                continue
            try:
                profile = ChromeProfile(email[0], email[1], email[2])
                self.driver = profile.retrieve_driver()
                profile.start()
            except:
                self.error = "CantsignintoGoogleAccount"
                Helper.write_error(error=self.error, email=email[0])
                self.error = None
                self.driver.quit()
                continue
            for num in range(1, 11):
                name = email[0].split('@')[0]
                name = Helper.change_name(name)
                self.create_project(project_name=name + str(num))
                if self.error is not None:
                    Helper.write_error(error=self.error, email=email[0], name_project=(name + str(num)))
                    self.error = None
            Helper.delete_temp()

    def get_key(self):
        f = open("accounts.txt", "r")
        for email in f:
            email = email.split(':')
            if Helper.check_number(email[0].split('@')[0]):
                continue
            try:
                profile = ChromeProfile(email[0], email[1], email[2])
                self.driver = profile.retrieve_driver()
                profile.start()
            except:
                self.error = "CantsignintoGoogleAccount"
                continue
            try:
                self.google_terms()
            except:
                pass
            for num in range(1, 11):
                name = email[0].split('@')[0]
                name = Helper.change_name(name)
                key = self.create_key(name + str(num))
                if self.error is None:
                    Helper.write_key(key=key, email=email[0])
                else:
                    Helper.write_error(error=self.error, email=email[0], name_project=(name + str(num)))
                    self.error = None
            Helper.delete_temp()

    def google_terms(self):
        driver = self.driver
        driver.get('https://console.cloud.google.com')
        sleep(Constant.STAND_BY_TIMEOUT)
        driver.execute_script("document.getElementById('mat-mdc-checkbox-2-input').click()")
        driver.execute_script("document.getElementsByClassName('mat-primary')[6].click()")
