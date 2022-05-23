# -*- coding: utf-8 -*-

import os
import json
import logging.config
from getpass import getuser
from definition import DEFAULT_PATH_TO_CONFIG_FOLDER, DEFAULT_PATH_TO_LOGGING_JSON, DEFAULT_PATH_TO_LOGS_FOLDER


class Logger:
    """
    Displays and writes to log file in different formats
    """

    def __new__(cls, path_to_logging_json=DEFAULT_PATH_TO_LOGGING_JSON, path_to_logs_folder=DEFAULT_PATH_TO_LOGS_FOLDER,
                default_level=logging.DEBUG):
        return cls.setup_logging(path_to_logging_json, path_to_logs_folder, default_level)

    @classmethod
    def setup_logging(cls, path_to_logging_json, path_to_logs_folder, default_level):
        """
        Setup logging configuration
        :param path_to_logging_json: default path to logging.json configuration file
        :param path_to_logs_folder: default path to folder with log files
        :param default_level: default level of logging
        :return: logging object
        """
        cls.create_log_folder(path_to_logs_folder)

        if os.path.exists(path_to_logging_json):
            with open(path_to_logging_json, 'rt') as f:
                config = json.load(f)
                cls.add_path_to_logs_folder_to_log_filenames_from_json_config(config, path_to_logs_folder)
            logging.config.dictConfig(config)
            logging.debug(f'JSON CONFIG defined: {path_to_logging_json} path to logs folder: {path_to_logs_folder}')
        else:
            logging.basicConfig(level=default_level)
            logging.debug('BASIC CONFIG')
        return logging.getLogger(getuser())

    @classmethod
    def create_log_folder(cls, path_to_logs_folder):
        """
        creates folder to write logs, if it doesn't exist
        :return: nothing to return
        """
        if not os.path.exists(path_to_logs_folder):
            os.makedirs(path_to_logs_folder)

    @classmethod
    def add_path_to_logs_folder_to_log_filenames_from_json_config(cls, config, path_to_logs_folder):
        """
        adds DEFAULT_PATH_TO_LOGS_FOLDER to all handlers, which have "filename" key
        :param config: data as dict from logging.json configuration file
        :param path_to_logs_folder: default path to folder with log files
        :return: modified config dictionary
        """
        for handler in config['handlers']:
            filename = config['handlers'][handler].get('filename')
            if filename:
                full_path_to_log_file = os.path.join(path_to_logs_folder, config['handlers'][handler].get('filename'))
                config['handlers'][handler]['filename'] = full_path_to_log_file


logger = Logger()
