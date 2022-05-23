# -*- coding: utf-8 -*-

import allure
import pytest
import time
from Data.constants import ONE_DAY_UNIX_TIMESTAMP_MS

from bin.project import send
from helpers.validator import equal_schema
from helpers.product_utils import user_params
from Data.url import rec
from config.project_config import cfg
from Data.generics import english, ukrainian, russian
from Data.fixtures_params import Features
from Data.products_modules_criteria import Recording


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.parametrize(("name", "description"), [(ukrainian.unique_name, ukrainian.string.text()),
                                                   (russian.unique_name, russian.string.text()),
                                                   (english.unique_name, english.string.text())])
def test_add_tag(name, description):
    data = {"$name": name,
            "$description": description}
    response = send.post(rec.tags, data)
    schema = response.schema
    assert response.status_code == 200
    equal_schema(response.json(), schema)


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_add_tag_without_name():
    data = {"$name": None,
            "$description": ukrainian.string.text()}
    response = send.post(rec.tags, data)
    expected_response = {'REC_VALIDATION_TAGS_NAME': 'TAG NAME should be from 1 to 255 characters'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_add_tag_without_description():
    data = {"$name": ukrainian.unique_name,
            "$description": None}
    response = send.post(rec.tags, data)
    assert response.status_code == 200


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_add_tag_with_existing_name(immutable_tag):
    existing_name = immutable_tag['name']
    data = {"$name": existing_name,
            "$description": None}
    response = send.post(rec.tags, data)
    expected_response = {'COMMON_ENTITY_WITH_SUCH_FIELD_EXISTS': 'NAME or TAG ID should be unique.'}
    assert response.status_code == 409
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_add_tag_with_existing_description(immutable_tag):
    existing_description = immutable_tag['description']
    data = {"$name": ukrainian.unique_name,
            "$description": existing_description}
    response = send.post(rec.tags, data)
    assert response.status_code == 200


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_edit_tag(tag):
    tag_id = tag['tagId']
    data = {"$tagId": tag_id,
            "$name": ukrainian.unique_name,
            "$description": ukrainian.string.text()}
    response = send.put(rec.tags, data, id_to_url=tag_id)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_edit_tag_on_existing_name(tag, immutable_tag):
    tag_id = tag['tagId']
    existing_tag_name = immutable_tag['name']
    data = {"$tagId": tag_id,
            "$name": existing_tag_name,
            "$description": ukrainian.string.text()}
    response = send.put(rec.tags, data, id_to_url=tag_id)
    expected_response = {'COMMON_ENTITY_WITH_SUCH_FIELD_EXISTS': 'NAME or TAG ID should be unique.'}
    assert response.status_code == 409
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_get_tag_by_id(immutable_tag):
    response = send.get(rec.tags, id_to_url=immutable_tag['tagId'])
    assert response.status_code == 200
    assert response.json()['name'] == immutable_tag['name']


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.xfail(reason='Очепятка в слове Resource')
def test_get_tag_by_unknown_id():
    unknown_tag_id = ukrainian.uuid
    response = send.get(rec.tags, id_to_url=unknown_tag_id)
    expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': f'Resource not found for tagId={unknown_tag_id}'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_delete_tag_by_id(tag):
    response = send.delete(rec.tags, id_to_url=tag['tagId'])
    assert response.status_code == 200
    assert response.json()['name'] == tag['name']


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.xfail(reason='Очепятка в слове Resource')
def test_delete_tag_by_unknown_id():
    unknown_tag_id = ukrainian.uuid
    response = send.delete(rec.tags, id_to_url=unknown_tag_id)
    expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': f'Resource not found for tagId={unknown_tag_id}'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_search_tags(immutable_tag):
    response = send.post(rec.tags_search)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)
    assert immutable_tag in response.json()['data']


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_add_tag_to_call_check_response_schema(tag, call):
    data = {"$tagId": tag['tagId'],
            "$callId": call}
    response = send.post(rec.tag_to_call, json=data)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_add_tag_to_call_check_that_tag_added_to_call(tag, call):
    data = {"$tagId": tag['tagId'],
            "$callId": call}
    send.post(rec.tag_to_call, json=data)
    call_response = send.get(rec.calls, id_to_url=call)
    assert tag['tagId'] == call_response.json()['tags'][0]['tagId']


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_add_unknown_tag_to_call(call):
    unknown_tag_id = ukrainian.uuid
    data = {"$tagId": unknown_tag_id,
            "$callId": call}
    response = send.post(rec.tag_to_call, json=data)
    expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': f'Recourse not found for tagId={unknown_tag_id}'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_add_tag_to_unknown_call(tag):
    unknown_call_id = ukrainian.uuid
    data = {"$tagId": tag['tagId'],
            "$callId": unknown_call_id}
    response = send.post(rec.tag_to_call, json=data)
    expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': f'Call by rid={unknown_call_id} not found'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_remove_tag_from_call_check_response(call_with_tag):
    data = {"$tagId": call_with_tag['tag']['tagId'],
            "$callId": call_with_tag['call']['callId']}
    response = send.post(rec.tag_from_call, data)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_remove_tag_from_call_check_that_tag_deleted_from_call(call_with_tag):
    call_id = call_with_tag['call']['callId']
    data = {"$tagId": call_with_tag['tag']['tagId'],
            "$callId": call_id}
    send.post(rec.tag_from_call, data)
    call_response = send.get(rec.calls, id_to_url=call_id)
    print(call_response.json())
    assert len(call_response.json()['tags']) == 0


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_remove_unknown_tag_to_call(call_with_tag):
    unknown_tag_id = ukrainian.uuid
    data = {"$tagId": unknown_tag_id,
            "$callId": call_with_tag['call']['callId']}
    response = send.post(rec.tag_from_call, data)
    expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': f'Recourse not found for tagId={unknown_tag_id}'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_remove_tag_to_unknown_call(tag):
    unknown_call_id = ukrainian.uuid
    data = {"$tagId": tag['tagId'],
            "$callId": unknown_call_id}
    response = send.post(rec.tag_from_call, data)
    expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': f'Call by rid={unknown_call_id} not found'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.xfail(reason='Отдает 200 ОК, когда пытается удалить тег, который не прикреплен к звонку')
def test_remove_tag_which_is_not_added_to_call(call_with_tag, immutable_tag):
    data = {"$tagId": immutable_tag['tagId'],
            "$callId": call_with_tag['call']['callId']}
    response = send.post(rec.tag_from_call, data)
    expected_response = {
        'COMMON_REQUESTED_RESOURCES_NOT_FOUND': f'Tag with rid={immutable_tag["tagId"]} not added to call'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_get_call_by_id(call):
    response = send.get(rec.calls, id_to_url=call)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_get_call_by_id(call):
    response = send.get(rec.calls, id_to_url=call)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.parametrize(('search_param', 'call_param'), [("callCrmCallId", "crmCallId"), ("callId", "callId"),
                                                          ("callDirection", "direction"), ("callState", "finishState"),
                                                          ("callContentType", "contentType"),
                                                          ("hasComment", "commented"),
                                                          ("callDate", "dateStart"), ("callDuration", "duration"),
                                                          ('recognizeState', 'recognizeState')])
@pytest.mark.xfail(
    reason="#4407 При передаче в criteria_values булевого или интового значение, в ответ приходит стринговое")
def test_search_call(call_with_params, search_param, call_param):
    data = {
        "$criteria_name": search_param,
        "$criteria_operator": "equal",
        "$criteria_values": str(call_with_params[call_param]),
        "$callDateFrom": str(call_with_params['dateStart'] - ONE_DAY_UNIX_TIMESTAMP_MS),
        "$callDateTo": str(call_with_params['dateFinish'] + ONE_DAY_UNIX_TIMESTAMP_MS)
    }
    response = send.post(rec.calls_search, data)
    assert response.status_code == 200
    assert response.json()['data'][0][call_param] == call_with_params[call_param]
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.parametrize(('search_param', 'call_param'), [("callCrmCallId", "crmCallId"), ("callId", "callId"),
                                                          ("callDirection", "direction"), ("callState", "finishState"),
                                                          ("callContentType", "contentType"),
                                                          ("hasComment", "commented"),
                                                          ("callDate", "dateStart")])
def test_search_check_by_call_id(call_with_params, search_param, call_param):
    data = {
        "$criteria_name": search_param,
        "$criteria_operator": "equal",
        "$criteria_values": str(call_with_params[call_param]),
        "$callDateFrom": str(call_with_params['dateStart'] - ONE_DAY_UNIX_TIMESTAMP_MS),
        "$callDateTo": str(call_with_params['dateFinish'] + ONE_DAY_UNIX_TIMESTAMP_MS)
    }
    response = send.post(rec.calls_search, data)
    assert response.status_code == 200
    assert call_with_params["callId"] in [calls['callId'] for calls in response.json()['data']]


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.parametrize('search_param', ["callDurationFrom", "callDurationTo", ])
def test_search_call_by_duration_from_to(call_with_params, search_param):
    data = {
        "$criteria_name": search_param,
        "$criteria_operator": "equal",
        "$criteria_values": round(call_with_params['duration'] / 1000) - 1 if search_param.endswith('From') else
        round(call_with_params['duration'] / 1000) + 1,
        "$callDateFrom": str(call_with_params['dateStart'] - ONE_DAY_UNIX_TIMESTAMP_MS),
        "$callDateTo": str(call_with_params['dateFinish'] + ONE_DAY_UNIX_TIMESTAMP_MS)
    }
    response = send.post(rec.calls_search, data)
    assert call_with_params["callId"] in [calls['callId'] for calls in response.json()['data']]


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.parametrize('search_param', ["recognizeConfidenceFrom", "recognizeConfidenceTo", ])
def test_search_call_by_recognize_confidence_from_to(call_with_params, search_param):
    data = {
        "$criteria_name": search_param,
        "$criteria_operator": "equal",
        "$criteria_values": call_with_params['callStatistic']['recognizeConfidence'] if search_param.endswith(
            'From') else call_with_params['callStatistic']['recognizeConfidence'],
        "$callDateFrom": str(call_with_params['dateStart'] - ONE_DAY_UNIX_TIMESTAMP_MS),
        "$callDateTo": str(call_with_params['dateFinish'] + ONE_DAY_UNIX_TIMESTAMP_MS)
    }
    response = send.post(rec.calls_search, data)
    assert call_with_params["callId"] in [calls['callId'] for
                                          calls in response.json()['data']]


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.parametrize('search_param', ["holdsCount", "holdsDuration", "partsCount", ])
@pytest.mark.xfail(
    reason="#4407 При передаче в criteria_values булевого или интового значение, в ответ приходит стринговое")
def test_search_call_by_call_statistic_params(call_with_params, search_param, ):
    data = {
        "$criteria_name": search_param,
        "$criteria_operator": "equal",
        "$criteria_values": str(call_with_params['callStatistic'][search_param]),
        "$callDateFrom": str(call_with_params['dateStart'] - ONE_DAY_UNIX_TIMESTAMP_MS),
        "$callDateTo": str(call_with_params['dateFinish'] + ONE_DAY_UNIX_TIMESTAMP_MS)
    }
    response = send.post(rec.calls_search, data)
    assert response.status_code == 200
    assert response.json()['data'][0]['callStatistic'][search_param] == call_with_params['callStatistic'][search_param]
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.parametrize('search_param', ["holdsCount", "holdsDuration", "partsCount", ])
def test_search_call_by_call_statistic_params_check_by_call_id(call_with_params, search_param):
    data = {
        "$criteria_name": search_param,
        "$criteria_operator": "equal",
        "$criteria_values": call_with_params['callStatistic'][search_param],
        "$callDateFrom": str(call_with_params['dateStart'] - ONE_DAY_UNIX_TIMESTAMP_MS),
        "$callDateTo": str(call_with_params['dateFinish'] + ONE_DAY_UNIX_TIMESTAMP_MS)
    }
    response = send.post(rec.calls_search, data)
    assert response.status_code == 200
    assert call_with_params["callId"] in [calls['callId'] for calls in response.json()['data']]


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.parametrize('search_param', ["holdsCountFrom", "holdsCountTo", "holdsDurationFrom", "holdsDurationTo",
                                          "partsCountFrom", "partsCountTo", ])
def test_search_call_by_call_statistic_from_to(call_with_params, search_param):
    if search_param.endswith('To'):
        criteria_name = search_param.split('To')[0]
        criteria_value = call_with_params['callStatistic'][criteria_name] + 1
    else:
        criteria_name = search_param.split('From')[0]
        criteria_value = call_with_params['callStatistic'][criteria_name]
    data = {
        "$criteria_name": search_param,
        "$criteria_operator": "equal",
        "$criteria_values": criteria_value,
        "$callDateFrom": str(call_with_params['dateStart'] - ONE_DAY_UNIX_TIMESTAMP_MS),
        "$callDateTo": str(call_with_params['dateFinish'] + ONE_DAY_UNIX_TIMESTAMP_MS)
    }
    response = send.post(rec.calls_search, data)
    assert call_with_params["callId"] in [calls['callId'] for calls in response.json()['data']]


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_get_confidence_settings():
    response = send.get(rec.confidence_settings)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_put_confidence_settings():
    confidence_settings_id = send.get(rec.confidence_settings).json()['confidenceSettingsRid']
    data = {
        "$badMaxValue": english.number.between(0, 49),
        "$goodMaxValue": english.number.between(50, 99)}
    response = send.put(rec.confidence_settings, data, id_to_url=confidence_settings_id)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.parametrize('value', [101, -1])
def test_put_confidence_settings_with_out_of_range_values(value):
    confidence_settings_id = send.get(rec.confidence_settings).json()['confidenceSettingsRid']
    data = {
        "$badMaxValue": value,
        "$goodMaxValue": value}
    response = send.put(rec.confidence_settings, data, id_to_url=confidence_settings_id)
    expected_response = {"REC_RECOGNIZE_CONFIDENCE_SETTINGS_BAD_MAX_VALUE": "Bad max value should be between 0 and 98",
                         "REC_RECOGNIZE_CONFIDENCE_SETTINGS_NORMAL_MAX_VALUE":
                             "Normal max value should be between value of bad max value and 99"}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_put_confidence_settings_bad_max_greater_good_max():
    confidence_settings_id = send.get(rec.confidence_settings).json()['confidenceSettingsRid']
    data = {
        "$badMaxValue": 55,
        "$goodMaxValue": 44}
    expected_response = {"REC_RECOGNIZE_CONFIDENCE_SETTINGS_NORMAL_MAX_VALUE":
                             "Normal max value should be between value of bad max value and 99"}
    response = send.put(rec.confidence_settings, data, id_to_url=confidence_settings_id)
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
@pytest.mark.skip
def test_put_confidence_settings_bad_max_99():
    confidence_settings_id = send.get(rec.confidence_settings).json()['confidenceSettingsRid']
    data = {
        "$badMaxValue": 99,
        "$goodMaxValue": 100}
    expected_response = {'REC_RECOGNIZE_CONFIDENCE_SETTINGS_NORMAL_MAX_VALUE': 'Normal max value '
                                                                               'should be between '
                                                                               'value of bad max value '
                                                                               'and 100'}
    response = send.put(rec.confidence_settings, data, id_to_url=confidence_settings_id)
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_post_recognizer_setting():
    data = {
        "$language": english.string.word(),
        "$login": english.string.word(),
        "$modelName": ukrainian.unique_name,
        "$password": ukrainian.string.word(),
        "$recognitionUrl": english.string.word()
    }
    response = send.post(rec.recognizer_settings, data)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_put_recognizer_setting(recognizer_setting):
    settings_id = recognizer_setting['speechRecognizerSettingsRid']
    data = {"$speechRecognizerSettingsRid": settings_id,
            "$language": english.string.word(),
            "$login": english.string.word(),
            "$modelName": ukrainian.unique_name,
            "$password": ukrainian.string.word(),
            "$recognitionUrl": english.string.word()
            }
    response = send.put(rec.recognizer_settings, data, id_to_url=settings_id)
    assert response.status_code == 200
    equal_schema(response.json(), response.schema)


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_delete_recognizer_setting(recognizer_setting):
    settings_id = recognizer_setting['speechRecognizerSettingsRid']
    response = send.delete(rec.recognizer_settings, id_to_url=settings_id)
    assert response.status_code == 200


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_delete_recognizer_setting_with_unknown_id():
    unknown_settings_id = ukrainian.uuid
    response = send.delete(rec.recognizer_settings, id_to_url=unknown_settings_id)
    expected_response = {'SETTINGS_EXCEPTION': f'SpeechRecognizerSettings not founded with rid {unknown_settings_id}'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_get_recognizer_setting(recognizer_setting):
    settings_id = recognizer_setting['speechRecognizerSettingsRid']
    response = send.get(rec.recognizer_settings)
    assert response.status_code == 200
    assert settings_id in [setting['speechRecognizerSettingsRid'] for setting in response.json()]
    assert "password" not in response.json()[0].keys()


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_put_recognizer_setting_activate(recognizer_setting):
    settings_id = recognizer_setting['speechRecognizerSettingsRid']
    response = send.put(rec.recognizer_settings_activate, id_to_url={'speechRecognizerSettingsRid': settings_id})
    assert response.status_code == 200
    assert response.json()['speechRecognizerSettingsRid'] == settings_id
    assert response.json()['default'] is True


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_put_recognizer_setting_activate_unknown_id(recognizer_setting):
    unknown_settings_id = ukrainian.uuid
    response = send.put(rec.recognizer_settings_activate, id_to_url={'speechRecognizerSettingsRid': unknown_settings_id})
    expected_response = {'SETTINGS_EXCEPTION': f'SpeechRecognizerSettings not founded with rid {unknown_settings_id}'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_delete_active_recognizer_setting(active_recognizer_setting):
    settings_id = active_recognizer_setting['speechRecognizerSettingsRid']
    response = send.delete(rec.recognizer_settings, id_to_url=settings_id)
    expected_response = {'SETTINGS_EXCEPTION': 'Default speechRecognizerSettings cannot be deleted'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_active_recognizer_setting_only_one(recognizer_setting):
    settings_id = recognizer_setting['speechRecognizerSettingsRid']
    send.put(rec.recognizer_settings_activate, id_to_url=settings_id)
    response = send.get(rec.recognizer_settings)
    assert len([setting for setting in response.json() if setting['default'] is True]) == 1


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_re_recognize_call(recognizer_setting, call):
    settings_id = recognizer_setting['speechRecognizerSettingsRid']
    call_id = call
    data = {"$callRid": call_id,
            "$speechRecognizerSettingsRid": settings_id}
    response = send.put(rec.re_recognize, data)
    assert response.status_code == 200


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_re_recognize_call_with_unknown_call_id(recognizer_setting):
    settings_id = recognizer_setting['speechRecognizerSettingsRid']
    unknown_call_id = ukrainian.uuid
    data = {"$callRid": unknown_call_id,
            "$speechRecognizerSettingsRid": settings_id}
    response = send.put(rec.re_recognize, data)
    expected_response = {'CALL_ENTITY_NOT_FOUND': "Calls with rid doesn't exist: " f'[{unknown_call_id}]'}
    assert response.status_code == 400
    assert response.json() == expected_response


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_re_recognize_call_with_unknown_settings_id(recognizer_setting, call):
    unknown_settings_id = ukrainian.uuid
    call_id = call
    data = {"$callRid": call_id,
            "$speechRecognizerSettingsRid": unknown_settings_id}
    response = send.put(rec.re_recognize, data)
    expected_result = {'SETTINGS_EXCEPTION': f'SpeechRecognizerSettings not founded with rid {unknown_settings_id}'}
    assert response.status_code == 400
    assert response.json() == expected_result


@allure.feature(Features.functional)
@allure.story('Создаем группу без parentGroupId')
def test_statistic_model_after_re_recognize(recognizer_setting, call_with_recognition_true_error_params):
    call_id = call_with_recognition_true_error_params
    data = {"$callRid": call_id,
            "$speechRecognizerSettingsRid": recognizer_setting['speechRecognizerSettingsRid']}
    response_recognize = send.put(rec.re_recognize, data)
    assert response_recognize.status_code == 200
    response = send.get(rec.calls, id_to_url=call_id)
    assert response.json()['callStatistic']['recognizeConfidence'] is None
    assert response.json()['callStatistic']['recognizeLanguageCode'] == recognizer_setting['speechRecognizerSettingsRid']
    assert response.json()['recognizeState'] == 'RE_RECOGNIZE'


@allure.feature(Features.validation)
@allure.story('Создаем группу без parentGroupId')
def test_add_recognizer_setting_with_existing_name(recognizer_setting):
    existing_name = recognizer_setting['modelName']
    data = {
        "$language": english.string.word(),
        "$login": english.string.word(),
        "$modelName": existing_name,
        "$password": ukrainian.string.word(),
        "$recognitionUrl": english.string.word()
    }
    expected_response = {'SETTINGS_EXCEPTION': 'Speech recognizer settings model name is not uniques. '
                       'Try to rename model name'}
    response = send.post(rec.recognizer_settings, data)
    assert response.status_code == 400
    assert response.json() == expected_response
