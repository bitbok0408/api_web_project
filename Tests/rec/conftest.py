import pytest
from bin.project import send
from Data.generics import english, ukrainian
from Data.url import rec


@pytest.fixture(scope="module")
def call():
    call_id = None
    data = english.call.make_call_with(records_count=1, content_type="AUDIO")
    for sql_filename in data:
        for sql_data in data[sql_filename]:
            send.sql(sql_name=sql_filename, data=sql_data)
            if sql_filename == "call":
                call_id = sql_data['@CALL_UUID']
    return call_id


@pytest.fixture(scope="function")
def tag():
    data = {"$name": ukrainian.unique_name,
            "$description": ukrainian.string.text()}
    response = send.post(rec.tags, data)
    yield response.json()
    send.delete(rec.tags, id_to_url=response.json()['tagId'])


@pytest.fixture(scope="module")
def immutable_tag():
    data = {"$name": ukrainian.unique_name,
            "$description": ukrainian.string.text()}
    response = send.post(rec.tags, data)
    yield response.json()
    send.delete(rec.tags, id_to_url=response.json()['tagId'])


@pytest.fixture(scope="function")
def call_with_tag(call, tag):
    data = {"$tagId": tag['tagId'],
            "$callId": call}
    response = send.post(rec.tag_to_call, json=data)
    return {"call": response.json(), "tag": tag}


@pytest.fixture(scope='function')
def call_with_params(call):
    response = send.get(rec.calls, id_to_url=call)
    return response.json()


@pytest.fixture(scope='function')
def call_with_recognition_true_error_params(call):
    call_id = None
    data = english.call.make_call_with(records_count=1, content_type="AUDIO", recognize_state=['RECOGNIZED',
                                                                                               'ERROR'])
    for sql_filename in data:
        for sql_data in data[sql_filename]:
            send.sql(sql_name=sql_filename, data=sql_data)
            if sql_filename == "call":
                call_id = sql_data['@CALL_UUID']
    return call_id


@pytest.fixture(scope='function')
def recognizer_setting():
    data = {
              "$language": english.string.word(),
              "$login": english.string.word(),
              "$modelName": ukrainian.unique_name,
              "$password": ukrainian.string.word(),
              "$recognitionUrl": english.string.word()
            }
    response = send.post(rec.recognizer_settings, data)
    yield response.json()
    send.delete(rec.recognizer_settings, id_to_url=response.json()['speechRecognizerSettingsRid'])


@pytest.fixture(scope='function')
def active_recognizer_setting(recognizer_setting):
    settings_id = recognizer_setting['speechRecognizerSettingsRid']
    response = send.put(rec.recognizer_settings_activate, id_to_url={'speechRecognizerSettingsRid': settings_id})
    return response.json()