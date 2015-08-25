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

__author__ = "Gabriel Araujo"
__copyright__ = "Copyright 2014"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Gabriel Araujo"

import os
import glob
import shutil
import re
import sys
import collections


def track_files(file_path, file_format):
    return glob.glob('{}/*.{}'.format(file_path, file_format))


def id_generator():
    i = 1
    while True:
        yield i
        i += 1


class Corpus:
    """Handle the organization and compilation of the speech corpus."""

    AUDIO_DIR = 'wav'
    METADATA_DIR = 'etc'

    TRAIN_SUFFIX = 'train'
    TEST_SUFFIX = 'test'

    FILEID_EXT = 'fileids'
    TRANSCRIPT_EXT = 'transcription'

    SPEAKER_ID = id_generator()
    AUDIO_ID = id_generator()

    def __init__(self, name, trg_path, src_path=None):
        self.name = name
        self.target_path = trg_path
        self.src = src_path
        # Initialization
        self.speakers = []
        self.suffix = self.trans_file = self.fileid_file = None

    @property
    def corpus_path(self):
        return os.path.join(self.target_path, self.name)

    def set_up(self):
        self.create_folder(Corpus.AUDIO_DIR)
        self.create_folder(Corpus.METADATA_DIR)
        trans_filename = self.format_filename(self.suffix, Corpus.TRANSCRIPT_EXT)
        self.trans_file = TranscriptionWriter(os.path.join(self.corpus_path, Corpus.METADATA_DIR, trans_filename))
        fileid_filename = self.format_filename(self.suffix, Corpus.FILEID_EXT)
        self.fileid_file = FileidWriter(os.path.join(self.corpus_path, Corpus.METADATA_DIR, fileid_filename))

    def create_folder(self, folder_path, absolute=False):
        full_path = folder_path if absolute else os.path.join(self.corpus_path, folder_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return full_path

    @staticmethod
    def format_speaker_id(spk_id):
        return '{:06}'.format(spk_id)

    @staticmethod
    def format_audio_id(spk_repr, audio_id):
        return '{}_{:03}'.format(spk_repr, audio_id)

    @staticmethod
    def _copy_audio(original_path, new_path):
        try:
            shutil.copy2(original_path, new_path)  # Copy audio file to the new location
        except IOError as e:
            print('I/O error(%s): %s %s' % (e.errno, e.strerror, e.filename))
            sys.exit(1)

    def format_filename(self, suffix, ext):
        return '{0}_{1}.{2}'.format(self.name, suffix, ext)

    def add_speaker(self, speaker):
        self.speakers.append(speaker)

    def _store_files(self):
        self.trans_file.store()
        self.fileid_file.store()

    def compile_corpus(self):
        for spk in self.speakers:
            spk_repr = str(spk)
            spk_dir_path = self.create_folder(os.path.join(Corpus.AUDIO_DIR, spk_repr))
            for audio_name, audio_ext, audio_old_path in spk.audios:
                if audio_name in spk.prompts:  # Has transcription?
                    audio_repr = Corpus.format_audio_id(spk_repr, next(Corpus.AUDIO_ID))
                    audio_new_path = os.path.join(spk_dir_path, '{}.{}'.format(audio_repr, audio_ext))
                    self._copy_audio(audio_old_path, audio_new_path)
                    # Include transcription
                    self.trans_file.add_content(spk.prompts[audio_name], audio_repr)
                    # Include file_id
                    self.fileid_file.add_content(spk_repr, audio_repr)
        self._store_files()


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
        with open(self.file, mode='a', encoding='iso-8859-1') as file:
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


class Speaker:
    """Handle the tasks strictly related to speakers entities.
    """

    def __init__(self, id_number, name):
        self._id = id_number
        self.name = name
        self.metadata = self.prompts = self.audios = None

    def __str__(self):
        return Corpus.format_speaker_id(self._id)


class SpeakerBuilder:
    def __init__(self, _id, name, source_path=None):
        self._speaker = Speaker(_id, name)
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


class Prompts(collections.UserDict):
    PROMPT_PATTERN = r"(?P<id>^\d+).?[ ]+(?P<prompt>\S+( \S+)*)"

    def _populate_from_file(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                m = re.search(self.PROMPT_PATTERN, line)
                if m:
                    self.data[m.group('id')] = m.group('prompt').lower()

    def _populate_from_files(self, file_path, ext):
        for trans_file in track_files(file_path, ext):
            with open(trans_file, mode='r', encoding='utf-8') as f:
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
        audios_files = track_files(audios_path, audios_format)
        for file_path in audios_files:
            filename, file_extension = os.path.splitext(os.path.basename(file_path))
            self.data.append((filename, file_extension[1:], file_path))


class Metadata(collections.UserDict):
    DATA_PATTERNS = [
        ('USERNAME', r'(?<=User Name:).*(?=\n)'),
        ('GENDER', r'(?<=Gender:).*(?=\n)'),
        ('AGE', r'(?<=Age Range:).*(?=\n)'),
        ('LANGUAGE', r'(?<=Language:).*(?=\n)')
    ]
    GLOBAL_PATTERN = '|'.join('(?P<%s>%s)' % pair for pair in DATA_PATTERNS)
    REGEX = re.compile(GLOBAL_PATTERN)

    def populate(self, file_path, regex=REGEX):
        with open(file_path, mode='r', encoding='utf-8') as f:
            content_file = f.read()
            for m in regex.finditer(content_file):
                self.data[m.lastgroup] = m.group(m.lastgroup).strip()
