# -*- coding: utf-8 -*-

# Copyright (C) 2014  Gabriel F. Araujo

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import glob
import re


def track_files(file_path, file_format):
    return glob.glob('{}/*.{}'.format(file_path, file_format))


class FileWriter:
    FORMAT = '{0}'

    def __init__(self, file_path):
        self.file = file_path
        self.content = []

    @classmethod
    def format_content(cls, args):
        return cls.FORMAT.format(*args)

    def add_content(self, *args):
        formatted_content = self.format_content(args)
        self.content.append(formatted_content)

    def store(self):
        with open(self.file, mode='a', encoding='utf-8') as file:
            for line in self.content:
                file.write(line + '\n')


class TranscriptionWriter(FileWriter):
    FORMAT = '<s> {0} </s> ({1})'  # Prompt / Audio representation
    trans_regex = re.compile('\S*[,.?!]+\S*')

    def __init__(self, target_file):
        super().__init__(target_file)

    def add_content(self, *args):
        filtered_trans = TranscriptionWriter.trans_regex.sub(' ', args[0])
        super().add_content(filtered_trans, *args[1:])


class FileidWriter(FileWriter):
    FORMAT = '{0}/{1}'  # Speaker representation / Audio representation

    def __init__(self, target_file):
        super().__init__(target_file)
