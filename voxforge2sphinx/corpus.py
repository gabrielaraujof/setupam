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
from collections import UserDict

info_attributes = [
    ('USERNAME', r'(?<=User Name:).*(?=\n)'),
    ('GENDER', r'(?<=Gender:).*(?=\n)'),
    ('AGE', r'(?<=Age Range:).*(?=\n)'),
    ('LANGUAGE', r'(?<=Language:).*(?=\n)')
]
info_pattern = '|'.join('(?P<%s>%s)' % pair for pair in info_attributes)
info_regex = re.compile(info_pattern)


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
    def track_files(file_path, file_format):
        return glob.glob('{}/*.{}'.format(file_path, file_format)).sort()

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
        self.trans_file = TranscriptionFile(path.join(self.corpus_path, Corpus.METADATA_DIR, trans_filename))
        fileid_filename = self.format_filename(Corpus.FILEID_EXT)
        self.fileid_file = FileidFile(path.join(self.corpus_path, Corpus.METADATA_DIR, fileid_filename))

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


class Speaker:
    """Handle the tasks strictly related to speakers entities."""

    def __init__(self, source_path, audio_path='wav', metadata_path='etc'):
        assert path.exists(source_path)
        self.src = source_path
        self.name = path.basename(self.src)
        self.audio_path = audio_path
        self.metadata_path = path.join(self.src, metadata_path)
        self.trans = None

    def gather_metadata(self, file='README', regex=info_regex):
        file_path = path.join(self.src, self.metadata_path, file)
        with open(file_path, mode='r', encoding='utf-8') as f:
            content_file = f.read()
        try:
            return {m.lastgroup: m.group(m.lastgroup) for m in regex.finditer(content_file)}
        except AttributeError as e:
            print('Invalid regular expression object: {}'.format(e))

    def gather_transcription(self, **kwargs):
        sub_folder = path.join(self.metadata_path, 'prompts-original')
        root_folder = path.join(self.src, '{}.txt'.format(self.name))
        path_list = kwargs.get('path_list', (sub_folder, root_folder))
        self.trans = Prompts.create_prompts(*path_list, multi_path=self.src)

    def gather_audios(self, audio_format='wav'):
        return Corpus.track_files(path.join(self.src, self.audio_path), audio_format)


class FileWriter:

    def __init__(self, file_path):
        assert path.exists(path.dirname(file_path))
        self.file = file_path
        self.content = []

    @classmethod
    def format_content(cls, args):
        return cls.FORMAT.format(*args)

    def add_content(self, *args):
        formatted_content = FileWriter.format_content(args)
        self.content.append(formatted_content)

    def store(self):
        with open(self.file, mode='a', encoding='iso-8859-1') as file:
            for line in self.content:
                file.write(line + '\n')


class TranscriptionFile(FileWriter):

    FORMAT = '<s> {0} </s> ({1})'
    trans_regex = re.compile('\S*[,.?!]+\S*')

    def __init__(self, target_file):
        super().__init__(target_file)

    def add_content(self, *args):
        filtered_trans = TranscriptionFile.trans_regex.sub(' ', args[0])
        super().add_content(filtered_trans, *args[1:])


class FileidFile(FileWriter):

    FORMAT = '{0}/{1}'

    def __init__(self, target_file):
        super().__init__(target_file)


class Prompts(UserDict):

    def __init__(self, *args):
        super().__init__()
        self.load_prompts(*args)

    def load_prompts(self, *args):
        raise NotImplementedError

    @staticmethod
    def create_prompts(*args, **kwargs):
        assert (len(args) > 0) and ('multi_path' in kwargs)
        for file_path in args:
            if path.exists(file_path):
                return SingleFilePrompts(file_path)
        else:
            return MultiFilePrompts(kwargs['multi_path'], kwargs.get('ext', 'txt'))


class SingleFilePrompts(Prompts):

    PROMPT_PATTERN = r"(?P<id>^\d+).?[ ]+(?P<prompt>\S+( \S+)*)"

    def load_prompts(self, *args):
        with open(args[0], mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                m = re.search(SingleFilePrompts.PROMPT_PATTERN, line)
                if m:
                    self.data[m.group('id')] = m.group('prompt').lower()


class MultiFilePrompts(Prompts):

    def load_prompts(self, *args):
        file_path, ext = args
        for trans_file in Corpus.track_files(file_path, ext):
            with open(trans_file, mode='r', encoding='utf-8') as f:
                self.data[path.splitext(path.basename(trans_file))[0]] = f.readline().lower()
