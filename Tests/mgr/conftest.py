import pytest
import random
from bin.project import send
from helpers.product_utils import user_params
from Data.url import mgr
from Data.generics import russian, ukrainian, english
from helpers.utils import make_user_group_roles


@pytest.fixture(scope="function")
def group():
    data = {"$name": ukrainian.unique_name,
            "$parentGroupId": user_params.root_group_id}
    response = send.post(mgr.groups, data)
    yield response.json()
    send.delete(mgr.groups, id_to_url=response.json()['groupId'])


@pytest.fixture(scope="function")
def user_without_roles_and_groups_on_roles():
    data = russian.manager.user()
    response = send.post(mgr.users, data)
    user = response.json()
    user['dateCreate'] = round(user['dateCreate']/1000) * 1000
    yield user
    send.delete(mgr.users, id_to_url=response.json()['userId'])


@pytest.fixture(scope="function")
def user_with_roles_and_without_group_on_roles(group, role):
    data = russian.manager.user()
    user_response = send.post(mgr.users, data)
    user = user_response.json()
    send.put(mgr.user_role, json=[role], id_to_url={'userId': user['userId']}, schema=False)
    user['dateCreate'] = round(user['dateCreate']/1000) * 1000
    yield user
    send.delete(mgr.users, id_to_url=user_response.json()['userId'])

#DEPRECATED: CANT_CREATE_DELETED USER, NEED ADD DATA AND THEN PRESS DELETE
# @pytest.fixture(scope='function')
# def deleted_user(immutable_role, immutable_group_with_child):
#     data = russian.manager.user(group=immutable_group_with_child['groupId'], role=immutable_role['roleId'])
#     data["$deleted"] = True
#     response = send.post(mgr.users, data)
#     user = response.json()
#     user['dateCreate'] = round(user['dateCreate']/1000) * 1000
#     return user


@pytest.fixture(scope="module")
def immutable_user(immutable_group_with_child, immutable_role):
    data = russian.manager.user()
    role_id = immutable_role['roleId']
    group_id = immutable_group_with_child['groupId']
    response = send.post(mgr.users, data)
    user = response.json()
    user_group_to_role = make_user_group_roles({group_id: role_id})
    send.put(mgr.user_role, json=[{"roleId": role_id}], schema=False, id_to_url={"userId": user['userId']})
    send.put(mgr.user_group_roles, json=user_group_to_role, schema=False, id_to_url={"userId": user['userId']})
    user['dateCreate'] = round(user['dateCreate']/1000) * 1000
    yield user
    send.delete(mgr.users, id_to_url=response.json()['userId'])


@pytest.fixture(scope="function")
def role(group):
    data = {"$name": ukrainian.unique_name,
            "$groupId": group['groupId']}
    response = send.post(mgr.roles, data)
    yield response.json()
    send.delete(mgr.roles, id_to_url=response.json()['roleId'])


@pytest.fixture(scope="module")
def immutable_role(immutable_group_with_child):
    data = {"$name": ukrainian.unique_name,
            "$groupId": immutable_group_with_child['groupId']}
    response = send.post(mgr.roles, data)
    yield response.json()
    send.delete(mgr.roles, id_to_url=response.json()['roleId'])


@pytest.fixture(scope="module")
def user_group_roles(immutable_group_with_child, immutable_role, role=None, group=None,):
    if not role:
        role = immutable_role
    if not group:
        group = immutable_group_with_child
    return make_user_group_roles({group['groupId']: role['roleId']})


@pytest.fixture(scope="module")
def create_10_users(immutable_group_with_child, immutable_role):
    users_list = []
    random_choose_lang = random.choice([russian, ukrainian, english])
    data = random_choose_lang.manager.user(count=10)
    group_id = immutable_group_with_child['groupId']
    role_id = immutable_role['roleId']
    for i in data:
        user = send.post(mgr.users, i).json()
        users_list.append(user)
        user_group_to_role = make_user_group_roles({group_id: role_id})
        send.put(mgr.user_role, json=[{"roleId": role_id}], schema=False, id_to_url={"userId": user['userId']})
        send.put(mgr.user_group_roles, json=user_group_to_role, schema=False, id_to_url={"userId": user['userId']})
    yield users_list
    for _ in users_list:
        send.delete(mgr.users, id_to_url=_['userId'])


@pytest.fixture(scope="function")
def add_user_with_role(request):

    def _user(role_name=None, enabled=True):
        role_name = "ROOT" if role_name is None else role_name
        role_id = user_params.get_role_id_by_name(role_name)
        data = russian.manager.user()
        data['$enabled'] = enabled
        data['$password'] = 'qwerty'
        response = send.post(mgr.users, data)
        user = response.json()
        user['dateCreate'] = round(user['dateCreate'] / 1000) * 1000
        user_group_to_role = make_user_group_roles({user_params.root_group_id: role_id})
        send.put(mgr.user_role, json=[{"roleId": role_id}], schema=False, id_to_url={"userId": user['userId']})
        send.put(mgr.user_group_roles, json=user_group_to_role, schema=False, id_to_url={"userId": user['userId']})

        def fin():
            send.delete(mgr.users, id_to_url=user['userId'])
        request.addfinalizer(fin)
        return send.get(mgr.users, id_to_url=user['userId']).json()
    return _user
