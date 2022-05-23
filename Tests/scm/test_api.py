# -*- coding: utf-8 -*-

import allure
import pytest
import time

from bin.project import send
from helpers.validator import equal_schema
from helpers.product_utils import user_params
from Data.url import scm
from config.project_config import cfg
from Data.generics import english, ukrainian, russian
from Data.fixtures_params import Features
from Data.products_modules_criteria import ContactManager


@allure.feature(Features.functional)
@allure.story('Создаем группу')
@pytest.mark.parametrize(['name', 'comment'], [(english.unique_name, english.string.word()),
                                               (russian.unique_name, russian.string.word()),
                                               (ukrainian.unique_name, ukrainian.string.word())])
def test_add_group(name, comment):
    data = {"$name": name,
            "$comment": comment}
    response = send.post(scm.groups, data)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без комента')
def test_add_group_without_comment():
    data = {"$name": ukrainian.unique_name,
            "$comment": None}
    response = send.post(scm.groups, data)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.validation)
@allure.story('Создаем группу без имени')
def test_add_group_without_name():
    data = {"$name": None,
            "$comment": ukrainian.unique_name}
    response = send.post(scm.groups, data)
    expected_response = {'GROUP_NAME_IS_BLANK': 'Group name can not be empty'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу с уже существующим именем')
@pytest.mark.skip
def test_add_group_with_existing_name(cm_group_without_delete):
    data = {"$name": cm_group_without_delete['name'],
            "$comment": ukrainian.unique_name}
    response = send.post(scm.groups, data)
    expected_response = {'GROUP_NAME_IS_BLANK': 'Group name can not be empty'}
    assert response.status_code == 400
    assert response.json() == expected_response


# TODO: Проверить что создаются поля при использщовании ТРУ параметра
@allure.feature(Features.functional)
@allure.story('Создаем группу с параметром useForSCM = true')
def test_add_group_with_useForSCM_true():
    data = {"$name": ukrainian.unique_name,
            "$comment": ukrainian.unique_name,
            "$useForSCM": True}
    response = send.post(scm.groups, data)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без параметра useForSCM')
def test_add_group_without_useForSCM():
    data = {"$name": ukrainian.unique_name,
            "$comment": ukrainian.unique_name,
            "$useForSCM": None}
    response = send.post(scm.groups, data)
    assert response.status_code == 200
    assert response.json()['useForSCM'] is False


@allure.feature(Features.functional)
@allure.story('Редактируем группу')
@pytest.mark.parametrize(['name', 'comment'], [(english.unique_name, english.string.word()),
                                               (russian.unique_name, russian.string.word()),
                                               (ukrainian.unique_name, ukrainian.string.word())])
def test_put_group(name, comment, cm_group_without_delete):
    group_id = cm_group_without_delete['rid']
    data = {"$name": name,
            "$comment": comment,
            "$rid": group_id}
    response = send.put(scm.groups, data, id_to_url=group_id)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Редактируем группу на параметр  useForSCM = true')
def test_edit_group_on_useForSCM_true(cm_group_without_delete):
    group_id = cm_group_without_delete['rid']
    data = {"$name": ukrainian.unique_name,
            "$comment": ukrainian.unique_name,
            "$rid": group_id,
            "$useForSCM": True}
    response = send.put(scm.groups, data, id_to_url=group_id)
    assert response.status_code == 200
    assert response.json()['useForSCM'] is False


@allure.feature(Features.functional)
@allure.story('Редактируем группу с неизвесным UUID')
def test_edit_group_with_unknown_uuid():
    group_id = ukrainian.uuid
    data = {"$name": ukrainian.unique_name,
            "$comment": ukrainian.unique_name,
            "$rid": group_id,
            "$useForSCM": True}
    expected_response = {'CM_GROUP_NOT_FOUND_EXCEPTION': f"Group doesn't exist with rid={group_id}"}
    response = send.put(scm.groups, data, id_to_url=group_id)
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Получаем групу по rid')
def test_get_group_by_rid(cm_group_without_delete):
    group_id = cm_group_without_delete['rid']
    response = send.get(scm.groups, id_to_url=group_id)
    assert response.status_code == 200
    assert response.json() == cm_group_without_delete


@allure.feature(Features.validation)
@allure.story('Получаем групу по неизвестному rid')
def test_get_group_by_unknown_rid():
    unknown_group_id = ukrainian.uuid
    response = send.get(scm.groups, id_to_url=unknown_group_id)
    expected_response = {'CM_GROUP_NOT_FOUND_EXCEPTION': f"Group doesn't exist with rid={unknown_group_id}"}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Получаем список груп')
def test_get_groups_list(cm_group_without_delete):
    response = send.get(scm.groups)
    assert response.status_code == 200
    assert cm_group_without_delete in response.json()


@allure.feature(Features.functional)
@allure.story('Удаляем групу по rid')
def test_delete_group_by_rid(cm_group_without_delete):
    group_id = cm_group_without_delete['rid']
    response = send.delete(scm.groups, id_to_url=group_id)
    assert response.status_code == 200
    assert response.json() == cm_group_without_delete


@allure.feature(Features.validation)
@allure.story('Удаляем груп у по неизвестному rid')
def test_delete_group_by_unknown_rid():
    unknown_group_id = ukrainian.uuid
    response = send.delete(scm.groups, id_to_url=unknown_group_id)
    expected_response = {'CM_GROUP_NOT_FOUND_EXCEPTION': f"Group doesn't exist with rid={unknown_group_id}"}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Удаляем групу по rid')
def test_check_that_deleted_group_doesnt_show(cm_group_without_delete):
    group_id = cm_group_without_delete['rid']
    send.delete(scm.groups, id_to_url=group_id)
    response = send.get(scm.groups)
    assert cm_group_without_delete not in response.json()


@allure.feature(Features.functional)
@allure.story('Создаем поле для клиента с типами данных кроме TEXT i DICTIONARY')
@pytest.mark.parametrize('data_type',
                         [i for i in ContactManager.client_field_datatype if i != "TEXT" and i != "DICTIONARY"])
def test_add_client_field_with_different_data_types(cm_group_without_delete, data_type):
    group_id = cm_group_without_delete['cmGroupRid']
    data = {"$field_name": english.string.word(),
            "$tittle": ukrainian.string.word(),
            "$data_type": data_type}
    response = send.post(scm.clients_fields, data, id_to_url=group_id)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем поле для клиента с типом данных TEXT')
def test_add_client_field_with_text_data_types(cm_group_without_delete):
    group_id = cm_group_without_delete['cmGroupRid']
    data = {"$field_name": english.string.word(),
            "$tittle": ukrainian.string.word(),
            "$data_type": "TEXT",
            "$inputType": "TEXT"}
    response = send.post(scm.clients_fields, data, id_to_url=group_id)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


# @allure.feature(Features.functional)
# @allure.story('Создаем поле для клиента с типом данных DICTIONARY')
# def test_add_client_field_with_dictionary_data_types(cm_group_without_delete):
#     group_id = cm_group_without_delete['cmGroupRid']
#     data = {"$field_name": english.string.word(),
#             "$tittle": ukrainian.string.word(),
#             "$data_type": "DICTIONARY",
#             "$inputType": "EDIT"}
#     response = send.post(scm.clients_fields, data, id_to_url=group_id)
#     assert response.status_code == 200
#     equal_schema(response.json(), response.schema)




