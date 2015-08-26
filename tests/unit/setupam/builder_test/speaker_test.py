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
import unittest.mock as mk

import setupam.corpus as cps


class SpeakerTest(unittest.TestCase):
    def setUp(self):
        self.src_path = '/home/user/source'
        self.speaker = cps.Speaker(self.src_path)

    @mk.patch('setupam.corpus.Corpus.format_speaker_id', return_value='')
    def test_str(self, mock_corpus):
        str(self.speaker)
        mock_corpus.assert_has_calls([])


class ResourceTest(unittest.TestCase):
    @staticmethod
    def get_calls(*args, **kwargs):
        return [mk.call(), mk.call().populate(*args, **kwargs)]
