import codecs
import json
from abc import ABCMeta, abstractmethod

from libs.Singleton import singleton
from libs.fileio import fileio


class Interface(singleton):
    __metaclass__ = ABCMeta

    def __init__(self, filename):
        fileio().file_name = fileio().root_path(filename)
        self.data = json.load(fileio().read_file_unsafe())

    @abstractmethod
    def property(self, parameter):
        raise NotImplementedError("Must override property")


class Language(Interface):
    __metaclass__ = ABCMeta

    def property(self, langname):
        for lang in self.data['language']:
            if lang['name'].lower() == langname.lower():
                return {
                    "name": str(lang['name']),
                    "open_comment": str(lang['open_comment']),
                    "close_comment": str(lang['close_comment']),
                    "semicolon": bool(lang['semicolon']),
                    "datatype": bool(lang['datatype']),
                    "regex_config": str(lang['regex_config'])
                }


class Regex(Interface):
    __metaclass__ = ABCMeta

    def property(self, propname):
        for prop in self.data['regex_group']:
            if prop['name'].lower() == propname.lower():
                return {
                    "name": str(prop['name']),
                    "type_pattern": prop['type_pattern'],
                    "value_pattern": prop['value_pattern'].replace('"', "'"),
                    "no_type": str(prop['no_type']),
                    "new_line": str(prop['new_line'])
                }
