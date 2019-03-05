import json
from abc import ABCMeta, abstractmethod
from libs.Singleton import singleton
from libs.fileio import fileio


class Interface(singleton):
    __metaclass__ = ABCMeta

    def __init__(self, filename):
        fileio().file_name = fileio().root_path(filename)
        self.data = json.load(fileio().read_file_unsafe())

    def print_json_file(self):
        return json.dumps(self.data, indent=2)

    @abstractmethod
    def property(self, parameter):
        raise NotImplementedError("Must override property")

    @abstractmethod
    def get_all(self):
        raise NotImplementedError("Must override property")


class Language(Interface):
    __metaclass__ = ABCMeta

    def property(self, lang_name):
        for lang in self.data['language']:
            if lang['name'].lower() == lang_name.lower():
                return {
                    "name": lang['name'],
                    "open_comment": lang['open_comment'],
                    "close_comment": lang['close_comment'],
                    "semicolon": bool(lang['semicolon']),
                    "datatype": bool(lang['datatype']),
                    "regex_config": lang['regex_config']
                }

    def get_all(self):
        for lang in self.data['language']:
            yield lang['name']


class Regex(Interface):
    __metaclass__ = ABCMeta

    def property(self, prop_name):
        for prop in self.data['regex_group']:
            if prop['name'].lower() == prop_name.lower():
                return {
                    "name": prop['name'],
                    "type_pattern": [obj.replace('"', "'") for obj in prop['type_pattern']],
                    "value_pattern": [obj.replace('"', "'") for obj in prop['value_pattern']],
                    "no_type": prop['no_type'],
                    "new_line": prop['new_line']
                }

    def get_all(self):
        for regex in self.data['regex_group']:
            yield regex['name']
