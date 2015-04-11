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

import re
from os import path
import pathlib as pl
import glob as g

_verbose = True

def get_prompts(speaker_dir):
    '''Get the list of iriginal prompts of the given speaker.'''
    files_path = pl.Path(speaker_dir) / '*.txt'
    prompts = []
    for audio in sorted(g.iglob(str(files_path))):
        #print('>>>>' + audio)
        with open(audio, mode='r', encoding='utf-8') as p_file:
            prompts.append([audio, p_file.readline()])

    #with open(path.join(speaker_dir, 'etc', 'prompts-original'), mode='r', encoding='utf-8') as p_file:
    #    prompts =  [x.split(maxsplit=1) for x in p_file.readlines()]
    return {pl.Path(x[0]).name:re.search('[^\n]+', x[1]).group(0) for x in prompts}

def _store(file_path, data):
    '''Store some metadata in a file.'''
    with open(file_path, mode='a', encoding='iso-8859-1') as file:
        if _verbose:
            print("Storing '{}' in {}.".format(data, path.split(file_path)[1]))
        file.write(data + '\n')

def store_fileids(file_path, speaker_ref, wav_ref):
    _store(file_path, '{}/{}'.format(speaker_ref, wav_ref))

def _build_trans(prompt, wav_ref):
    prompt = prompt.lower()
    pattern = re.compile('[,.?!]+')
    prompt = pattern.sub('', prompt)
    return '<s> {} </s> ({})'.format(prompt, wav_ref)

def store_trans(file_path, prompt, wav_ref):
    '''Store the transcription of a wav file'''
    trans = _build_trans(prompt, wav_ref)
    _store(file_path, trans)