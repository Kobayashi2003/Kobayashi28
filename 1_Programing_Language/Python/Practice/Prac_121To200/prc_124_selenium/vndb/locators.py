from selenium.webdriver.common.by import By

class BasePageLocators(object):
    HOME = (By.CSS_SELECTOR, 'h1 a')
    SEARCH_BOX = (By.ID, 'sq')

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

class BrowsePageLocators(object):
    VNLIST = (By.CSS_SELECTOR, 'tbody .tc_title a') 
    NOACTION = (By.TAG_NAME, 'h2')

class VisualNovelPageLocators(object):
    VNIMG = (By.CSS_SELECTOR, '.vnimg img')