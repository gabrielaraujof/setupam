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
    def test_store(self):
        file_path = 'testpath'
        file_w = setupam.io.FileWriter(file_path)
        self.assertEqual(file_w.file, file_path)
        text = 'Texto'
        file_w.content.append(text)
        mock_open = mk.mock_open()
        with mk.patch('setupam.io.open', mock_open, create=True):
            file_w.store()
        handle = mock_open()
        handle.write.assert_called_with(text + '\n')

    def test_add_content(self):
        text = 'text1 text2'.split()
        trans = setupam.io.TranscriptionWriter('test')
        trans.add_content(*text)
        self.assertEqual(trans.content[0], setupam.io.TranscriptionWriter.FORMAT.format(*text))
        fileid = setupam.io.FileidWriter('test')
        fileid.add_content(*text)
        self.assertEqual(fileid.content[0], setupam.io.FileidWriter.FORMAT.format(*text))
