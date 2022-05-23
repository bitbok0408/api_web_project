import pymysql as db
import os, re
from config.project_config import cfg


class SqlClient:

    def __init__(self):
        self._parse_cfg_params()
        self.connection = self._connection()

    def __del__(self):
        self.connection.close()

    def _connection(self):
        return db.connect(host=self.host, db=self.schema, user=cfg.database['username'],
                          password=cfg.database['password'], cursorclass=db.cursors.DictCursor)

    def _parse_cfg_params(self):
        host_with_port = cfg.database['host'].split("/")[2]
        self.host = host_with_port.split(':')[0]
        self.schema = cfg.database['host'].split("/")[3]

    @staticmethod
    def _exec_sql_file(cursor, sql_file):
        # print("\n[INFO] Executing SQL script file: '%s'" % (sql_file))
        statement = ""

        for line in sql_file:
            if re.match(r'--', line):  # ignore sql comment lines
                continue
            if not re.search(r';$', line):  # keep appending lines that don't end in ';'
                statement = statement + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement = statement + line
                cursor.execute(statement)

                statement = ""

    def send(self, query):
        with self.connection.cursor() as cursor:
            print(query)
            cursor.execute(query)
            self.connection.commit()


sql_session = SqlClient()



