#!/usr/bin/env python3

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

from os import path, makedirs
import glob
from shutil import copy2
import re
import sys
from collections import UserDict, UserList


def track_files(file_path, file_format):
    return glob.glob('{}/*.{}'.format(file_path, file_format)).sort()


class Corpus:
    """Handle the organization and compilation of the speech corpus."""

    AUDIO_DIR = 'wav'
    METADATA_DIR = 'etc'

    FILEID_EXT = 'fileids'
    TRANSC_EXT = 'transcription'

    speaker_counter = 0
    audio_counter = 0

    def __init__(self, name, suffix, source_path, target_path, audio_fmt='wav'):
        self.name = name
        self.suffix = suffix
        self.speakers = []
        self.src = source_path
        self.base_path = target_path
        self.corpus_path = path.join(self.base_path, self.name)
        self.audio_format = audio_fmt

    @staticmethod
    def format_speaker_id(spk_id):
        return '{:06}'.format(spk_id)

    @staticmethod
    def format_audio_id(spk_id, audio_id):
        return '{}_{:03}'.format(Corpus.format_speaker_id(spk_id), audio_id)

    def format_filename(self, ext):
        return '{0}_{1}.{2}'.format(self.name, self.suffix, ext)

    def set_up(self):
        assert not path.exists(self.corpus_path)
        self.create_folder(Corpus.AUDIO_DIR)
        self.create_folder(Corpus.METADATA_DIR)
        trans_filename = self.format_filename(Corpus.TRANSC_EXT)
        self.trans_file = TranscriptionWriter(path.join(self.corpus_path, Corpus.METADATA_DIR, trans_filename))
        fileid_filename = self.format_filename(Corpus.FILEID_EXT)
        self.fileid_file = FileidWriter(path.join(self.corpus_path, Corpus.METADATA_DIR, fileid_filename))

    def add_speaker(self, speaker):
        assert isinstance(speaker, Speaker)
        self.speakers.append(speaker)

    def create_speaker(self, source_path):
        assert isinstance(source_path, str)
        speaker = Speaker(source_path)
        self.speakers.append(speaker)

    def compile(self):
        audio_ref = 0
        for spk_id, spk in enumerate(self.speakers, start=1):
            spk_repr = Corpus.format_speaker_id(spk_id)
            target_path = self.create_folder(spk_repr)
            trans = spk.gather_transcription()
            for audio in spk.gather_audios(audio_format=self.audio_format):
                audio_name = path.splitext(path.basename(audio))[0]
                if audio_name in trans:  # Has transcription?
                    audio_repr = Corpus.format_audio_id(spk_id, audio_ref)
                    new_filename = path.join(target_path, '{}.{}'.format(audio_repr, self.audio_format))
                    try:
                        copy2(audio, new_filename)
                        self.trans_file.add_content(trans[audio_name].lower())
                        self.fileid_file.add_content(spk_repr, audio_repr)
                        audio_ref += 1
                    except IOError as e:
                        print('I/O error(%s): %s %s' % (e.errno, e.strerror, e.filename))
                        sys.exit(1)

    # def process_audio(self, audio_file, trans):
    #    # TODO copiar audio
    #    # TODO adicionar transc
    #    # TODO adicionar fileid
    #    pass

    def store_files(self):
        self.trans_file.store()
        self.fileid_file.store()

    def create_folder(self, folder_path, absolute=False):
        full_path = folder_path if absolute else path.join(self.corpus_path, folder_path)
        makedirs(full_path)
        return full_path


class FileWriter:

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

    FORMAT = '<s> {0} </s> ({1})'
    trans_regex = re.compile('\S*[,.?!]+\S*')

    def __init__(self, target_file):
        super().__init__(target_file)

    def add_content(self, *args):
        filtered_trans = TranscriptionWriter.trans_regex.sub(' ', args[0])
        super().add_content(filtered_trans, *args[1:])


class FileidWriter(FileWriter):

    FORMAT = '{0}/{1}'

    def __init__(self, target_file):
        super().__init__(target_file)


class Speaker:
    """Handle the tasks strictly related to speakers entities.
    """
    def __init__(self, id_number, name):
        self._id = id_number
        self.name = name
        self.metadata = self.prompts = self.audios = None


class SpeakerBuilder:

    def __init__(self, _id, name, source_path=None):
        self._speaker = Speaker(_id, name)
        self.relative_path = source_path

    @property
    def speaker(self):
        return self._speaker

    def set_audios(self, **kwargs):
        full_path = kwargs.get('audios_path')
        audio_format = kwargs.get('audio_format', 'wav')
        if self.relative_path:
            full_path = path.join(self.relative_path, full_path) if full_path else self.relative_path
        if full_path and audio_format:
            audios_list = Audios(full_path, audio_format)
            audios_list.populate()
            self.speaker.audios = audios_list
        # TODO else

    def set_prompts(self, *args, **kwargs):
        single_path_list = args
        multi_path = kwargs.get('multi')
        if self.relative_path:
            single_path_list = [path.join(self.relative_path, p) for p in single_path_list]
            single_path_list.append(path.join(self.relative_path, 'etc', 'prompts-original'))
            single_path_list.append(path.join(self.relative_path, '{}.txt'.format(self.speaker.name)))
            multi_path = path.join(self.relative_path, multi_path) if multi_path else self.relative_path
        if single_path_list and multi_path:
            prompts = Prompts.create_prompts(*single_path_list, multi_path=multi_path)
            prompts.populate()
            self.speaker.prompts = prompts
        # TODO else

    def set_metadata(self, **kwargs):
        full_path = kwargs.get('path')
        if self.relative_path:
            if full_path:
                full_path = path.join(self.relative_path, full_path)
            else:
                full_path = path.join(self.relative_path, 'etc', 'README')
        if full_path:
            metadata = Metadata(full_path, kwargs['regex']) if 'regex' in kwargs else Metadata(full_path)
            metadata.populate()
            self.speaker.metadata = metadata
        # else:
        #     raise TypeError('Missing the file path.')


class Prompts(UserDict):

    def populate(self):
        raise NotImplementedError

    @staticmethod
    def create_prompts(*args, **kwargs):
        for file_path in args:
            if path.exists(file_path):
                return SingleFilePrompts(file_path)
        else:
            return MultiFilePrompts(kwargs['multi_path'], kwargs.get('ext', 'txt'))


class SingleFilePrompts(Prompts):

    PROMPT_PATTERN = r"(?P<id>^\d+).?[ ]+(?P<prompt>\S+( \S+)*)"

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def populate(self):
        with open(self.file_path, mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                m = re.search(SingleFilePrompts.PROMPT_PATTERN, line)
                if m:
                    self.data[m.group('id')] = m.group('prompt').lower()


class MultiFilePrompts(Prompts):

    def __init__(self, file_path, ext):
        super().__init__()
        self.file_path = file_path
        self.ext = ext

    def populate(self):
        for trans_file in track_files(self.file_path, self.ext):
            with open(trans_file, mode='r', encoding='utf-8') as f:
                first_line = f.readline()
                if first_line.strip():
                    self.data[path.splitext(path.basename(trans_file))[0]] = first_line.lower()


class Audios(UserList):

    def __init__(self, audios_path, audio_format):
        super().__init__()
        self.path = audios_path
        self.format = audio_format

    def populate(self):
        audios_files = track_files(self.path, self.format)
        for file_path in audios_files:
            self.data.append((path.splitext(path.basename(file_path))[0], file_path))


class Metadata(UserDict):

    DATA_PATTERNS = [
        ('USERNAME', r'(?<=User Name:).*(?=\n)'),
        ('GENDER', r'(?<=Gender:).*(?=\n)'),
        ('AGE', r'(?<=Age Range:).*(?=\n)'),
        ('LANGUAGE', r'(?<=Language:).*(?=\n)')
    ]
    GLOBAL_PATTERN = '|'.join('(?P<%s>%s)' % pair for pair in DATA_PATTERNS)
    REGEX = re.compile(GLOBAL_PATTERN)

    def __init__(self, file_path, regex=REGEX):
        super().__init__()
        self.path = file_path
        self.re = regex

    def populate(self):
        with open(self.path, mode='r', encoding='utf-8') as f:
            content_file = f.read()
            for m in self.re.finditer(content_file):
                self.data[m.lastgroup] = m.group(m.lastgroup).strip()