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
import os
import glob
import math
import random
import logging

import setupam.corpus as cp


parser = argparse.ArgumentParser(description='Structure the voxforge speech corpus in the Sphinx-Train template.')

parser.add_argument('model', help='The name of your model to be set up.')

parser.add_argument('-s', '--source', default='.', help='The source directory for the wav files.')

parser.add_argument(
    '-t', '--target', default='.', help='The target directory for setting up the acoustic model training.')

parser.add_argument(
    '-q', '--quota', default=0.1, type=float,
    help="The percentage (float value) of speakers selected for the tests database. Default=0.1", metavar='Q')

parser.add_argument('--log', default='INFO', help='Print the debug messages.', action="store_true")

args = parser.parse_args()
model, source, target, db_test_p, log_level = args.model, args.source, args.target, args.quota, args.log

numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: {}'.format(log_level))
logging.basicConfig(level=numeric_level, format='%(levelname)s: %(message)s')


def load_spk_content(corpus, spk_path_list):
    for spk_path in spk_path_list:
        builder = cp.SpeakerBuilder(next(corpus.SPEAKER_ID), spk_path, os.path.join(corpus.src, spk_path))
        builder.set_audios()
        builder.set_prompts()
        corpus.add_speaker(builder.speaker)


if __name__ == '__main__':

    logging.info('Scanning for speaker directories...')
    os.chdir(source)
    speakers_dir = [cur_path for cur_path in glob.glob('*') if os.path.isdir(cur_path)]
    spk_count = len(speakers_dir)
    logging.info("Found {} possible speaker's directories.".format(spk_count))

    # Compute the percentage of the tests base
    spk_count_test = math.floor(db_test_p * spk_count)
    if not spk_count_test:
        spk_count_test = 1
    spk_count_train = spk_count - spk_count_test
    logging.info(
        'Selected {} for the train database, and {} for the tests database.'.format(spk_count_train, spk_count_test)
    )
    random.shuffle(speakers_dir)  # Choose speakers randomly

    train_corpus = cp.Corpus(model, target, src_path=source)
    train_corpus.suffix = cp.Corpus.TRAIN_SUFFIX
    logging.info('Setting up the training corpus...')
    train_corpus.set_up()

    logging.info("Loading speakers' content...")
    load_spk_content(train_corpus, speakers_dir[:spk_count_train])
    logging.info('Building train corpus...')
    train_corpus.compile_corpus()

    test_corpus = cp.Corpus(model, target, src_path=source)
    test_corpus.suffix = cp.Corpus.TEST_SUFFIX
    logging.info('Setting up the test corpus...')
    test_corpus.set_up()
    logging.info("Loading speakers' content...")
    load_spk_content(test_corpus, speakers_dir[-spk_count_test:])
    logging.info('Building test corpus...')
    test_corpus.compile_corpus()

    logging.info('Done.')

