import re
import bin.defaults as const
from libs.Singleton import Singleton
from libs.fileio import fileio
from libs.jsonInterface import Regex, Language


@Singleton
class transl:

    def __init__(self, lang_name, input_lst, lang_config=const.LANG_CONFIG,
                 regex_config=const.REGEX_CONFIG, output_file=None):
        self.input_lst = input_lst
        self.output_file = output_file
        self.__lang_property = Language(lang_config).property(lang_name)
        self.__regex_property = Regex(regex_config).property(self.__lang_property['regex_config'])
        self.__open_comment = re.escape(self.__lang_property['open_comment'])
        self.__close_comment = re.escape(self.__lang_property['close_comment'])
        self.fio = fileio()

    def list_build(self):
        for file in self.input_lst:
            self.fio.file_name = self.fio.root_path(file)
            for line in self.fio.read_file_unsafe():
                if re.search(const.ID.format(self.__open_comment, self.__close_comment), line):
                    yield line

    def write_output(self):
        for line in self.list_build():
            try:
                type, value = re.split(const.ID.format(self.__open_comment, self.__close_comment), line)
                yield self.get_type(type), self.get_value(value)
            except Exception as e:
                print(e)
                continue

    def get_value(self, string):
        found = False
        for value_pattern in self.__regex_property['value_pattern']:
            value = value_pattern.format(self.__open_comment, self.__close_comment)
            if re.search(value, string):
                found = True
                string = re.search(value, string).group(1)
                break

        if not found:
            string = ''
        elif string.endswith(self.__regex_property['new_line']):
            string.replace(self.__regex_property['new_line'], '')

        return string.strip()

    def get_type(self, string):
        found = False
        for type_pattern in self.__regex_property['type_pattern']:
            if re.search(type_pattern, string):
                found = True
                string = re.search(type_pattern, string).group(1)
                break

        if not found:
            string = self.__regex_property['no_type']

        return string.strip()

    def string_openers(self):
        for string_opener in self.__lang_property['string-openers']:
            yield string_opener

    def set_lang(self, lang_name, lang_config=const.LANG_CONFIG,
                 regex_config=const.REGEX_CONFIG):
        self.__lang_property = Language(lang_config).property(lang_name)
        self.__regex_property = Regex(regex_config).property(self.__lang_property['regex_config'])
        self.__open_comment = re.escape(self.__lang_property['open_comment'])
        self.__close_comment = re.escape(self.__lang_property['close_comment'])

    def multi_language(self, lang_names, lang_config=const.LANG_CONFIG,
                       regex_config=const.REGEX_CONFIG):
        for lang_name in lang_names:
            self.set_lang(lang_name, lang_config, regex_config)
            yield self.write_output()
