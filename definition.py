import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
DATA_DIR = os.path.join(ROOT_DIR, "Data")
SQL_DIR = os.path.join(DATA_DIR, "sql")
SCHEMAS_DIR = os.path.join(DATA_DIR, "schemas")
HELPERS_DIR = os.path.join(ROOT_DIR, "helpers")

SETTINGS = os.path.join(CONFIG_DIR, "settings.json")
PROJECT_CONFIG = os.path.join(CONFIG_DIR, "project.cfg")
VALIDATOR = os.path.join(HELPERS_DIR, "validator.py")

DEFAULT_PATH_TO_LOGS_FOLDER = os.path.join(ROOT_DIR, 'logs')
DEFAULT_PATH_TO_CONFIG_FOLDER = os.path.join(ROOT_DIR, 'config')
DEFAULT_PATH_TO_LOGGING_JSON = os.path.join(DEFAULT_PATH_TO_CONFIG_FOLDER, 'logging.json')
TEMP_DATA = os.path.join(DATA_DIR, 'temp')
