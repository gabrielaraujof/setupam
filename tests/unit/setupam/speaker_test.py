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
import setupam.io
import setupam.speaker

__author__ = 'Gabriel Araujo'

import unittest
from unittest import mock as mk


class PromptsTest(unittest.TestCase):
    @mk.patch('setupam.speaker.Prompts._populate_from_files')
    @mk.patch('setupam.speaker.Prompts._populate_from_file')
    def test_prompts(self, mock_single_file, mock_multi_files):
        with self.assertRaises(KeyError):
            prompts = setupam.speaker.Prompts()
            prompts.populate()
        with self.assertRaises(KeyError):
            prompts = setupam.speaker.Prompts()
            prompts.populate('')

        with mk.patch('setupam.corpus.os.path.exists', return_value=True):
            prompts = setupam.speaker.Prompts()
            prompts.populate('', multi_path='', ext='')
            mock_single_file.assert_called_with('')
            mock_multi_files.assert_has_calls([])
            mock_single_file.reset_mock()

        with mk.patch('setupam.corpus.os.path.exists', return_value=False):
            prompts = setupam.speaker.Prompts()
            prompts.populate('', multi_path='')
            mock_multi_files.assert_called_with('', 'txt')
            mock_single_file.assert_has_calls([])
            mock_multi_files.reset_mock()


class SingleFilePromptsTest(unittest.TestCase):
    def setUp(self):
        self.prompts = setupam.speaker.Prompts()

    def test_valid_single(self):
        data = "094    Vou tomar um pouquinho d'água. \n095 Para onde a senhora quer ir? \n" + \
               "096   Que horas são? \n\n097 Amanhã é sexta.\n16.       Para onde a senhora quer ir?"
        exp_dict = {'094': "vou tomar um pouquinho d'água.", '095': 'para onde a senhora quer ir?',
                    '096': 'que horas são?', '097': 'amanhã é sexta.', '16': 'para onde a senhora quer ir?'}

        with mk.patch('setupam.speaker.os.path.exists', return_value=True):
            with mk.patch('setupam.speaker.open', mk.mock_open(read_data=data), create=True):
                self.prompts.populate('', multi_path='')
                self.assertEqual(self.prompts, exp_dict)

    def test_invalid_single(self):
        data = "094   \nPara onde a senhora quer ir?\n096Que horas são?\n\n"
        with mk.patch('setupam.speaker.os.path.exists', return_value=True):
            with mk.patch('setupam.speaker.open', mk.mock_open(read_data=data), create=True):
                self.prompts.populate('', multi_path='')
                self.assertEqual(self.prompts, {})


class MultiFilePromptsTest(unittest.TestCase):
    @mk.patch('setupam.io.track_files', return_value=['/home/user/test.txt'])
    @mk.patch('setupam.speaker.open', mk.mock_open(read_data="Vou tomar um pouquinho d'água"), create=True)
    def test_multi(self, mock_track_files):
        multi = setupam.speaker.Prompts()
        multi.populate(multi_path='/home/user/')
        mock_track_files.assert_called_with('/home/user/', 'txt')
        self.assertTrue('test' in multi)
        self.assertEqual(multi['test'], "vou tomar um pouquinho d'água")


class AudiosTest(unittest.TestCase):

    def setUp(self):
        self.audios = setupam.speaker.Audios()

    def test_populate(self):
        return_list = ('/home/001.wav', '/home/audio.raw', 'file.mp3')
        with mk.patch('setupam.io.track_files', return_value=return_list):
            self.audios.populate('', '')
            self.assertEqual(
                tuple(self.audios),
                (('001', 'wav', '/home/001.wav'), ('audio', 'raw', '/home/audio.raw'), ('file', 'mp3', 'file.mp3')))


class MetadataTest(unittest.TestCase):

    def setUp(self):
        self.metadata = setupam.speaker.Metadata('')

    def test_populate(self):
        content_file = '''
        User Name:anonymous

        Speaker Characteristics:

        Gender: desconhecido
        Age Range: desconhecido
        Language: PT_BR
        Pronunciation dialect: desconhecido
        '''
        exp_dict = {
            'USERNAME': 'anonymous',
            'GENDER': 'desconhecido',
            'AGE': 'desconhecido',
            'LANGUAGE': 'PT_BR'
        }
        with mk.patch('setupam.speaker.open', mk.mock_open(read_data=content_file), create=True):
            self.metadata.populate('')
            self.assertEqual(self.metadata, exp_dict)

if __name__ == "__main__":
    unittest.main()
