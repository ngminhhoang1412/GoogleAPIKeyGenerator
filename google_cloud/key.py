from login_gmail_selenium.util.profile import ChromeProfile
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
import common.constants as Constant
from time import sleep


class GoogleApiKey:
    def __init__(self, output_file):
        self.file = output_file + '.txt'
        self.driver = None

    def create_project(self, project_name):
        driver = self.driver
        driver.set_window_size(900, 800)
        driver.get("https://cloud.google.com/resource-manager/reference/rest/v3/projects/create?apix_params=%7B%22resource%22%3A%7B%22projectId%22%3A%22" + project_name + "%22%7D%7D")
        sleep(Constant.SHORT_WAIT)
        driver.execute_script("window.scrollBy(0,1530)", "")
        sleep(Constant.SHORT_WAIT)
        window_before = driver.window_handles[0]
        driver.switch_to.frame(
            driver.find_element(By.CSS_SELECTOR, ".apis-explorer > iframe"))
        driver.find_element(By.ID, "execute").click()
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
            pass
        sleep(10)

    def create_key(self, project_name):
        driver = self.driver
        driver.get(
            "https://console.cloud.google.com/welcome?project=" + project_name)
        sleep(100)
        xpath = '//*[@id="cfctest-section-nav-item-metropolis_api_credentials"]'
        create = '_0rif_action-bar-create-button'
        WebDriverWait(driver, Constant.LOADING_TIMEOUT).until(EC.visibility_of_element_located(
            (By.ID, create)))
        driver.find_element(By.ID, create).click()
        sleep(10)

    def create_multi_projects(self):
        f = open("accounts.txt", "r")
        for email in f:
            email = email.split(':')
            try:
                profile = ChromeProfile(email[0], email[1], email[2])
                self.driver = profile.retrieve_driver()
                profile.start()
            except:
                continue
            for num in range(1, 11):
                name = email[0].split('@')[0]
                # self.create_project(project_name=name + 'test1' + str(num))
                self.create_key(project_name=name + 'test1' + str(num))

