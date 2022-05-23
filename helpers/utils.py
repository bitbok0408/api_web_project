import re
import openpyxl
from os.path import join as path_join
from config.project_config import cfg
from urllib.parse import urljoin
from datetime import datetime, date
from definition import TEMP_DATA


def get_url(url, id_to_replace=None):
    """
    Добавляет http к URL, так же добавляет ID в конец, если тип str
    :param url: str
    :param id_to_replace: dict {"userId": "1234-qwee-asd-123e"} or str
    :return: example: http://10.100.90.14:8080/Module/1234-qwer-3456-asdf/user
    """
    host = cfg.host
    url_with_host = urljoin(host, str(url))
    if id_to_replace:
        if isinstance(id_to_replace, str):
            if "$" in url_with_host:
                url_with_host = re.sub(r'(\$[\w]+)', id_to_replace, url_with_host)
            else:
                url_with_host = urljoin(url_with_host + "/", id_to_replace)

        else:
            for i in id_to_replace:
                url_with_host = url_with_host.replace(f"${i}", id_to_replace[i])
    url_with_host = re.sub(r'(\/\$[\w]+)$', '', url_with_host)
    return url_with_host


def make_user_group_roles(group_roles_obj):
    """
    :param group_roles_obj: {'groupId': roleId} :type roleId: str or list
    :return: [{'group': {'groupId': str}, 'roles': [{'roleId': str}], 'applyRolesRecursively': False}]
    """
    user_group_roles = list()
    for i in group_roles_obj:
        result = dict()
        result['group'] = {"groupId": i}
        if isinstance(group_roles_obj[i], list):
            roles = [{'roleId': groupId} for groupId in group_roles_obj[i]]
        else:
            roles = [{'roleId': group_roles_obj[i]}]
        result['roles'] = roles
        result["applyRolesRecursively"] = False
        user_group_roles.append(result)
    return user_group_roles


def get_search_param(json_obg: dict, param: str):
    nesting = param.split('.')
    for i in nesting:
        json_obg = json_obg.get(i)
    return json_obg


def get_now_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_today_midnight_datetime():
    return datetime.combine(date.today(), datetime.min.time()).strftime("%d.%m.%Y %H:%M")


def get_today_start_datetime():
    return datetime.combine(date.today(), datetime.max.time()).strftime("%d.%m.%Y %H:%M")


def convert_timestamp(timestamp_ms):
    """
    :param timestamp_ms: timestamp in milliseconds
    :return: FE filter date format (
    """
    return datetime.fromtimestamp(timestamp_ms//1000).strftime("%d/%m/%Y %H:%M:%S")


def get_data_from_xls_file(file_name, cells):
    sheet = open_xls_file(file_name)
    cells_values = {cell: sheet[cell].value for cell in cells}
    return cells_values


def open_xls_file(file_name):
    if '.xls' not in file_name:
        file_name = f"{file_name}.xlsx"
    wb_obj = openpyxl.load_workbook(path_join(TEMP_DATA, file_name))
    return wb_obj.active


def data_row_count_in_xls_file(file_name):
    sheet = open_xls_file(file_name)
    count = 0
    for i in sheet.values:
        if i.count(None) < len(i):
            count += 1
    return count
