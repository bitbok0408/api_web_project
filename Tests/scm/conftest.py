import pytest
from bin.project import send
from Data.generics import english, ukrainian
from Data.url import scm


@pytest.fixture(scope="module")
def cm_group_without_delete():
    data = {"$name": ukrainian.unique_name,
            "$comment": ukrainian.unique_name}
    response = send.post(scm.groups, data)
    yield response.json()
    send.delete(scm.groups, id_to_url=response.json()['cmGroupRid'])



@pytest.fixture(scope="function")
def get_fields_for_report_by_group_id():
    def _fields(group_rid):
        json = {"criteriaList": [{"name": "table_name", "operator": "equal", "values": ["CLIENTS", "REQUESTS"]}]}
        response = send.post(url=scm.group_fields_search, json=json, id_to_url={"group_rid": group_rid}, schema=False)
        return response.json()

    return _fields
