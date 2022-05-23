from src.web.pages.RecordingPage import RecordingPage
from Data.generics import english, ukrainian
from helpers.utils import get_today_midnight_datetime, get_today_start_datetime, convert_timestamp
import time, pytest
from selene.api import s, by, be, have


def test_time_first_enter_on_recording_page():
    page = RecordingPage()
    assert page.header.product_name == 'Recording'
    assert sorted(page.minimize_filter_params_list()) == sorted(
        [get_today_start_datetime(), get_today_midnight_datetime()])


def test_first_time_enter_to_filter():
    p = RecordingPage()
    p.click_on_filter_button()
    assert p.search_type().matching(have.text('Телефон'))
    assert p.operation().matching(have.text('починається з'))
    assert p.add_filter_button_is_clickable()


def test_add_tag_to_tag_library():
    p = RecordingPage()
    p.click_on_tag_library_button()
    assert p.tag_container().matching(be.visible)
    p.click_add_tag_button()
    tag_name, tag_description = ukrainian.string.word(), ukrainian.string.word()
    p.type_tag_name(tag_name)
    p.type_tag_description(tag_description)
    p.click_save_tag_button()
    assert p.tag_edited_row_is_closed()
    assert p.last_element_has_text(tag_name)


def test_add_filter():
    p = RecordingPage()
    p.click_on_filter_button()
    p.click_on_add_filter_button()
    p.click_on_filter_param_input()
    assert p.filter_listbox_is_opened()
    p.choose_groups_param()
    assert not p.add_filter_button_is_clickable()
    p.select_root_group()
    assert p.add_filter_button_is_clickable()


def test_search_call_by_search_params():
    # call_date = convert_timestamp(call_with_params['dateStart'])
    p = RecordingPage()
    p.click_on_filter_button()
    p.move_to_calendar_icon()
    p.click_on_clear_date_from_button()
    # p.click_on_date_from_input()
    # assert p.calendar_is_present()
    # p.type_date_from(call_date)

