from selene.api import s, browser, be, query

from .BasePage import BasePage


class LoginPage(BasePage):
    _LOGIN_BUTTON = s(".ant-btn-primary")
    _LOGIN_INPUT = s("#principal")
    _PASSWORD_INPUT = s("#credential")
    _LOGIN_EXPLAIN = s('.ant-form-explain')

    def __init__(self):
        super().__init__()

    def press_login_button(self):
        self._LOGIN_BUTTON.click()

    def fill_login(self, text):
        self._LOGIN_INPUT.type(text)

    def fill_password(self, text):
        self._PASSWORD_INPUT.type(text)

    def open_login_page(self):
        browser.open("http://qa.company.lab/#/login")
        self._LOGIN_BUTTON.should(be.clickable)

    def login_with_root_credentials(self):
        self.open_login_page()
        self.fill_login('root')
        self.fill_password('root')
        self.press_login_button()

    def login_explain_text(self):
        self._LOGIN_EXPLAIN.should(be.visible)
        return self._LOGIN_EXPLAIN.get(query.text)


log = LoginPage()
