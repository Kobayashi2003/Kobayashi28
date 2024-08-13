from locators import MainPageLocators, BrowsePageLocators, VisualNovelPageLocators, BasePageLocators

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def back(self):
        self.driver.back()

    def go_home(self):
        self.driver.find_element(*BasePageLocators.HOME).click()

    def search_and_go(self, search_text):
        search_box = self.driver.find_element(*BasePageLocators.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(search_text)
        search_box.send_keys(Keys.RETURN)

class MainPage(BasePage):
    """Home page action methods come here. I.e. vndb.org"""

    def is_title_matches(self):
        """Verifies that the hardcoded text "vndb" appears in page title"""
        return "vndb" in self.driver.title

class BrowsePage(BasePage):

    def get_visual_novels_list(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(*BrowsePageLocators.NOACTION))

        if self.driver.find_elements(*VisualNovelPageLocators.VNIMG):
            return self.driver.find_elements(*BrowsePageLocators.NOACTION)

        return self.driver.find_elements(*BrowsePageLocators.VNLIST)
        
class VisualNovelPage(BasePage):

    def get_visual_novel_img_url(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(*VisualNovelPageLocators.VNIMG))
        return self.driver.find_element(*VisualNovelPageLocators.VNIMG).get_attribute('src')
