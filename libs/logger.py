import os
import json
import logging.config
from libs.Singleton import Singleton, singleton


@Singleton
class logger:

    def __init__(self, log_print=False):
        self.log = self.setup()
        self.log_stamp =log_print

    @staticmethod
    def setup():
        """Setup logging configuration

        """

        default_path = 'logging.json'
        default_level = logging.INFO
        env_key = 'LOG_CFG'

        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
        return logging.getLogger(__name__)

    @property
    def get_log(self):
        return self.log

    def log_print(self, string):
        if self.log_stamp is True:
            print(string)
