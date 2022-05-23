from .LoginPage import LoginPage, BasePage
from selene.api import ss, s, be, query, have
from selene.support.shared import browser
import time




class Filter(BasePage):
    _MAIN_FILTER_PARAMS = '.search .ant-col-8'
    _FILTER_CONTAINER = '.toFilter'
    _ADD_FILTER_BUTTON = '.toggleFullFilter'
    _FILTER_PARAM = '.ant-select-dropdown-menu-item'
    _FILTER_PARAMS_INPUT = '.choseField .ant-input'
    _FILTER_PARAMS_LISTBOX = '.ant-select-dropdown-menu-vertical'
    _FILTER_PARAM_SELECTED_INPUT = '.n-filter .ant-select-enabled'
    _FILTER_PARAM_GROUP_LIST_DROPDOWN = '.ant-select-tree-treenode-switcher-open'
    _FILTER_PARAM_GROUP = '.ant-select-tree-title'
    _FILTER_DATE_FROM_PARAM = '.ant-input[placeholder="Дата з"]'
    _FILTER_DATE_TO_PARAM = '.ant-input[placeholder="Дата по"]'
    _FILTER_CALENDAR = '.ant-calendar-time'
    _FILTER_DATE_FROM_INPUT = '.ant-calendar-input'
    _FILTER_DATE_FROM_CLEAR_BUTTON = '.ant-input[placeholder="Дата з"] + .ant-calendar-picker-clear'
    _FILTER_DATE_FROM_CALENDAR_ICON = '.ant-calendar-picker'

    def move_to_calendar_icon(self):
        self._move_to_element(browser.driver.find_element_by_css_selector(self._FILTER_DATE_FROM_CALENDAR_ICON))

    def select_root_group(self):
        s(self._FILTER_PARAM_SELECTED_INPUT).click()
        s(self._FILTER_PARAM_GROUP_LIST_DROPDOWN).should(be.visible)
        self._search_element_by_text(self._FILTER_PARAM_GROUP, 'ROOT').click()

    def click_on_add_filter_button(self):
        return s(self._ADD_FILTER_BUTTON).click()

    def add_filter_button_is_clickable(self):
        return s(self._ADD_FILTER_BUTTON).matching(be.clickable)

    def search_type(self):
        return self._search_element_by_text(self._MAIN_FILTER_PARAMS, self._search_type)

    def filter_container_is_visible(self):
        s(self._FILTER_CONTAINER).should(be.visible)

    def operation(self):
        return self._search_element_by_text(self._MAIN_FILTER_PARAMS, self._operation)

    def search_input_field(self):
        return self._search_element_by_text(self._MAIN_FILTER_PARAMS, self._search_input_field)

    def click_on_filter_param_input(self):
        s(self._FILTER_PARAMS_INPUT).click()
        s(self._FILTER_PARAMS_LISTBOX).should(be.visible)

    def filter_listbox_is_opened(self):
        return s(self._FILTER_PARAMS_LISTBOX).matching(be.visible)

    def choose_groups_param(self):
        self._search_element_by_text(self._FILTER_PARAM, self._groups).click()

    def click_on_date_from_input(self):
        s(self._FILTER_DATE_FROM_PARAM).click()

    def type_date_from(self, date):
        s(self._FILTER_DATE_FROM_INPUT).type(date)

    def calendar_is_present(self):
        return s(self._FILTER_CALENDAR).should(be.visible)

    def type_date_to(self, date):
        s(self._FILTER_DATE_TO_PARAM).clear().type(date)

    def click_on_clear_date_from_button(self):
        return s(self._FILTER_DATE_FROM_CLEAR_BUTTON).click()

    @property
    def _search_type(self):
        return 'Тип пошуку'

    @property
    def _operation(self):
        return 'Операція'

    @property
    def _search_input_field(self):
        return 'Пошук'

    @property
    def _groups(self):
        return "Групи"

    @property
    def _holds_duration(self):
        return "Загальна тривалість утримання (в секундах):"

    @property
    def _inner_outer_call(self):
        return 'Зовнішній/внутрішній дзвінок'

    @property
    def _holds_count(self):
        return 'Кількість утримань:'

    @property
    def _parts_count(self):
        return 'Кількість частин у дзвінку:'

    @property
    def _has_comment(self):
        return 'Містить коментар'

    @property
    def _has_tags(self):
        return 'Містить теги'

    @property
    def _call_direction(self):
        return 'Напрямок дзвінка'

    @property
    def _search_chat_text(self):
        return 'Пошук в тексті (лише чати)'

    @property
    def _keywords_search(self):
        return 'Пошук за ключовими словами'

    @property
    def _search_by_recognition_text(self):
        return 'Пошук фрагментів розпізнаного тексту (лише аудіозаписи)'

    @property
    def _call_status(self):
        return 'Статус запису'

    @property
    def _call_type(self):
        return 'Тип запису'


class TagLibrary:
    _NEW_TAG_SECTION = s('.calls-item-edited')
    _ADD_TAG_BUTTON = s('.add-btn')
    _TAG_NAME_INPUT = s('.ant-input[name="name"]')
    _TAG_DESCRIPTION_INPUT = s('.ant-input[name="description"]')
    _TAG_BLOCK_CONTAINER = s('.containerTagBlock')
    _TAG_SAVE_EDIT_DELETE = ss('.material-icons m-icons')
    _TAG_EDITED_ROW = s('.rec-calls-item-edited')
    _TAG_ROWS_LIST = ss('.tags-body .ant-spin-container .rec-calls-item')
    _TAG_ACTIONS_BUTTONS = '.tags-body .m-icons'

    def new_tag_section_is_visible(self):
        return self._NEW_TAG_SECTION.matching(be.visible)

    def click_add_tag_button(self):
        return self._ADD_TAG_BUTTON.click()

    def type_tag_name(self, text):
        return self._TAG_NAME_INPUT.type(text)

    def type_tag_description(self, text):
        return self._TAG_DESCRIPTION_INPUT.type(text)

    def tag_container(self):
        return self._TAG_BLOCK_CONTAINER.should(be.present)

    def tag_edited_row_is_present(self):
        return self._TAG_EDITED_ROW.matching(be.visible)

    def tag_edited_row_is_closed(self):
        return self._TAG_EDITED_ROW.should(be.not_.present)

    def click_edit_tag_button_in_row_with_number(self, row_number=1):
        return self._TAG_ROWS_LIST[row_number-1].ss(self._TAG_ACTIONS_BUTTONS)\
            .element_by(have.text(self._edit_button)).click()

    def click_delete_tag_button_in_row_with_number(self, row_number=1):
        return self._TAG_ROWS_LIST[row_number-1].ss(self._TAG_ACTIONS_BUTTONS)\
            .element_by(have.text(self._delete_button)).click()

    def click_save_tag_button(self):
        return ss(self._TAG_ACTIONS_BUTTONS).element_by(have.text(self._save_button)).click()

    def get_list_of_tags(self):
        return [el.get(query.text).split('\n') for el in self._TAG_ROWS_LIST]

    def last_element_has_text(self, text):
        return self._TAG_ROWS_LIST[-1].should(have.text(text))

    @property
    def _save_button(self):
        return 'check'

    @property
    def _edit_button(self):
        return 'create'

    @property
    def _delete_button(self):
        return 'delete'


class RecordingPage(LoginPage, TagLibrary, Filter):
    _MINIMIZE_FILTER_BLOCK = s('.action-container.small_mode .toFilter')
    _MINIMIZE_FILTER_PARAMS_LIST = ss('.ant-tag')
    _FILTER_BUTTON = s('[name="REC_FILTER"]')
    _TAG_LIBRARY_BUTTON = s('[name=REC_TAG_LIBRARY]')
    _REFRESH_BUTTON = s('.ant-btn[type="button"]')
    _EXPORT_EXCEL_BUTTON = s('.ant-btn-primary')

    def __init__(self):
        super().__init__()
        if not self.menu.is_present():
            self.login_with_root_credentials()
            self.menu.is_loaded()
        self.menu.recording.go()
        self._MINIMIZE_FILTER_BLOCK.should(be.visible)

    def minimize_filter_params_list(self):
        return [search_param.get(query.text) for search_param in self._MINIMIZE_FILTER_PARAMS_LIST]

    def click_on_filter_button(self):
        self._FILTER_BUTTON.click()
        self.filter_container_is_visible()

    def click_on_tag_library_button(self):
        self._TAG_LIBRARY_BUTTON.click()
        self.tag_container()

    def click_on_refresh_button(self):
        return self._REFRESH_BUTTON.click()

    def click_on_export_excel_button(self):
        return self._EXPORT_EXCEL_BUTTON.click()




