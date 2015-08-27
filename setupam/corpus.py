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

import os
import shutil
import sys

import setupam.speaker
import setupam.io


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
        self.trans_file = setupam.io.TranscriptionWriter(
            os.path.join(self.corpus_path, Corpus.METADATA_DIR, trans_filename)
        )
        fileid_filename = self.format_filename(self.suffix, Corpus.FILEID_EXT)
        self.fileid_file = setupam.io.FileidWriter(
            os.path.join(self.corpus_path, Corpus.METADATA_DIR, fileid_filename)
        )

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
        if isinstance(speaker, setupam.speaker.Speaker):
            self.speakers.append((next(self.SPEAKER_ID), speaker))
        else:
            raise ValueError('Invalid speaker object. Given {}.'.format(speaker))

    def _store_files(self):
        self.trans_file.store()
        self.fileid_file.store()

    def compile_corpus(self):
        for spk_id, spk in self.speakers:
            spk_repr = self.format_speaker_id(spk_id)
            spk_dir_path = self.create_folder(os.path.join(Corpus.AUDIO_DIR, spk_repr))
            for audio_name, audio_ext, audio_old_path in spk.audios:
                if audio_name in spk.prompts:  # Has transcription?
                    audio_repr = self.format_audio_id(spk_repr, next(self.AUDIO_ID))
                    audio_new_path = os.path.join(spk_dir_path, '{}.{}'.format(audio_repr, audio_ext))
                    self._copy_audio(audio_old_path, audio_new_path)
                    # Include transcription
                    self.trans_file.add_content(spk.prompts[audio_name], audio_repr)
                    # Include file_id
                    self.fileid_file.add_content(spk_repr, audio_repr)
        self._store_files()
