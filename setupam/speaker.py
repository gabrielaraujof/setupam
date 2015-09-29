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

import collections
import glob
import os
import re
import logging

import chardet.universaldetector

import setupam.io


class Speaker:
    """Handle the tasks strictly related to speakers entities.
    """

    def __init__(self, name):
        self.name = name
        self.metadata = self.prompts = self.audios = None


class SpeakerBuilder:
    def __init__(self, name, source_path=None):
        self._speaker = Speaker(name)
        self.relative_path = source_path

    @property
    def speaker(self):
        return self._speaker

    def set_audios(self, *args, **kwargs):
        path_list = args
        audio_format = kwargs.get('audio_format', 'wav')
        if self.relative_path:
            path_list = [os.path.join(self.relative_path, p) for p in path_list]
            path_list.append(os.path.join(self.relative_path, 'wav'))
            path_list.append(self.relative_path)
        if not path_list:
            raise TypeError("Missing the path list of audios' directory.")
        for audios_path in path_list:
            if len(glob.glob(os.path.join(audios_path, '*.{}'.format(audio_format)))) > 0:
                audios_list = Audios()
                audios_list.populate(audios_path, audio_format)
                self.speaker.audios = audios_list
                break
        else:
            raise ValueError('Given an invalid path list given.')

    def set_prompts(self, *args, **kwargs):
        single_path_list = args
        multi_path = kwargs.get('multi')
        if self.relative_path:
            single_path_list = [os.path.join(self.relative_path, p) for p in single_path_list]
            single_path_list.append(os.path.join(self.relative_path, 'etc', 'prompts-original'))
            single_path_list.append(os.path.join(self.relative_path, '{}.txt'.format(self.speaker.name)))
            multi_path = os.path.join(self.relative_path, multi_path) if multi_path else self.relative_path
        if not (single_path_list or multi_path):
            raise TypeError('Missing arguments. Must have at least a path for multi files.')
        else:
            prompts = Prompts()
            if not multi_path:
                prompts.populate(*single_path_list)
            else:
                prompts.populate(*single_path_list, multi_path=multi_path)
        self.speaker.prompts = prompts

    def set_metadata(self, **kwargs):
        full_path = kwargs.get('full_path')
        if self.relative_path:
            if full_path:
                full_path = os.path.join(self.relative_path, full_path)
            else:
                full_path = os.path.join(self.relative_path, 'etc', 'README')
        if full_path:
            metadata = Metadata()
            if 'regex' in kwargs:
                metadata.populate(full_path, kwargs['regex'])
            else:
                metadata.populate(full_path)
            self.speaker.metadata = metadata
        else:
            raise TypeError('Missing the file path.')


class SpeakerFileReader:
    @staticmethod
    def _get_encoding(filename):
        detector = chardet.universaldetector.UniversalDetector()
        for line in open(filename, 'rb'):
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        logging.debug('Enconding detected for {} file: {} (confidence level: {:.2f})'.format(
            os.path.basename(filename),
            detector.result['encoding'],
            detector.result['confidence'])
        )
        if detector.result['confidence'] > .8:
            return detector.result['encoding']
        else:
            return 'utf-8'


class Prompts(SpeakerFileReader, collections.UserDict):
    PROMPT_PATTERN = r"(?P<id>^\d+).?[ ]+(?P<prompt>\S+( \S+)*)"

    def _populate_from_file(self, file_path):
        with open(file_path, mode='r', encoding=self._get_encoding(file_path)) as f:
            for line in f.readlines():
                m = re.search(self.PROMPT_PATTERN, line)
                if m:
                    self.data[m.group('id')] = m.group('prompt').lower()

    def _populate_from_files(self, file_path, ext):
        for trans_file in setupam.io.track_files(file_path, ext):
            with open(trans_file, mode='r', encoding=self._get_encoding(trans_file)) as f:
                first_line = f.readline().strip()
                if first_line.strip():
                    self.data[os.path.splitext(os.path.basename(trans_file))[0]] = first_line.lower()

    def populate(self, *args, **kwargs):
        for file_path in args:
            if os.path.exists(file_path):
                self._populate_from_file(file_path)
        else:
            return self._populate_from_files(kwargs['multi_path'], kwargs.get('ext', 'txt'))


class Audios(collections.UserList):
    def populate(self, audios_path, audios_format):
        audios_files = setupam.io.track_files(audios_path, audios_format)
        for file_path in audios_files:
            filename, file_extension = os.path.splitext(os.path.basename(file_path))
            self.data.append((filename, file_extension[1:], file_path))


class Metadata(SpeakerFileReader, collections.UserDict):
    DATA_PATTERNS = [
        ('USERNAME', r'(?<=User Name:).*(?=\n)'),
        ('GENDER', r'(?<=Gender:).*(?=\n)'),
        ('AGE', r'(?<=Age Range:).*(?=\n)'),
        ('LANGUAGE', r'(?<=Language:).*(?=\n)')
    ]
    GLOBAL_PATTERN = '|'.join('(?P<%s>%s)' % pair for pair in DATA_PATTERNS)
    REGEX = re.compile(GLOBAL_PATTERN)

    def populate(self, file_path, regex=REGEX):
        with open(file_path, mode='r', encoding=self._get_encoding(file_path)) as f:
            content_file = f.read()
            for m in regex.finditer(content_file):
                self.data[m.lastgroup] = m.group(m.lastgroup).strip()
