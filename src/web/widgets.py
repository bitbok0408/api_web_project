from selene.api import s, ss, be, have, query


class ProductsMenu:
    _PRODUCTS_BUTTONS_LIST = ss("nav.leftMenu>ul>li")
    _PRODUCTS_MENU = s("nav.leftMenu")

    def __init__(self):
        self.product = None

    def is_present(self):
        return self._PRODUCTS_MENU.matching(be.present)

    def is_loaded(self):
        return self._PRODUCTS_BUTTONS_LIST[0].should(be.clickable)

    def go(self):
        if not self.product:
            raise AttributeError
        self._PRODUCTS_BUTTONS_LIST.element_by(have.text(self.product)).click()

    @property
    def agent_scripting(self):
        self.product = "Agent scripting"
        return self

    @property
    def recording(self):
        self.product = "Recording"
        return self

    @property
    def quality_management(self):
        self.product = "Quality Management"
        return self

    @property
    def contact_manager(self):
        self.product = "Contact Manager"
        return self

    @property
    def smart_callback(self):
        self.product = "Smart callback"
        return self

    @property
    def messenger_connector(self):
        self.product = "Messenger connector"
        return self

    @property
    def video_conference(self):
        self.product = "Video Conference"
        return self


class Header:

    def __init__(self):
        self.product = None
        self.lang = None

    _SETTINGS_BUTTON = s(".settingClickIcon")
    _MORE_BUTTON = s(".setting")
    _USER_INFO = s(".info")
    _DROPDOWN_MENU_BUTTONS_LIST = ss('.ant-row-flex-middle')
    _PRODUCT_NAME = s('.main_title')

    def go_to_settings(self):
        self._SETTINGS_BUTTON.click()

    def click_on_kebab_button(self):
        self._MORE_BUTTON.click()
        return self

    def click_on_user_info_menu(self):
        self._USER_INFO.click()
        return self

    def go(self):
        if not self.product:
            raise AttributeError
        self._DROPDOWN_MENU_BUTTONS_LIST.element_by(have.text(self.product)).click()

    @property
    def product_name(self):
        return self._PRODUCT_NAME.get(query.text)

    @property
    def user_fio(self):
        return self._USER_INFO.get(query.text)

    @property
    def rus(self):
        self.product = "Профіль"
        return self

    @property
    def profile(self):
        self.product = "Профіль"
        return self

    @property
    def exit(self):
        self.product = "Вихід"
        return self

    @property
    def users(self):
        self.product = "Користувачі"
        return self

    @property
    def licenses(self):
        self.product = "Ліцензії"
        return self

    @property
    def logs(self):
        self.product = "Журнал подій"
        return self

    @property
    def panel_administration(self):
        self.product = "Panel Administration"
        return self

    @property
    def products_versions(self):
        self.product = "Версії продуктів"
        return self

    @property
    def integrations(self):
        self.product = "Інтеграції"
        return self

