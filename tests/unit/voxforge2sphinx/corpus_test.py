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

__author__ = 'Gabriel Araujo'

import unittest
from unittest import mock as mk
from os import path

import voxforge2sphinx.corpus as cps


class CorpusTest(unittest.TestCase):

    @mk.patch('voxforge2sphinx.corpus.glob.glob')
    def test_track_files(self, mock_glob):
        cps.Corpus.track_files('file_path', 'ext')
        mock_glob.assert_called_with(path.join('file_path', '*.ext'))


class PromptsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_single(self):
        data = "094    Vou tomar um pouquinho d'água. \n095 Para onde a senhora quer ir? \n" + \
               "096   Que horas são? \n\n097 Amanhã é sexta.\n16.       Para onde a senhora quer ir?"
        exp_dict = {'094': "vou tomar um pouquinho d'água.", '095': 'para onde a senhora quer ir?',
                    '096': 'que horas são?', '097': 'amanhã é sexta.', '16': 'para onde a senhora quer ir?'}

        with mk.patch('voxforge2sphinx.corpus.open', mk.mock_open(read_data=data), create=True) as m:
            self.assertEqual(cps.SingleFilePrompts(''), exp_dict, 'Dictionary of prompts were loaded incorrectly.')

    def test_invalid_single(self):
        data = "094   \nPara onde a senhora quer ir?\n096Que horas são?\n\n"
        with mk.patch('voxforge2sphinx.corpus.open', mk.mock_open(read_data=data),
                        create=True) as m:
            self.assertEqual(cps.SingleFilePrompts(''), {}, 'Dictionary of prompts were loaded incorrectly.')

    @mk.patch('voxforge2sphinx.corpus.Corpus.track_files', return_value=['/home/user/test.txt'])
    @mk.patch('voxforge2sphinx.corpus.open', mk.mock_open(read_data="Vou tomar um pouquinho d'água"), create=True)
    def test_multi(self, mock_track_files):
        multi = cps.MultiFilePrompts('/home/user/', 'txt')
        mock_track_files.assert_called_with('/home/user/', 'txt')
        self.assertTrue('test' in multi)
        self.assertEqual(multi['test'], "vou tomar um pouquinho d'água")


if __name__ == "__main__":
    unittest.main()