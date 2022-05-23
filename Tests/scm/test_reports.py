# -*- coding: utf-8 -*-

import allure
import pytest
import time

from bin.project import send
from helpers.validator import equal_schema
from helpers.product_utils import user_params
from Data.url import scm
from Data.generics import english, ukrainian, russian
from Data.fixtures_params import Features


group_id = "qwe"

@allure.feature(Features.functional)
@allure.story('Створюємо списочний звіт з одним полем')
def test_create_list_report():
    data = {
        "$code": "unique_code1112",
        "$value": "val",
        "$info": "text_info",
        "$order": 1,
        "$dict_name": "test_dict",
        "$lvl": 1
    }
    response = send.post(scm.dictionaries, data)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)
