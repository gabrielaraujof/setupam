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
from unittest import mock

from voxforge2sphinx.corpus.speaker import Speaker


class GatherPromptsTest(unittest.TestCase):
    def setUp(self):
        self.spkid = 0
        self.spksrc = 'src'
        self.spktrg = 'trg'
        self.speaker = Speaker(self.spkid, self.spksrc, self.spktrg)

    def test_valid_prompts(self):
        data = "094    Vou tomar um pouquinho d'água. \n095 Para onde a senhora quer ir? \n096   Que horas são? \n\n097 Amanhã é sexta."
        exp_dict = {'094': "Vou tomar um pouquinho d'água.", '095': 'Para onde a senhora quer ir?',
                   '096': 'Que horas são?', '097': 'Amanhã é sexta.'}
        with mock.patch('voxforge2sphinx.corpus.speaker.open', mock.mock_open(read_data=data),
                        create=True) as m:
            self.speaker._gather_prompts()
        self.assertEqual(self.speaker.prompts, exp_dict, 'Dictionary of prompts were loaded incorrectly.')

    def test_invalid_prompts(self):
        data = "094   \nPara onde a senhora quer ir?\n096Que horas são?\n\n"
        exp_dict = {}
        with mock.patch('voxforge2sphinx.corpus.speaker.open', mock.mock_open(read_data=data),
                        create=True) as m:
            self.speaker._gather_prompts()
        self.assertEqual(self.speaker.prompts, exp_dict, 'Dictionary of prompts were loaded incorrectly.')


if __name__ == "__main__":
    unittest.main()