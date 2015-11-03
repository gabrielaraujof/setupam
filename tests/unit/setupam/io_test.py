"""
Copyright (C) by Demetrius Santana and Gabriel Araujo - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
File created by Gabriel Araujo <gabrielaraujof@outlook.com>, Agosto 2015
"""
from os import path
import unittest
from unittest import mock as mk

import setupam.io


class TrackFilesTest(unittest.TestCase):
    @mk.patch('setupam.io.glob.glob')
    def test_track_files(self, mock_glob):
        setupam.io.track_files('file_path', 'ext')
        mock_glob.assert_called_with(path.join('file_path', '*.ext'))


class FileWriterTest(unittest.TestCase):

    def test_add_content(self):
        text = 'text1 text2'.split()
        trans = setupam.io.TranscriptionWriter('test')
        trans.add_content(*text)
        self.assertEqual(trans.content.getvalue(), setupam.io.transcription_formatter(*text) + '\n')
        fileid = setupam.io.FileidWriter('test')
        fileid.add_content(*text)
        self.assertEqual(fileid.content.getvalue(), '{0}/{1}'.format(*text) + '\n')
