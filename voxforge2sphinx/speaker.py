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
from glob import iglob
from shutil import copy2

from voxforge2sphinx import metadata


_verbose = True

def _get_wav_files(speakerDir):
    '''Get all wav files in a given directory.'''
    return sorted(iglob(path.join(speakerDir, 'wav/*.wav')))

def _create_dir(target, speaker):
    '''Create the speaker directory.'''
    d = path.join(target, speaker)
    if not path.exists(d):
        try:
            if _verbose:
                print("Creating directory '{}'...".format(d), end='')
            makedirs(d)
            if _verbose:
                print('[Done.]')
        except Exception as err:
            print("Error while creating directory '{}': ".format(d), err)
    return d

def _copy_wavs(sourcefile, targetpath, wav_ref):
    '''Copy the wav files from source path to target path.'''
    dstname = path.join(targetpath, '{}.wav'.format(wav_ref))
    if not path.exists(dstname):
        try:
            (folder, namefile) = path.split(sourcefile)
            if _verbose:
                print("Copying wav file '{}'...".format(namefile), end='')
            copy2(sourcefile, dstname)
            if _verbose:
                print('[Done.]')
            return dstname
        except Exception as err:
            print("Error while copying wav file '{}': ".format(namefile), err)

def add(source_dir, speaker_id, wav_dir, file_id, trans):
    '''Add a speaker to the speech database.'''
    #if args.verbose:
    speaker_ref = '{:04}'.format(speaker_id)
    print("Setting {}. (source: '{}')".format(speaker_ref, source_dir))
    spk_dir = _create_dir(wav_dir, speaker_ref)
    spk_prompts = metadata.get_prompts(source_dir)
    wav_id = 0
    for wavfile in _get_wav_files(source_dir):
        wav_id = wav_id + 1
        wav_ref = '{}_{:03}'.format(speaker_ref, wav_id)
        _copy_wavs(wavfile, spk_dir, wav_ref)
        metadata.store_fileids(file_id, speaker_ref, wav_ref)
        metadata.store_trans(trans, spk_prompts[path.basename(wavfile)], wav_ref)