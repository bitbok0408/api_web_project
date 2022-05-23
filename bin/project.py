import inspect
import json

from bin.sql_client import sql_session
from bin.api_client import Session
from bin.cleaner import Cleaner
from helpers.utils import get_url
from helpers.schemas_file_parser import params_replacer
from bin.logger import logger
from pprint import pformat


class Project:

    def __init__(self):
        self.logger = logger
        self.session = Session()
        self.cleaner = Cleaner()
        self.json_params_replacer = params_replacer
        self.sql_client = sql_session

    def _send(self, method, url, id_to_url, schema=True, **kwargs):
        if method in ("GET", "DELETE"):
            default_json = {}
            request_response = self.json_params_replacer.replace_on(url=url, method=method, data=default_json)
        elif not schema:
            request_response = {"request": kwargs['json'], "schema": {}}
        else:
            request_response = self.json_params_replacer.replace_on(url=url, method=method, data=kwargs['json'])
            kwargs['json'] = request_response['request']
        url = get_url(url, id_to_url)
        response = self.session.send_request(method, url, **kwargs)
        call_method_name = inspect.stack()[2][3]
        if response.request.body:
            request_body = json.loads(response.request.body)
        else:
            request_body = None
        if str(call_method_name).startswith("test"):
            step = f"TEST_STEP - {call_method_name}"
            expected_schema = pformat(request_response['schema'])
            self.logger.error(f"{step}\n"
                              f"{method} {url}\n "
                              f"***Request_headers*** = {response.request.headers}\n"
                              f"***Request_body***:\n {pformat(request_body)},\n"
                              f"***Response_status code*** =  {response.status_code},\n "
                              f"***Response_body**:\n {pformat(response.json())}")
            self.logger.debug(f"***Expected_schema_response*** :\n {expected_schema}")
        else:
            step = f"PRE/POST CONDITION STEP - {call_method_name}"
            expected_schema = "Doest need for not Test method"
            self.logger.error(f"{step}\n"
                              f"{method} {url}\n "
                              f"***Request_headers*** = {response.request.headers}\n"
                              f"***Request_body*** = {pformat(request_body)},\n"
                              f"***Response_status code*** =  {response.status_code},\n "
                              f"***Response_body**:\n {pformat(response.json())}")
            self.logger.debug(f"***Expected_schema_response*** :\n {expected_schema}")

        response.schema = request_response['schema']
        return response

    def post(self, url, json=None, id_to_url=None, **kwargs):

        response = self._send(method="POST", url=url, id_to_url=id_to_url, json=json, verify=False, **kwargs)
        self.cleaner.add(get_url(url), response)
        return response

    def get(self, url, id_to_url=None, **kwargs):
        return self._send(method="GET", url=url, id_to_url=id_to_url, verify=False, **kwargs)

    def put(self, url, json=None, id_to_url=None, **kwargs):
        return self._send(method="PUT", url=url, id_to_url=id_to_url, json=json, verify=False, **kwargs)

    def patch(self, url, json=None, id_to_url=None, **kwargs):
        return self._send(method="PATCH", url=url, id_to_url=id_to_url, json=json, **kwargs)

    def delete(self, url, id_to_url=None, **kwargs):
        response = self._send(method="DELETE", url=url, id_to_url=id_to_url, verify=False, **kwargs)
        if response.status_code == 200:
            self.cleaner.remove(get_url(url), id_to_url)
        return response

    def sql(self, sql_name, data):
        query = params_replacer.replace_on(sql_name=sql_name, data=data, is_sql=True)
        self.sql_client.send(query)


send = Project()
