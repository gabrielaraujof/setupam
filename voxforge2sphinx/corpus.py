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
    speaker_counter = 0
    audio_counter = 0

    def __init__(self, name, source_path, target_path, audio_fmt='wav'):
        self.name = name
        self.speakers = []
        self.src = source_path
        self.tgt = target_path
        self.audio_format = audio_fmt

    @staticmethod
    def format_speaker_id(spk_id):
        assert isinstance(spk_id, int)
        return '{:06}'.format(spk_id)

    @staticmethod
    def format_audio_id(spk_id, audio_id):
        assert isinstance(spk_id, int)
        assert isinstance(audio_id, int)
        return '{}_{:03}'.format(Corpus.format_speaker_id(spk_id), audio_id)

    @staticmethod
    def track_files(file_path, file_format):
        assert isinstance(file_path, str)
        assert isinstance(file_format, str)
        return glob.glob('{}/*.{}'.format(file_path, file_format)).sort()

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
            target_path = self.create_sub_folder(spk_repr)
            for audio in spk.gather_audios(audio_format=self.audio_format):
                audio_repr = Corpus.format_audio_id(spk_id, audio_ref)
                new_filename = path.join(target_path, '{}.{}'.format(audio_repr, self.audio_format))
                try:
                    copy2(audio, new_filename)
                    # TODO Store fileid (metadata.store_fileids(file_id, speaker_ref, wav_ref))
                    # TODO Store transcription (metadata.store_trans(trans, prompts[path.basename(wavfile)], wav_ref))
                    audio_ref += 1
                except IOError as e:
                    print('I/O error(%s): %s %s' % (e.errno, e.strerror, e.filename))
                    sys.exit(1)

    def create_sub_folder(self, sub_folder):
        directory = path.join(self.tgt, sub_folder)
        makedirs(directory)
        return directory


class Speaker:
    """Handle the tasks strictly related to speakers entities."""

    def __init__(self, source_path, audio_path='wav', metadata_path='etc'):
        #assert path.exists(source_path)
        self.src = source_path
        self.audio_path = audio_path
        self.metadata_path = metadata_path

    def gather_metadata(self, file='README', regex=info_regex):
        assert isinstance(file, str)
        file_path = path.join(self.src, self.metadata_path, file)
        with open(file_path, mode='r', encoding='utf-8') as f:
            content_file = f.read()
        try:
            return {m.lastgroup: m.group(m.lastgroup) for m in regex.finditer(content_file)}
        except AttributeError as e:
            print('Invalid regular expression object: {}'.format(e))

    def gather_transcription(self, file='prompts-original', multi=False, format_file='.txt'):
        if not multi:
            assert isinstance(file, str)
            file_path = path.join(self.src, self.metadata_path, file)
            with open(file_path, mode='r', encoding='utf-8') as f:
                transcriptions = {}
                for line in f.readlines():
                    m = re.search(r"(?P<id>^\d+)[ ]+(?P<prompt>\S+( \S+)*)", line)
                    if m:
                        transcriptions[m.group('id')] = m.group('prompt')
            return transcriptions
        else:
            assert isinstance(format_file, str)
            trans_files = Corpus.track_files(self.src, format_file)
            transcriptions = {}
            for trans_file in trans_files:
                with open(trans_file, mode='r', encoding='utf-8') as f:
                    transcriptions[path.splitext(path.basename(trans_file))[0]] = f.readline()
            return transcriptions

    def gather_audios(self, audio_format='wav'):
        return Corpus.track_files(path.join(self.src, self.audio_path), audio_format)