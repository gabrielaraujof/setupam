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

import argparse
from os import path, makedirs
from glob import iglob
from shutil import copy2
from math import floor
from random import shuffle
import re
import metadata

parser = argparse.ArgumentParser(description='Structure the voxforge speech corpus in the Sphinx-Train template.')

parser.add_argument('model', help='The name of your model to be set up.')

parser.add_argument('-s', '--source', default='.', help='The source directory for the wav files.')

parser.add_argument('-t', '--target', default='.', help='The target directory for the wav files.')

parser.add_argument('-q', '--quota', default=0.1, type=float, \
	help="The percentage (float value) of speakers selected for the test database. Default=0.1", metavar='Q')

parser.add_argument('-v', '--verbose', help='Print the debug messages.', action="store_true")

args = parser.parse_args()

model = args.model
source = args.source
target = path.join(args.target, model)
dbtest_p = args.quota

def getAllDirs(source):
	'''Get all wav directories.'''
	return [path.split(x)[0] for x in sorted(iglob(path.join(source, '*/wav')))]

def getWavFiles(speakerDir):
	'''Get all wav files in a given directory.'''
	return sorted(iglob(path.join(speakerDir, 'wav/*.wav')))

def mkdirSpeaker(target, index):
	'''Create the speaker directory.'''
	d = path.join(target, 'speaker_{}'.format(str(index)))
	if not path.exists(d):
		try:
			if args.verbose:
				print("Creating directory '{}'...".format(d), end='')
			makedirs(d)
			if args.verbose:
				print('[Done.]')
		except Exception as err:
			print("Error while creating directory '{}': ".format(d), err)
	return d

def copywavs(sourcefile, targetpath, wav_index):
	'''Copy the wav files from source path to target path.'''
	dstname = path.join(targetpath, '{:03}.wav'.format(wav_index))
	if not path.exists(dstname):
		try:
			(folder, namefile) = path.split(sourcefile)
			if args.verbose:
				print("Copying wav file '{}'...".format(namefile), end='')
			copy2(sourcefile, dstname)
			if args.verbose:
				print('[Done.]')
			return dstname
		except Exception as err:
			print("Error while copying wav file '{}': ".format(namefile), err)

if __name__ == '__main__':
	metadata._verbose = args.verbose

	# Creating root directories
	etc_dir = path.join(target, 'etc')
	if not path.exists(etc_dir):
		makedirs(etc_dir) # Creating the configuration files' directory.
	wav_dir = path.join(target, 'wav')
	if not path.exists(wav_dir):
		makedirs(wav_dir) # Creating the audios' directory.

	# Path of configuration files
	train_fileid = path.join(etc_dir, '{}_train.fileids'.format(model))
	train_trans = path.join(etc_dir, '{}_train.transcription'.format(model))
	test_fileid = path.join(etc_dir, '{}_test.fileids'.format(model))
	test_trans = path.join(etc_dir, '{}_test.transcription'.format(model))


	dirs = getAllDirs(source)
	nspeakers = len(dirs)
	print("Found {} speakers' directories.".format(nspeakers))
	
	nstest =  floor(dbtest_p * nspeakers)
	nstrain = nspeakers - nstest
	print('Selected {} speakers for the train database, and {} speakers for the test database.'.format(nstrain,nstest))

	shuffle(dirs)

	speaker_count = 0
	wav_count = 0
	for directory in dirs: # Iterating over speakers' directories
		speaker_count = speaker_count + 1
		if speaker_count <= nstrain:
			fileid = train_fileid
			trans = train_trans
		else:
			fileid = test_fileid
			trans = test_trans

		#if args.verbose:
		print("Setting speaker number {}. (source: '{}')".format(speaker_count, directory))
		spk_dir = mkdirSpeaker(wav_dir, speaker_count)
		spk_prompts = metadata.get_prompts(directory)
		for wavfile in getWavFiles(directory):
			wav_count = wav_count + 1
			copywavs(wavfile, spk_dir, wav_count)
			metadata.store_fileids(fileid, speaker_count, wav_count)
			metadata.store_trans(trans, spk_prompts[path.basename(wavfile)], wav_count)
			
			
