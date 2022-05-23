import os
import sys
from configparser import ConfigParser
from definition import PROJECT_CONFIG


class ProjectConfig:
    ENVIRONMENT_KEYS = ['QA_SERVER_host', 'QA_DB_host', 'QA_DB_username', 'QA_DB_password', ]

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(PROJECT_CONFIG)
        self.set_config_variables()

    def get_environ_items(self):
        try:
            environ_params = {key: os.environ[key] for key in self.ENVIRONMENT_KEYS}
        except KeyError:
            sys.exit(f"Can't find  some of {self.ENVIRONMENT_KEYS} in environment variables")
        return environ_params

    def set_config_variables(self):
        param = self.get_environ_items()
        for key, val in param.items():
            self.config[key.split('_')[1]][key.split('_')[2]] = val

    @property
    def host(self):
        return self.config['SERVER']['host']

    @property
    def credentials(self):
        return self.config['CREDENTIALS']

    @property
    def database(self):
        return self.config['DB']


cfg = ProjectConfig()

