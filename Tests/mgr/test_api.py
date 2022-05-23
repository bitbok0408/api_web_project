# -*- coding: utf-8 -*-

import allure
import pytest
import random

from bin.project import send
from helpers.validator import equal_schema
from helpers.product_utils import user_params
from Data.url import mgr, AuthServer
from config.project_config import cfg
from Data.generics import english, ukrainian, russian


class TestAuthorizationServer:

    @allure.feature('Функциональный тест')
    @allure.story('Получаем токент для рута')
    def test_get_token_for_root(self):
        credentials = cfg.credentials
        data = {"$principal": credentials['principal'],
                "$credential": credentials['credential']}
        response = send.post(AuthServer.token, data)
        assert (response.status_code, "X-Company-Auth-Token") == (200, response.json()['name'])

    @allure.feature('Функциональный тест')
    @allure.story('Получаем токент для разных системных ролей')
    @pytest.mark.parametrize("role_name",
                             ["ROOT", "ADMINISTRATOR", "SUPERVISOR", "USER"])
    def test_get_token_for_system_roles(self, add_user_with_role, role_name):
        user = add_user_with_role(role_name)
        data = {"$principal": user['login'],
                "$credential": "qwerty"}
        response = send.post(AuthServer.token, data)
        equal_schema(response.json(), response.schema)

    @allure.feature('Функциональный тест')
    @allure.story('Получаем токент с не правильными полномочиями')
    def test_get_token_with_wrong_credentials(self):
        data = {"$principal": ukrainian.person.username(),
                "$credential": ukrainian.string.word()}
        response = send.post(AuthServer.token, data)
        expected_result = {'SAS_AUTHORIZATION_ERROR': 'Authorization Error'}
        assert (response.status_code, response.json()) == (400, expected_result)

    @allure.feature('Функциональный тест')
    @allure.story('Получаем токент с пустыми полномочиями(логин, пароль)')
    def test_get_token_with_empty_credentials(self):
        data = {"principal": None, "credential": None}
        response = send.post(AuthServer.token, data)
        expected_result = {'PRINCIPAL_EMPTY': 'principal is empty', 'CREDENTIALS_EMPTY': 'credentials is empty'}
        assert (response.status_code, response.json()) == (400, expected_result)

    # DEPRECATED: check conftest make_deleted_user
    # @allure.feature('Функциональный тест')
    # @allure.story('Получаем токент для удаленного пользователя')
    # def test_get_token_for_deleted_user(self, immutable_deleted_user):
    #     data = {"$principal": immutable_deleted_user['login'],
    #             "$credential": "qwerty"}
    #     response = send.post(AuthServer.token, data)
    #     expected_response = {'PRINCIPAL_NOT_FOUND': 'Not authorized. No user found'}
    #     assert (response.json(), response.status_code) == (expected_response, response.status_code)

    @allure.feature('Функциональный тест')
    @allure.story('Получаем токент для пользователя без прав доступа')
    def test_get_token_for_user_without_credentials(self, immutable_user):
        data = {"$principal": immutable_user['login'],
                "$credential": "qwerty"}
        response = send.post(AuthServer.token, data)
        expected_response = {'SAS_AUTHORIZATION_ERROR': 'Authorization Error'}
        assert (response.json(), response.status_code) == (expected_response, 400)

    @allure.feature('Функциональный тест')
    @allure.story('Получаем токент для выключеного пользователя')
    def test_get_token_for_disabled_user(self, add_user_with_role):
        user = add_user_with_role("ROOT", enabled=False)
        data = {"$principal": user['login'],
                "$credential": "qwerty"}
        response = send.post(AuthServer.token, data)
        expected_response = {'USER_DISABLED': 'Account disabled'}
        assert (response.status_code, response.json()) == (500, expected_response)

    @allure.feature('Функциональный тест')
    @allure.story('Логинимся с полученым токеном и проверяем соответсвие логина')
    def test_sign_in_with_token_check_login(self, add_user_with_role):
        user = add_user_with_role('ADMINISTRATOR')
        data = {"$principal": user['login'],
                "$credential": "qwerty",
                "$sessionLiveTimeSec": 300}
        response_auth = send.post(AuthServer.token, data)
        response_auth = response_auth.json()
        headers = {'content-type': "application/json;charset=UTF-8", response_auth['name']: response_auth['token']}
        response_current_account = send.get(mgr.account, headers=headers)
        assert user['login'] == response_current_account.json()['login']


class TestGroups:

    @allure.feature('Функциональный тест')
    @allure.story('Получаем все группы')
    def test_get_groups(self):
        response = send.get(mgr.groups)
        assert response.status_code == 200 and "ROOT" in response.json()[0]['name']

    @allure.feature('Функциональный тест')
    @allure.story('Получаем групу по ID')
    def test_get_group_by_id(self, group):
        response = send.get(mgr.groups, id_to_url=group['groupId'])
        assert (response.status_code, response.json()) == (200, group)

    @allure.feature('Функциональный тест')
    @allure.story('Проверяем есть ли ранеее созданная группа в списке полученных груп')
    def test_get_group_few_group_in_group_list(self, group):
        response = send.get(mgr.groups)
        root_childs_id = [group['groupId'] for group in response.json()[0]['children']]
        assert response.status_code == 200 and group['groupId'] in root_childs_id

    @allure.feature('Проверка валидации')
    @allure.story('Получаем группу с неизвестным id')
    def test_get_group_with_unknown_id(self):
        unknown_id = ukrainian.uuid
        response = send.get(mgr.groups, id_to_url=unknown_id)
        excepted_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': 'GROUP by groupId=%s not found' % unknown_id}
        assert (response.status_code, response.json()) == (400, excepted_response)

    @allure.feature('Функциональный тест')
    @allure.story('Создаем группу')
    @pytest.mark.parametrize('name', [ukrainian.unique_name, russian.unique_name, english.unique_name])
    def test_add_group(self, name):
        data = {"$name": name,
                "$parentGroupId": user_params.root_group_id}
        response = send.post(mgr.groups, data)
        assert response.status_code == 201
        equal_schema(response.json(), response.schema)

    @allure.feature('Проверка валидации')
    @allure.story('Создаем группу без имени')
    def test_add_group_without_name(self):
        data = {"$name": None,
                "$parentGroupId": user_params.root_group_id}
        response = send.post(mgr.groups, data)
        excepted_response = {'ADM_VALIDATION_GROUP_NAME': 'Group name not specified'}
        assert (response.status_code, response.json()) == (400, excepted_response)

    @allure.feature('Проверка валидации')
    @allure.story('Создаем группу без parentGroupId')
    def test_add_group_without_group(self):
        data = {"$name": ukrainian.unique_name,
                "$parentGroupId": None}
        response = send.post(mgr.groups, data)
        excepted_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': 'GROUP by groupId=null not found'}
        assert (response.status_code, response.json()) == (400, excepted_response)

    @allure.feature('Проверка валидации')
    @allure.story('Создаем группу с неизвестным parendGroupId')
    def test_add_group_with_unknown_parent_group_id(self):
        random_group_id = ukrainian.uuid
        data = {"$name": ukrainian.unique_name,
                "$parentGroupId": random_group_id
                }
        response = send.post(mgr.groups, data)
        expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': 'GROUP by groupId=%s not found' % random_group_id}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Функциональный тест')
    @allure.story('Создаем группу с сущесвующим именем')
    def test_add_group_with_existing_name(self, immutable_group_with_child):
        existing_group_name = immutable_group_with_child['name']
        data = {"$name": existing_group_name,
                "$parentGroupId": user_params.root_group_id}
        response = send.post(mgr.groups, data)
        assert response.status_code == 201
        equal_schema(response.json(), response.schema)

    @allure.feature('Функциональный тест')
    @allure.story('Редактируем группу')
    def test_edit_group(self, group):
        data = {"$name": ukrainian.unique_name,
                "$groupId": group['groupId']}
        response = send.put(mgr.groups, data, id_to_url=group['groupId'])
        assert response.status_code == 200
        equal_schema(response.json(), response.schema)

    @allure.feature('Функциональный тест')
    @allure.story('Редактируем группу на пустое имя')
    def test_edit_group_on_empty_name(self, group):
        data = {"$name": None,
                "$groupId": group['groupId']}
        response = send.put(mgr.groups, data, id_to_url=group['groupId'])
        expected_response = {'ADM_VALIDATION_GROUP_NAME': 'Group name not specified'}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Функциональный тест')
    @allure.story('Редактируем группу с неизвестным groupId')
    def test_edit_group_with_unknown_group_id(self, group):
        unknown_group_id = ukrainian.uuid
        data = {"$name": ukrainian.unique_name,
                "$groupId": group['groupId']}
        response = send.put(mgr.groups, data, id_to_url=unknown_group_id)
        expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': 'GROUP by groupId=%s not found' % unknown_group_id}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Функциональный тест')
    @allure.story('Удаляем группу')
    def test_delete_group(self, group):
        response = send.delete(mgr.groups, id_to_url=group['groupId'])
        assert (response.status_code, response.json()) == (200, group)

    @allure.feature('Проверка валидации')
    @allure.story('Удаляем группу с неизвестным id')
    def test_delete_group_with_unknown_id(self):
        unknown_group_id = ukrainian.uuid
        response = send.delete(mgr.groups, id_to_url=unknown_group_id)
        expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': 'GROUP by groupId=%s not found' % unknown_group_id}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Проверка валидации')
    @allure.story('Удаляем группу у которой есть child')
    def test_delete_group_with_child(self, immutable_group_with_child):
        group_id = immutable_group_with_child['groupId']
        response = send.delete(mgr.groups, id_to_url=group_id)
        expected_response = {'COMMON_NOT_ALLOWED_OPERATION': 'The group has subgroups'}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Проверка валидации')
    @allure.story('Удаляем ROOT группу')
    def test_delete_root_group(self):
        response = send.delete(mgr.groups, id_to_url=user_params.root_group_id)
        expected_response = {'COMMON_NOT_ALLOWED_OPERATION': "You can't delete ROOT group"}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Проверка валидации')
    @allure.story('Удаляем групу, к которой привязана роль')
    def test_delete_root_which_have_role(self, role):
        response = send.delete(mgr.groups, id_to_url=role['group']['groupId'])
        expected_response = {'ADM_GROUP_ROLE_CONSTRAINT_EXCEPTION': 'Unable to delete the group due some '
                                                                    'roles are assigned to it'}
        assert (response.status_code, response.json()) == (500, expected_response)

    @allure.feature('Проверка валидации')
    @allure.story('Проверяем что cid ROOT групы = 0')
    def test_check_cid_of_root_group(self):
        response = send.get(mgr.groups, id_to_url=user_params.root_group_id)
        assert response.json()['cid'] == 0

    @allure.feature('Проверка валидации')
    @allure.story('Проверяем что cid групы созданой под ROOT == id ROOT групы')
    @pytest.mark.xfail(reason='https://helpdesk.company.com/issues/4135')
    def test_check_cid_of_root_child_group(self, immutable_group_with_child):
        response = send.get(mgr.groups, id_to_url=immutable_group_with_child['groupId'])
        assert response.json()['cid'] == user_params.root_group_id

    @allure.feature('Проверка валидации')
    @allure.story('Проверяем что cid групы созданой на n уровне ниже под ROOT == id ROOT групы')
    @pytest.mark.xfail(reason='https://helpdesk.company.com/issues/4135')
    def test_check_cid_of_root_2nd_child_group(self, immutable_group_with_child):
        response = send.get(mgr.groups, id_to_url=immutable_group_with_child['children'][0]['groupId'])
        assert response.json()['cid'] == user_params.root_group_id


class TestRoles:

    @allure.feature('Функциональний тест')
    @allure.story('Создаем роль с первым child от рута')
    def test_add_role_with_first_root_child(self, immutable_group_with_child):
        data = {"$name": ukrainian.unique_name,
                "$groupId": immutable_group_with_child['groupId']}
        response = send.post(mgr.roles, data)
        assert response.status_code == 201
        equal_schema(response.json(), response.schema)

    @allure.feature('Функциональний тест')
    @allure.story('Создаем роль')
    def test_add_role_without_name(self, immutable_group_with_child):
        data = {"$name": None,
                "$groupId": immutable_group_with_child['groupId']}
        response = send.post(mgr.roles, data)
        expected_response = {'ADM_VALIDATION_ROLE_NAME': 'Role name not specified'}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Функциональний тест')
    @allure.story('Создаем роль с root групой')
    def test_add_role_with_root_group(self):
        data = {"$name": ukrainian.unique_name,
                "$groupId": user_params.root_group_id}
        response = send.post(mgr.roles, data)
        assert response.status_code == 201
        equal_schema(response.json(), response.schema)

    @allure.feature('Функциональний тест')
    @allure.story('Создаем роль с templateRole')
    def test_add_role_with_template_role(self, immutable_group_with_child):
        data = {"$name": ukrainian.unique_name,
                "$groupId": immutable_group_with_child['groupId'],
                "$templateRole": {"roleId": user_params.root_role_id}}
        response = send.post(mgr.roles, data)
        assert (response.status_code, response.json()['templateRole']['roleId']) == (201, user_params.root_role_id)

    @allure.feature('Функциональний тест')
    @allure.story('Создаем роль с вторым по вложености child')
    def test_add_role_with_second_child(self, immutable_group_with_child):
        child_group_id = immutable_group_with_child['children'][0]['groupId']
        data = {"$name": ukrainian.unique_name,
                "$groupId": child_group_id}
        response = send.post(mgr.roles, data)
        assert (response.status_code, response.json()['group']['groupId']) == (
            201, immutable_group_with_child['groupId'])

    @allure.feature('Функциональний тест')
    @allure.story('Создаем роль без группы')
    def test_add_role_without_group(self):
        data = {"$name": ukrainian.unique_name,
                "$groupId": None}
        response = send.post(mgr.roles, data)
        expected_response = {'ADM_VALIDATION_ROLE_GROUP_EMPTY': 'Role group not specified'}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Функциональний тест')
    @allure.story('Создаем роль с неизвестной групой')
    def test_add_role_with_unknown_group(self):
        unknown_group_id = ukrainian.uuid
        data = {"$name": ukrainian.unique_name,
                "$groupId": unknown_group_id}
        response = send.post(mgr.roles, data)
        expected_response = {
            'ADM_VALIDATION_GROUP_NOT_FOUND': 'Group by the following group id not found: %s' % unknown_group_id}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Функциональний тест')
    @allure.story('Создаем роль с сущесвующим именем')
    def test_add_role_with_existing_name(self, role):
        existing_name = role['name']
        data = {"$name": existing_name,
                "$groupId": role['group']['groupId']}
        response = send.post(mgr.roles, data)
        expected_response = {'COMMON_ENTITY_WITH_SUCH_FIELD_EXISTS': 'Name is not unique'}
        assert (response.status_code, response.json()) == (409, expected_response)

    @allure.feature('Функциональний тест')
    @allure.story('Создаем роль с сущесвующим именем в другой групе')
    def test_add_role_with_existing_name_different_groups(self, role):
        existing_name = role['name']
        data = {"$name": existing_name,
                "$groupId": user_params.root_group_id}
        response = send.post(mgr.roles, data)
        assert response.status_code == 201
        equal_schema(response.json(), response.schema)

    @allure.feature('Функциональний тест')
    @allure.story('Получаем все роли')
    def test_get_roles(self, role):
        response = send.get(mgr.roles)
        role.pop("templateRole")
        assert response.status_code == 200 and role in response.json()

    @allure.feature('Функциональний тест')
    @allure.story('Получаем конкретную роль по id')
    def test_get_role_by_id(self, role):
        response = send.get(mgr.roles, id_to_url=role['roleId'])
        role.pop("templateRole")
        assert (response.status_code, response.json()) == (200, role)

    @allure.feature('Функциональний тест')
    @allure.story('Получаем конкретную роль по не известному id')
    def test_get_role_by_unknown_id(self):
        unknown_role_id = ukrainian.uuid
        response = send.get(mgr.roles, id_to_url=unknown_role_id)
        expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': 'ROLE by roleId=%s not found' % unknown_role_id}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Функциональний тест')
    @allure.story('Удаляем роль')
    def test_delete_role(self, role):
        role.pop("templateRole")
        response = send.delete(mgr.roles, id_to_url=role['roleId'])
        assert (response.status_code, response.json()) == (200, role)

    @allure.feature('Функциональний тест')
    @allure.story('Удаляем роль с неизвестным id')
    def test_delete_role_by_unknown_id(self):
        unknown_role_id = ukrainian.uuid
        response = send.delete(mgr.roles, id_to_url=unknown_role_id)
        expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': 'ROLE by roleId=%s not found' % unknown_role_id}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('Функциональний тест')
    @allure.story('Удаляем системную роль')
    def test_delete_system_role(self):
        response = send.delete(mgr.roles, id_to_url=user_params.root_role_id)
        expected_response = {'COMMON_INVALID_SYSTEM_ROLE_OPERATION': "System role can't be deleted"}
        assert response.status_code == 400
        assert response.json() == expected_response

    @allure.feature('Функциональний тест')
    @allure.story('Редактируем роль')
    def test_edit_role(self, role, immutable_group_with_child):
        data = {"$roleId": role['roleId'],
                "$name": ukrainian.unique_name,
                "$groupId": immutable_group_with_child['groupId']
                }
        response = send.put(mgr.roles, data, id_to_url=role['roleId'])
        assert response.status_code == 200
        equal_schema(response.json(), response.schema)

    @allure.feature('Функциональний тест')
    @allure.story('Редактируем системную роль')
    @pytest.mark.xfail(reason="https://helpdesk.company.com/issues/4136")
    def test_edit_system_role(self):
        data = {"$roleId": user_params.root_role_id,
                "$name": ukrainian.unique_name,
                "$groupId": user_params.root_group_id
                }
        response = send.put(mgr.roles, data, id_to_url=user_params.root_role_id)
        expected_response = {'COMMON_INVALID_SYSTEM_ROLE_OPERATION': "System role can't be modified"}
        assert response.status_code == 400
        assert response.json() == expected_response

    @allure.feature('Функциональний тест')
    @allure.story('Редактируем роль на пустое имя')
    @pytest.mark.skip(reason='https://helpdesk.company.com/issues/4136')
    def test_edit_role_on_empty_name(self, role, immutable_group_with_child):
        data = {"$roleId": role['roleId'],
                "$name": None,
                "$groupId": immutable_group_with_child['groupId']
                }
        response = send.put(mgr.roles, data, id_to_url=role['roleId'])
        expected_response = {'ADM_VALIDATION_ROLE_NAME': 'Role name not specified'}
        assert (response.json(), response.status_code) == (expected_response, 400)

    @allure.feature('Функциональний тест')
    @allure.story('Редактируем роль на не существующую групу')
    def test_edit_role_on_unknown_group(self, role):
        unknown_group_id = ukrainian.uuid
        data = {"$roleId": role['roleId'],
                "$name": ukrainian.unique_name,
                "$groupId": unknown_group_id
                }
        response = send.put(mgr.roles, data, id_to_url=role['roleId'])
        expected_response = {
            'ADM_VALIDATION_GROUP_NOT_FOUND': 'Group by the following group id not found: %s' % unknown_group_id}
        assert (response.json(), response.status_code) == (expected_response, 400)

    @allure.feature('Функциональний тест')
    @allure.story('Редактируем имя роли на существующее')
    def test_edit_role_name_on_existing(self, role, immutable_role):
        existing_name = immutable_role['name']
        data = {"$roleId": role['roleId'],
                "$name": existing_name,
                "$groupId": immutable_role['group']['groupId']
                }
        response = send.put(mgr.roles, data, id_to_url=role['roleId'])
        expected_response = {'COMMON_ENTITY_WITH_SUCH_FIELD_EXISTS': 'Name is not unique'}
        assert (response.json(), response.status_code) == (expected_response, 409)


# TODO: Проверить фильтр без criteriaList (нужно продумать как брать request body из json), все тесты с пользователями и групами переделать, так как групы добавляются после создания пользователя
class TestUsers:

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя только с обязательными полями')
    def test_add_user_with_required_fields(self, immutable_role, user_group_roles):
        data = {"$login": ukrainian.generic.company.login(),
                "$fname": ukrainian.person.name(),
                "$lname": ukrainian.person.last_name(),
                "$roleId": immutable_role['roleId']
                }
        response = send.post(mgr.users, data)
        assert response.status_code == 201
        equal_schema(response.json(), response.schema)

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя только с обязательными полями')
    def test_add_user_group_roles(self, user_with_roles_and_without_group_on_roles, role, group, user_group_roles):
        user_id = user_with_roles_and_without_group_on_roles['userId']
        response = send.put(mgr.user_group_roles, json=user_group_roles(group=group, role=role),
                            id_to_url={'userId': user_id}, schema=False)
        assert response.status_code == 201
        assert len(response.json()['userGroupRoles']) == len(user_group_roles)

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя с групами, которые не должны присваиватся этим методом')
    def test_add_user_with_group_roles_which_must_be_empty_in_response(self, immutable_role, user_group_roles):
        data = {"$login": ukrainian.generic.company.login(),
                "$fname": ukrainian.person.name(),
                "$lname": ukrainian.person.last_name(),
                "$roleId": immutable_role['roleId'],
                "$userGroupRoles": user_group_roles
                }
        response = send.post(mgr.users, data)
        assert response.status_code == 201
        equal_schema(response.json(), response.schema)
        assert len(response.json()['userGroupRoles']) == 0

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя со всеми полями')
    @pytest.mark.parametrize('user', [ukrainian.manager.user(), russian.manager.user(), english.manager.user()])
    def test_add_user_with_all_fields(self, user, immutable_role):
        data = user
        response = send.post(mgr.users, data)
        assert response.status_code == 201
        equal_schema(response.json(), response.schema)


    # Фікстура створює користувача а тест поивнен тільки добавити роль на групу
    # @allure.feature('функциональный тест')
    # @allure.story('Создаем пользователя с групой, которая первый child от ROOT')
    # def test_add_user_with_child_root_group(self, immutable_group_with_child):
    #     data = ukrainian.manager.user(group=immutable_group_with_child['groupId'])
    #     response = send.post(mgr.users, data)
    #     assert response.status_code == 201
    #     equal_schema(response.json(), response.schema)
    #
    # @allure.feature('функциональный тест')
    # @allure.story('Создаем пользователя с групой, которая второй child от ROOT')
    # def test_add_user_with_2nd_child_root_group(self, immutable_group_with_child):
    #     data = ukrainian.manager.user(group=immutable_group_with_child['children'][0]['groupId'])
    #     response = send.post(mgr.users, data)
    #     assert response.status_code == 201
    #     equal_schema(response.json(), response.schema)

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя с уже существующим login')
    def test_add_user_with_existing_login(self, immutable_role, user_group_roles, immutable_user):
        existing_login = immutable_user['login']
        data = {"$login": existing_login,
                "$fname": ukrainian.person.name(),
                "$lname": ukrainian.person.last_name(),
                "$userGroupRoles": user_group_roles,
                "$roleId": immutable_role['roleId']}
        response = send.post(mgr.users, data)
        expected_response = {'COMMON_ENTITY_WITH_SUCH_FIELD_EXISTS': 'Non-deleted user with such login already exists'}
        assert (response.status_code, response.json()) == (409, expected_response)

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя с существующими полями (кроме уникальных)')
    def test_add_user_with_existing_fields_which_are_not_unique(self, immutable_role, user_group_roles, immutable_user):
        existing_field = immutable_user
        data = {"$login": ukrainian.generic.company.login(),
                "$fname": existing_field['fname'],
                "$lname": existing_field['lname'],
                "$userGroupRoles": user_group_roles,
                "$roleId": immutable_role['roleId'],
                "$agentId": ukrainian.unique_name,
                "$ADlogin": existing_field['loginAD'],
                "$pname": existing_field['pname'],
                "$email": existing_field['email'],
                "$phone": str(random.randint(1111111, 999999999)),
                "$fax": existing_field['phone']
                }
        response = send.post(mgr.users, data)
        assert response.status_code == 201
        equal_schema(response.json(), response.schema)

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя с уже существующим phone')
    def test_add_user_with_existing_phone(self, immutable_role, user_group_roles, immutable_user):
        existing_phone = immutable_user['phone']
        data = {"$login": ukrainian.generic.company.login(),
                "$fname": ukrainian.person.name(),
                "$lname": ukrainian.person.last_name(),
                "$userGroupRoles": user_group_roles,
                "$roleId": immutable_role['roleId'],
                "$phone": existing_phone}
        response = send.post(mgr.users, data)
        expected_response = {'COMMON_EXCEPTION': 'Not deleted user with phone = %s already exist!' % existing_phone}
        assert (response.status_code, response.json()) == (500, expected_response)

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя с уже существующим agentId')
    def test_add_user_with_existing_agent_id(self, immutable_role, user_group_roles, immutable_user):
        existing_agent_id = immutable_user['agentId']
        data = {"$login": ukrainian.generic.company.login(),
                "$fname": ukrainian.person.name(),
                "$lname": ukrainian.person.last_name(),
                "$userGroupRoles": user_group_roles,
                "$roleId": immutable_role['roleId'],
                "$agentId": existing_agent_id}
        response = send.post(mgr.users, data)
        expected_response = {'COMMON_ENTITY_WITH_SUCH_FIELD_EXISTS': 'AGENT ID =%s already exists' % existing_agent_id}
        assert (response.status_code, response.json()) == (409, expected_response)

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя без login, fname, lname')
    def test_add_user_without_login_fname_lname(self, immutable_role, user_group_roles):
        data = {"$login": None,
                "$fname": None,
                "$lname": None,
                "$userGroupRoles": user_group_roles,
                "$roleId": immutable_role['roleId']}
        response = send.post(mgr.users, data)
        expected_response = {'ADM_VALIDATION_USER_LAST_NAME_LENGTH': 'Last name length from 1 to 256',
                             'ADM_VALIDATION_USER_FIRST_NAME_LENGTH': 'First name length from 1 to 256',
                             'ADM_VALIDATION_USER_LOGIN_LENGTH': 'Login length from 1 to 104'}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя без roleId')
    def test_add_user_without_role_id(self, user_group_roles):
        data = {"$login": ukrainian.generic.company.login(),
                "$fname": ukrainian.person.name(),
                "$lname": ukrainian.person.last_name(),
                "$userGroupRoles": user_group_roles,
                "$roleId": None}
        response = send.post(mgr.users, data)
        assert response.status_code == 201

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя без groupId')
    def test_add_user_without_group_id(self, immutable_role):
        data = {"$login": ukrainian.generic.company.login(),
                "$fname": ukrainian.person.name(),
                "$lname": ukrainian.person.last_name(),
                "$groupId": None,
                "$roleId": immutable_role['roleId']}
        response = send.post(mgr.users, data)
        assert response.status_code == 201

    @allure.feature('функциональный тест')
    @allure.story('Добавляем пользователя, указывая в user_group_roles роль, которой нет в roleId')
    @pytest.mark.xfail('нужно в end-to-end')
    def test_add_user_with_role_in_user_group_roles_which_not_exist_in_role_id(self, user_group_roles):
        data = {"$login": ukrainian.generic.company.login(),
                "$fname": ukrainian.person.name(),
                "$lname": ukrainian.person.last_name(),
                "$roleId": user_params.root_role_id,
                "$userGroupRoles": user_group_roles}
        response = send.post(mgr.users, data)
        expected_response = \
            {"ADM_VALIDATION_USER_NOT_ALLOWED_ROLE_IN_GROUP": f"Roles in groups by the following role ids not allowed: "
                                                              f"{user_group_roles[0]['roles'][0]['roleId']}"}
        assert (response.status_code, response.json()) == (400, expected_response)

    @allure.feature('функциональный тест')
    @allure.story('Получаем пользователя по userId')
    def test_get_user(self, immutable_user):
        response = send.get(mgr.users, id_to_url=immutable_user['userId'])
        assert (response.json()['userId'], response.status_code) == (immutable_user['userId'], 200)

    @allure.feature('функциональный тест')
    @allure.story('Получаем пользователя по неизвестному id')
    def test_get_user_with_unknown_id(self):
        unknown_user_id = ukrainian.uuid
        response = send.get(mgr.users, id_to_url=unknown_user_id)
        expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': 'USER not found by userId=%s' % unknown_user_id}
        assert (response.json(), response.status_code) == (expected_response, 400)

    # Нужно правильно добавить удаленного пользщователя
    # @allure.feature('функциональный тест')
    # @allure.story('Получаем удаленного пользователя по userId')
    # def test_get_deleted_user(self, immutable_deleted_user):
    #     response = send.get(mgr.users, id_to_url=immutable_deleted_user['userId'])
    #     assert (response.json(), response.status_code) == (immutable_deleted_user, 200)

    @allure.feature('функциональный тест')
    @allure.story('Удаляем пользователя по userId')
    def test_delete_user(self, user_without_roles_and_groups_on_roles):
        response = send.delete(mgr.users, id_to_url=user_without_roles_and_groups_on_roles['userId'])
        assert (response.json(), response.status_code) == (user_without_roles_and_groups_on_roles, 200)

    @allure.feature('функциональный тест')
    @allure.story('Удаляем пользователя по неизвестному userId')
    def test_delete_user_by_unknown_user_id(self):
        unknown_user_id = ukrainian.uuid
        response = send.delete(mgr.users, id_to_url=unknown_user_id)
        expected_response = {'COMMON_REQUESTED_RESOURCES_NOT_FOUND': 'USER not found by userId=%s' % unknown_user_id}
        assert (response.json(), response.status_code) == (expected_response, 400)

    @allure.feature('функциональный тест')
    @allure.story('Получаем disabled пользователя')
    def test_get_user_enabled_false(self, add_user_with_role):
        disabled_user = add_user_with_role(enabled=False)
        response = send.get(mgr.users, id_to_url=disabled_user['userId'])
        assert (response.json(), response.status_code) == (disabled_user, 200)

    @allure.feature('функциональный тест')
    @allure.story('Удаляем disabled пользователя')
    def test_delete_user_enabled_false(self, add_user_with_role):
        disabled_user = add_user_with_role(enabled=False)
        response = send.delete(mgr.users, id_to_url=disabled_user['userId'])
        assert (response.json(), response.status_code) == (disabled_user, 200)

    @allure.feature('функциональный тест')
    @allure.story('Редактируем пользователя')
    @pytest.mark.xfail(reason='https://helpdesk.company.com/issues/4137')
    @pytest.mark.parametrize('user_data', [ukrainian.manager.user(), russian.manager.user(), english.manager.user()])
    def test_edit_user(self, user_without_roles_and_groups_on_roles, user_data):
        user_id = user_without_roles_and_groups_on_roles['userId']
        user_data['$userId'] = user_id
        response = send.put(mgr.users, json=user_data, id_to_url=user_id)
        assert response.status_code == 200
        equal_schema(response.json(), response.schema)

    @allure.feature('функциональный тест')
    @allure.story('Создаем удаленного (deleted=true) пользователя со всеми полями, должен создатся не удаленный пользователь')
    def test_add_deleted_user(self, immutable_role):
        data = ukrainian.manager.user()
        data['$deleted'] = True
        response = send.post(mgr.users, data)
        assert response.status_code == 201
        assert response.json()['deleted'] is False

    @allure.feature('функциональный тест')
    @allure.story('Создаем пользователя с логином, телефоном ы емейлом, как у удаленного пользователя')
    @pytest.mark.xfail(reason='https://helpdesk.company.com/issues/4138')
    def test_add_user_with_email_phone_login_which_in_deleted_user(self, immutable_deleted_user):
        data = ukrainian.manager.user()
        data['$login'] = immutable_deleted_user['login']
        data['$phone'] = immutable_deleted_user['phone']
        data['$email'] = immutable_deleted_user['email']
        response = send.post(mgr.users, data)
        assert response.status_code == 200
        equal_schema(response.json(), response.schema)

    @allure.feature('функциональный тест')
    @allure.story('Восстанавдливаем disabled пользователя')
    @pytest.mark.skip(reason='Нужно создать удаленного пользователя (создать пользователя --> Сделать активность(звонок) --> Удалить пользователя')
    def test_recover_deleted_user(self, deleted_user):
        response = send.post(mgr.recover, id_to_url={"userId": deleted_user['userId']})
        assert response.status_code == 200
        assert response.json()['deleted'] is False
        assert response.json()['login'] == deleted_user['login']

    @allure.feature('функциональный тест')
    @allure.story('Проверка схемы ответа поиска пользователя по логину используя search')
    def test_search_user_by_login_check_schema(self, user_without_roles_and_groups_on_roles):
        data = {
            "$criteria_name": "userLogin",
            "$criteria_operator": "equal",
            "$criteria_values": user_without_roles_and_groups_on_roles['login']
        }
        response = send.post(mgr.users_search, data)
        assert response.status_code == 200
        equal_schema(response.json(), response.schema)

    @allure.feature('функциональный тест')
    @allure.story('Поиск пользователя по всем критериям пользователя используя search')
    @pytest.mark.parametrize("criteria_name, user_value", [("userLogin", "login"), ("userFirstName", "fname"),
                                                           ("userLastName", "lname"), ("userPatronymicName", "pname"),
                                                           ("userPhone", "phone"), ("userAgentId", "agentId"),
                                                           ("userLoginAd", "loginAD")])
    def test_search_user_by_criterias(self, user_without_roles_and_groups_on_roles, criteria_name, user_value):
        data = {
            "$criteria_name": criteria_name,
            "$criteria_operator": "equal",
            "$criteria_values": user_without_roles_and_groups_on_roles[user_value]
        }
        response = send.post(mgr.users_search, data)
        assert response.status_code == 200
        assert response.json()['data'][0][user_value] == user_without_roles_and_groups_on_roles[user_value]

    @allure.feature('функциональный тест')
    @allure.story('Поиск пользователя по групе и роли используя search')
    @pytest.mark.parametrize("criteria_name, user_value, id_param", [("userGroupId", "groups", "groupId"),
                                                                     ("userRoleId", "roles", "roleId")])
    def test_search_user_by_group_and_role(self, user_without_roles_and_groups_on_roles, criteria_name, user_value, id_param):
        data = {
            "$criteria_name": criteria_name,
            "$criteria_operator": "equal",
            "$criteria_values": user_without_roles_and_groups_on_roles[user_value][0][id_param]
        }
        response = send.post(mgr.users_search, data)
        assert response.status_code == 200
        assert response.json()['data'][0][user_value][0][id_param] == user_without_roles_and_groups_on_roles[user_value][0][id_param]

    # Нужно добалвять удаленного пользщователя
    # @allure.feature('функциональный тест')
    # @allure.story('Поиск удаленных пользователей')
    # @pytest.mark.xfail('Нужно сначала добавлять удаленного')
    # def test_search_deleted_users(self, immutable_deleted_user):
    #     data = {
    #         "$criteria_name": "userDeletedOnly",
    #         "$criteria_operator": "equal",
    #         "$criteria_values": True
    #     }
    #     response = send.post(mgr.users_search, data)
    #     assert response.status_code == 200
    #     assert immutable_deleted_user['login'] in [i['login'] for i in response.json()['data']]

    @allure.feature('функциональный тест')
    @allure.story('Проверка пагинации (переход на вторую страницу)')
    def test_search_pagination(self, user_without_roles_and_groups_on_roles):
        data = {
            "$criteria_name": "userDeletedOnly",
            "$criteria_operator": "equal",
            "$criteria_values": False,
            "$pageNumber": 2,
            "$pageSize": 1
        }
        response = send.post(mgr.users_search, data)
        assert response.status_code == 200
        assert response.json()['data']

    @allure.feature('функциональный тест')
    @allure.story('Проверка корректности работы pageSize')
    def test_search_correct_page_size(self, user_without_roles_and_groups_on_roles):
        data = {
            "$criteria_name": "userDeletedOnly",
            "$criteria_operator": "equal",
            "$criteria_values": False,
            "$pageNumber": 2,
            "$pageSize": 2
        }
        response = send.post(mgr.users_search, data)
        assert response.status_code == 200
        assert len(response.json()['data']) == 2

    @allure.feature('функциональный тест')
    @allure.story('Проверка пагинации - переход на страницу без данных')
    @pytest.mark.xfail(reason="https://helpdesk.company.com/issues/4139")
    def test_search_pagination_on_page_without_data(self, user_without_roles_and_groups_on_roles):
        data = {
            "$criteria_name": "userDeletedOnly",
            "$criteria_operator": "equal",
            "$criteria_values": False,
            "$pageNumber": 111,
            "$pageSize": 9999
        }
        response = send.post(mgr.users_search, data)
        assert response.status_code == 200
        assert response.json()['pagination']["pageNumber"] == 111
        assert response.json()['pagination']["pageSize"] == 9999
        assert len(response.json()['data']) == 0

    @allure.feature('Валидация')
    @allure.story('Проверка валиадции пагинации pageNumber, pageSize = 0')
    def test_search_pagination_zero_page_number_and_page_size(self, user_without_roles_and_groups_on_roles):
        data = {
            "$criteria_name": "userDeletedOnly",
            "$criteria_operator": "equal",
            "$criteria_values": False,
            "$pageNumber": 0,
            "$pageSize": 0
        }
        response = send.post(mgr.users_search, data)
        expected_response = {'FILTER_VALIDATION_PAGINATION_PAGE_NUMBER': "PAGINATION PAGE_NUMBER can't be "
                                                                         'less than 1',
                             'FILTER_VALIDATION_PAGINATION_PAGE_SIZE': "PAGINATION PAGE_SIZE can't be less "
                                                                       'than 1'}
        assert response.status_code == 400
        assert response.json() == expected_response

    @allure.feature('функциональный тест')
    @allure.story('Проверка корректности работы sorting')
    @pytest.mark.parametrize("sorted_column, order", [("login", "ASC"), ("lname", "DESC"), ('phone', 'ASC')])
    @pytest.mark.xfail(reason='Не работает сортировка по украинской букве "І"')
    def test_search_correct_sorting(self, create_10_users, sorted_column, order):
        data = {
            "$criteria_name": "userDeletedOnly",
            "$criteria_operator": "equal",
            "$criteria_values": False,
            "$order": order,
            "$sortedColumn": sorted_column
        }
        response = send.post(mgr.users_search, data)
        assert response.status_code == 200
        sorting_param_list = [(_[sorted_column] or '') for _ in response.json()['data']]
        assert sorting_param_list == sorted(sorting_param_list, reverse=False if order == "ASC" else True)

    @allure.feature('Валидация')
    @allure.story('Передаем не существующий order')
    def test_search_sorting_with_incorrect_order(self, user_without_roles_and_groups_on_roles):
        data = {
            "$criteria_name": "userDeletedOnly",
            "$criteria_operator": "equal",
            "$criteria_values": False,
            "$order": "blabla",
            "$sortedColumn": "login"
        }
        response = send.post(mgr.users_search, data)
        expected_response = {'FILTER_VALIDATION_SORTING_ORDER_UNKNOWN': 'SORTING ORDER is unknown'}
        assert response.status_code == 400
        assert response.json() == expected_response

    @allure.feature('Валидация')
    @allure.story('Передаем не существующий критерий сортировки')
    @pytest.mark.xfail(reason="https://helpdesk.company.com/issues/4140")
    def test_search_sorting_with_incorrect_criteria(self, user_without_roles_and_groups_on_roles):
        data = {
            "$criteria_name": "userDeletedOnly",
            "$criteria_operator": "equal",
            "$criteria_values": False,
            "$order": "ASC",
            "$sortedColumn": "unknown_criteria"
        }
        response = send.post(mgr.users_search, data)
        expected_response = {'FILTER_VALIDATION_SORTING_CRITERIA_UNKNOWN': "SORTING criteria doesn't supports"}
        assert response.status_code == 400
        assert response.json() == expected_response


#TODO: import_excel, import_from_AD, settings, end_to_end: Создать пользователя, сделать что то(звонки, чаты...), удалить,
# должен пометиться удалаенный