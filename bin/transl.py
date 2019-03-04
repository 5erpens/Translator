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
        Type_pattern = self.__regex_property['type_pattern']
        Value_pattern = self.__regex_property['value_pattern'].format(self.__open_comment, self.__close_comment)
        new_line = self.__regex_property['new_line']
        for line in self.list_build():
            try:
                x, y = re.split(const.ID.format(self.__open_comment, self.__close_comment), line)
                y = re.search(Value_pattern, y).group(1)
                if y.endswith(new_line):
                    y, z = y.split(new_line)
                if re.search(Type_pattern, x):
                    x = re.search(Type_pattern, x).group(1)
                else:
                    x = const.NO_TYPE
                yield x, y

            except Exception as e:
                print(e)
                continue

