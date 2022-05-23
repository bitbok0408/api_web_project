from config.project_config import cfg
from ..widgets import ProductsMenu, Header
from selene.api import ss, have
from selenium.webdriver import ActionChains
from selene.support.shared import browser


class BasePage:
    def __init__(self):
        # config.timeout = 10
        # config.browser_name = 'chrome'
        # config.window_height = 1000
        # config.window_width = 1920
        self.menu = ProductsMenu()
        self.header = Header()
        # config.browser_name = cfg.browser

    @property
    def credentials(self):
        return cfg.credentials

    @staticmethod
    def _search_element_by_text(locator, text):
        return ss(locator).element_by(have.text(text))

    @staticmethod
    def _move_to_element(element):
        action = ActionChains(browser.driver)
        return action.move_to_element(element).perform()
