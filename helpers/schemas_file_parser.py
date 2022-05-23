import json
import sys
import re
from os import path
from json.decoder import JSONDecodeError
from definition import SCHEMAS_DIR, SQL_DIR


class Parser:

    def replace_on(self, url=None, method=None, data=None, is_sql=False, sql_name=None):
        if is_sql:
            sql_data = self._exec_json_file(file_path=self._path_to_sql(sql_name))
            return self._replace_sql(sql_data, data)
        json_data = self._exec_json_file(file_path=self._path_to_json(url, method))
        return self._replace_json(json_data, data)

    @staticmethod
    def _path_to_json(url, method_name):
        file_name = method_name.lower() + "_" + url.path.split('.')[1] + ".json"
        schema_abs_path = path.join(url.path.split('.')[0], file_name)
        schema_full_path = path.join(SCHEMAS_DIR, schema_abs_path)
        return schema_full_path

    @staticmethod
    def _path_to_sql(name):
        return path.join(SQL_DIR, f"{name}.sql")

    @staticmethod
    def _exec_json_file(file_path):
        try:
            with open(file_path, encoding="utf8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"FileNotFound by path {file_path}")
            return str({"request": {}, "schema": {}})

    @staticmethod
    def _replace_default_values(json_file):
        def nested_replace(data, schema=None):
            for key, val in data.items():
                if isinstance(val, dict) and ("default", "value") == tuple(val.keys()):
                    if isinstance(val['value'], str):
                        if val['value'].startswith('$'):
                            data[key] = val['default']
                            try:
                                schema[key]["allowed"] = [val['default']]
                            except TypeError:
                                print(f'Возможно не добавлен "allowed" для {key} в схеме')
                                raise
                        else:
                            data[key] = val['value']
                    else:
                        data[key] = val['value']
                elif isinstance(val, dict):
                    try:
                        nested_replace(val, schema[key]['schema'])
                    except KeyError:
                        continue
                elif isinstance(val, list):
                    for i in val:
                        if isinstance(i, dict):
                            try:
                                nested_replace(i, schema[key]['schema']['schema'])
                            except KeyError:
                                continue
            return {"request": data, "schema": schema}
        try:
            json_data = json.loads(json_file)
        except JSONDecodeError:
            print("Schema is not correct, fix it")
            sys.exit(1)
        if isinstance(json_data['request'], list):
            result = {"request": [], "schema": {}}
            obj = nested_replace(json_data['request'][0], json_data['schema'])
            result['request'].append(obj['request'])
            result['schema'] = obj['schema']
        else:
            result = nested_replace(json_data['request'], json_data['schema'])
        result = json.loads(re.sub(r'(\"\$[\w]+\")', 'null', json.dumps(result)))
        return result

    def _replace_json(self, json_data, data):
        if data:
            for key, val in iter(data.items()):
                if key.startswith("$"):
                    if isinstance(val, str):
                        val = val.replace('"', "").replace("'", "")
                    elif isinstance(val, (int, dict, list)):
                        key = '"%s"' % key
                        val = str(val)
                    elif val is None:
                        key = '"%s"' % key
                        val = "null"
                    json_data = json_data.replace(key, val)
        json_data = json_data.replace("'", '"').replace("False", 'false').replace("True", 'true')
        return self._replace_default_values(json_data)

    @staticmethod
    def _replace_sql(sql_data, data):
        for key, val in iter(data.items()):
            if isinstance(val, str):
                val = f"'{val}'"
            if isinstance(val, int):
                val = str(val)
            elif val is None:
                val = "null"
            sql_data = sql_data.replace(key, val)
        return sql_data


params_replacer = Parser()

