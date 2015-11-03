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
import io
import shutil


def track_files(file_path, file_format):
    return glob.glob('{}/*.{}'.format(file_path, file_format))


def transcription_formatter(*args):
    return '<s> {0} </s> ({1})'.format(re.sub('\S*[,.?!]+\S*', ' ', args[0]), *args[1:])


class FileWriter(object):
    def __init__(self, file_path, format_func='{0}'.format):
        self.file = file_path
        self.format_line = format_func
        self.content = io.StringIO()

    def add_content(self, *args):
        formatted_content = self.format_line(*args)
        self.content.write(formatted_content + '\n')

    def store(self):
        with open(self.file, mode='w', encoding='utf-8') as file:
            self.content.seek(0)
            shutil.copyfileobj(self.content, file)
        self.content.close()


class TranscriptionWriter(FileWriter):

    def __init__(self, target_file):
        super(TranscriptionWriter, self).__init__(target_file, transcription_formatter)


class FileidWriter(FileWriter):

    def __init__(self, target_file):
        super(FileidWriter, self).__init__(target_file, '{0}/{1}'.format)
