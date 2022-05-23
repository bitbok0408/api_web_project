from src.web.pages.LoginPage import LoginPage
from Data.generics import english
import time


def test_success_login_as_root():
    page = LoginPage()
    page.open_login_page()
    page.fill_login('root')
    page.fill_password('root')
    page.press_login_button()
    assert page.menu.is_loaded()
    assert page.header.user_fio.endswith('Initiate Root User')


def test_login_with_wrong_credentials():
    login_page = LoginPage()
    login_page.open_login_page()
    login_page.fill_login(english.generic.company.login())
    login_page.fill_password(english.generic.company.password())
    login_page.press_login_button()
    assert login_page.login_explain_text() == '@Login is incorrect'
