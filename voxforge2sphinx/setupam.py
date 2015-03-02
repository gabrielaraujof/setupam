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
from math import floor
from random import shuffle

from voxforge2sphinx import speaker, metadata


parser = argparse.ArgumentParser(description='Structure the voxforge speech corpus in the Sphinx-Train template.')

parser.add_argument('model', help='The name of your model to be set up.')

parser.add_argument('-s', '--source', default='.', help='The source directory for the wav files.')

parser.add_argument('-t', '--target', default='.', help='The target directory for setting up the acoustic model training.')

parser.add_argument('-q', '--quota', default=0.1, type=float, \
	help="The percentage (float value) of speakers selected for the tests database. Default=0.1", metavar='Q')

parser.add_argument('-v', '--verbose', help='Print the debug messages.', action="store_true")

args = parser.parse_args()

model = args.model
source = args.source
target = path.join(args.target, model)
dbtest_p = args.quota

def get_all_dirs(source):
	'''Get all wav directories.'''
	return [path.split(x)[0] for x in sorted(iglob(path.join(source, '*/wav')))]

if __name__ == '__main__':
	metadata._verbose = args.verbose
	speaker._verbose = args.verbose

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

	# Get all speaker directories to setup.
	dirs = get_all_dirs(source)
	nspeakers = len(dirs)
	print("Found {} speakers' directories.".format(nspeakers))
	
	# Compute the percentage of the tests base
	nstest =  floor(dbtest_p * nspeakers)
	nstrain = nspeakers - nstest
	print('Selected {} speakers for the train database, and {} speakers for the tests database.'.format(nstrain,nstest))

	shuffle(dirs) #choose speakers randomly

	# Iterating over train speakers' directories
	for speaker_id in range(nstrain):
		speaker.add(dirs[speaker_id], speaker_id, wav_dir, train_fileid, train_trans)

	# Iterating over tests speakers' directories
	for speaker_id in range(nstrain, nspeakers):
		speaker.add(dirs[speaker_id], speaker_id, wav_dir, test_fileid, test_trans)			
			
