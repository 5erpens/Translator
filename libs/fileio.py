import os
from sys import platform as _platform
# noinspection PyCompatibility
from pathlib import Path, PureWindowsPath
from libs.Singleton import Singleton


@Singleton
class fileio:

    def __init__(self, File_Name=None):
        self.file_name = File_Name

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, file_name):
        self.__file_name = file_name

    def read_lines(self):
        file = self.read_file()
        for line in file:
            yield line
        file.close()

    def write_file(self, input):
        text_file = open(self.file_name, "a")
        text_file.write(input)
        text_file.close()

    def write_overwrite(self, input):
        text_file = open(self.file_name, "a")
        text_file.write(input)
        text_file.close()

    def file_flush(self):
        open(self.file_name, "w").close()

    def read_file(self):
        file = open(self.file_name, 'r')
        yield file
        file.close()

    def read_file_unsafe(self):
        return open(self.file_name, 'r')

    def create_folder(self, name, sub_directory):
        if sub_directory is not None:
            directory_list = [self.file_name, sub_directory, "/", name]
            directory = "".join(directory_list)
            if not os.path.exists(self.path(directory_list)):
                os.makedirs(directory)
        else:
            directory_list = [self.file_name, "", "/", name]
            directory = "".join(directory_list)
            if not os.path.exists(self.path(directory_list)):
                os.makedirs(directory)

        return self.path(directory + "/")

    @staticmethod
    def path(string):
        if _platform == "win32" or _platform == "win64":
            return str(PureWindowsPath(string))
        else:
            return string

    def root_path(self, string):
        rootdir = os.getcwd().split("Translator")
        return rootdir[0] + "Translator" + self.path(string)
