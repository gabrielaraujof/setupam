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

import argparse
import os
import glob
import math
import random
import logging

import setupam.corpus
import setupam.speaker


def setup_log(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {}'.format(log_level))
    logging.basicConfig(level=numeric_level, format='%(levelname)s: %(message)s')


def get_parser():
    parser = argparse.ArgumentParser(description='Structure the voxforge speech corpus in the Sphinx-Train template.')
    parser.add_argument('-s', '--source', default='.', help='The source directory for the wav files.')
    parser.add_argument(
        '-t', '--target', default='.', help='The target directory for setting up the acoustic model training.')
    parser.add_argument(
        '-r', '--ratio', default=0.1, type=float,
        help="The ratio of speakers selected for the train and tests base. Default to 10%.")
    parser.add_argument('-l', '--log', default='INFO', help='Print the debug messages.')
    parser.add_argument('model', help='The name of your model to be set up.')
    return parser


def load_spk_content(corpus, spk_path_list):
    for spk_path in spk_path_list:
        builder = setupam.speaker.SpeakerBuilder(spk_path, os.path.join(corpus.src, spk_path))
        builder.set_audios()
        builder.set_prompts()
        corpus.add_speaker(builder.speaker)


def build_corpus(log, ratio, source, model, target):
    setup_log(log)

    logging.info('Checking source directory.')
    if not os.path.isabs(source):
        source = os.path.abspath(source)
    if not os.path.exists(source):
        raise ValueError("The source directory {} doesn't exists.".format(source))

    logging.info('Scanning for speaker directories...')
    cwd = os.getcwd()
    os.chdir(source)  # Changing working directory to source
    speakers_dir = [cur_path for cur_path in glob.glob('*') if os.path.isdir(cur_path)]
    spk_count = len(speakers_dir)
    os.chdir(cwd)  # Returning to working directory
    logging.info("Found {} possible speaker's directories.".format(spk_count))

    # Compute the percentage of the tests base
    spk_count_test = math.floor(ratio * spk_count)
    if not spk_count_test:
        spk_count_test = 1
    spk_count_train = spk_count - spk_count_test
    logging.info(
        'Selected {} for the train database, and {} for the tests database.'.format(spk_count_train, spk_count_test)
    )
    random.shuffle(speakers_dir)  # Choose speakers randomly

    train_corpus = setupam.corpus.Corpus(model, target, src_path=source)
    train_corpus.suffix = setupam.corpus.Corpus.TRAIN_SUFFIX
    logging.info('Setting up the training corpus...')
    train_corpus.set_up()

    logging.info("Loading speakers' content...")
    load_spk_content(train_corpus, speakers_dir[:spk_count_train])
    logging.info('Building train corpus...')
    train_corpus.compile_corpus()

    test_corpus = setupam.corpus.Corpus(model, target, src_path=source)
    test_corpus.suffix = setupam.corpus.Corpus.TEST_SUFFIX
    logging.info('Setting up the test corpus...')
    test_corpus.set_up()
    logging.info("Loading speakers' content...")
    load_spk_content(test_corpus, speakers_dir[-spk_count_test:])
    logging.info('Building test corpus...')
    test_corpus.compile_corpus()

    logging.info('Done.')


def main():
    args = vars(get_parser().parse_args())
    build_corpus(**args)
