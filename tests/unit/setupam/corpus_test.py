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

import setupam.corpus as cps


def glob_side_effect():
        yield []
        yield ['']


class CorpusTest(unittest.TestCase):
    @mk.patch('setupam.corpus.glob.glob')
    def test_track_files(self, mock_glob):
        cps.track_files('file_path', 'ext')
        mock_glob.assert_called_with(path.join('file_path', '*.ext'))


class SpeakerTest(unittest.TestCase):
    def setUp(self):
        self.src_path = '/home/user/source'
        self._id = 0
        self.speaker = cps.Speaker(self._id, self.src_path)


class SpkBuilderAudiosTest(unittest.TestCase):

    def setUp(self):
        self.builder = cps.SpeakerBuilder(0, 'test')

    def test_no_source_fails(self):
        with self.assertRaisesRegex(TypeError, 'Missing.*path list'):
            self.builder.set_audios()
        with self.assertRaisesRegex(TypeError, 'Missing.*path list'):
            self.builder.set_audios(audio_format='')
        with mk.patch('setupam.corpus.glob.glob', return_value=[]):
            with self.assertRaisesRegex(ValueError, '.*invalid path list.*'):
                self.builder.set_audios('x', 'y')

    @mk.patch('setupam.corpus.Audios')
    @mk.patch('setupam.corpus.glob.glob', side_effect=glob_side_effect())
    def test_no_source_only_path(self, mock_glob, mock_audios):
        self.builder.set_audios('/home', '/test')
        calls = [mk.call(), mk.call().populate('/test', 'wav')]
        mock_audios.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Audios')
    @mk.patch('setupam.corpus.glob.glob', side_effect=glob_side_effect())
    def test_no_source_both(self, mock_glob, mock_audios):
        self.builder.set_audios('/home', '/test', audio_format='raw')
        calls = [mk.call(), mk.call().populate('/test', 'raw')]
        mock_audios.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Audios')
    @mk.patch('setupam.corpus.glob.glob', return_value=[''])
    def test_source_no_args(self, mock_glob, mock_audios):
        self.builder.relative_path = '/home'
        self.builder.set_audios()
        calls = [mk.call(), mk.call().populate(path.join('/home', 'wav'), 'wav')]
        mock_audios.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Audios')
    @mk.patch('setupam.corpus.glob.glob', return_value=[''])
    def test_source_only_path(self, mock_glob, mock_audios):
        self.builder.relative_path = '/home'
        self.builder.set_audios('test')
        calls = [mk.call(), mk.call().populate(path.join('/home', 'test'), 'wav')]
        mock_audios.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Audios')
    @mk.patch('setupam.corpus.glob.glob', return_value=[''])
    def test_source_only_format(self, mock_glob, mock_audios):
        self.builder.relative_path = '/home'
        self.builder.set_audios(audio_format='raw')
        calls = [mk.call(), mk.call().populate(path.join('/home', 'wav'), 'raw')]
        mock_audios.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Audios')
    @mk.patch('setupam.corpus.glob.glob', side_effect=glob_side_effect())
    def test_source_both(self, mock_glob, mock_audios):
        self.builder.relative_path = '/home'
        self.builder.set_audios('sub', 'test', audio_format='raw')
        calls = [mk.call(), mk.call().populate(path.join('/home', 'test'), 'raw')]
        mock_audios.assert_has_calls(calls)


class SpkBuilderPromptsTest(unittest.TestCase):

    def setUp(self):
        self.builder = cps.SpeakerBuilder(0, 'test')

    def test_no_source_fails(self):
        with self.assertRaisesRegex(TypeError, 'Missing arguments.*'):
            self.builder.set_prompts()

    @mk.patch('setupam.corpus.Prompts.create_prompts')
    def test_no_source_only_one(self, mock_prompts):
        self.builder.set_prompts('file1', 'file2')
        calls = [mk.call('file1', 'file2'), mk.call().populate()]
        mock_prompts.assert_has_calls(calls)
        mock_prompts.reset_mock()
        self.builder.set_prompts(multi='folder')
        calls = [mk.call(multi_path='folder'), mk.call().populate()]
        mock_prompts.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Prompts.create_prompts')
    def test_no_source_both(self, mock_prompts):
        self.builder.set_prompts('file1', 'file2', multi='folder')
        calls = [mk.call('file1', 'file2', multi_path='folder'), mk.call().populate()]
        mock_prompts.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Prompts.create_prompts')
    def test_source_no_args(self, mock_prompts):
        self.builder.relative_path = '/home'
        self.builder.set_prompts()
        paths = [path.join('/home', *args) for args in [('etc', 'prompts-original'), ('test.txt',)]]
        calls = [mk.call(*paths, multi_path='/home'), mk.call().populate()]
        mock_prompts.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Prompts.create_prompts')
    def test_source_only_path(self, mock_prompts):
        self.builder.relative_path = '/home'
        self.builder.set_prompts('file1', 'file2')
        paths = [
            path.join('/home', *args) for args in [('file1',), ('file2',), ('etc', 'prompts-original'), ('test.txt',)]]
        calls = [mk.call(*paths, multi_path='/home'), mk.call().populate()]
        mock_prompts.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Prompts.create_prompts')
    def test_source_only_multi(self, mock_prompts):
        self.builder.relative_path = '/home'
        self.builder.set_prompts(multi='folder')
        paths = [path.join('/home', *args) for args in [('etc', 'prompts-original'), ('test.txt',)]]
        calls = [mk.call(*paths, multi_path=path.join('/home', 'folder')), mk.call().populate()]
        mock_prompts.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Prompts.create_prompts')
    def test_source_both(self, mock_prompts):
        self.builder.relative_path = '/home'
        self.builder.set_prompts('file1', multi='folder')
        paths = [
            path.join('/home', *args) for args in [('file1',), ('etc', 'prompts-original'), ('test.txt',)]]
        calls = [mk.call(*paths, multi_path=path.join('/home', 'folder')), mk.call().populate()]
        mock_prompts.assert_has_calls(calls)


class SpkBuilderMetadataTest(unittest.TestCase):

    def setUp(self):
        self.builder = cps.SpeakerBuilder(0, 'test')

    def test_no_source_fails(self):
        with self.assertRaisesRegex(TypeError, 'Missing.*path'):
            self.builder.set_metadata()
        with self.assertRaisesRegex(TypeError, 'Missing.*path'):
            self.builder.set_metadata(regex='')

    @mk.patch('setupam.corpus.Metadata')
    def test_no_source_only_path(self, mock_metadata):
        self.builder.set_metadata(path='test_path')
        calls = [mk.call(), mk.call().populate('test_path')]
        mock_metadata.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Metadata')
    def test_no_source_both(self, mock_metadata):
        self.builder.set_metadata(path='test_path', regex='test')
        calls = [mk.call(), mk.call().populate('test_path', 'test')]
        mock_metadata.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Metadata')
    def test_source_no_args(self, mock_metadata):
        self.builder.relative_path = '/home'
        self.builder.set_metadata()
        calls = [mk.call(), mk.call().populate(path.join('/home', 'etc', 'README'))]
        mock_metadata.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Metadata')
    def test_source_only_regex(self, mock_metadata):
        self.builder.relative_path = '/home'
        self.builder.set_metadata(regex='re_test')
        calls = [mk.call(), mk.call().populate(path.join('/home', 'etc', 'README'), 're_test')]
        mock_metadata.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Metadata')
    def test_source_only_path(self, mock_metadata):
        self.builder.relative_path = '/home'
        self.builder.set_metadata(path='test_path')
        calls = [mk.call(), mk.call().populate(path.join('/home', 'test_path'))]
        mock_metadata.assert_has_calls(calls)

    @mk.patch('setupam.corpus.Metadata')
    def test_source_both(self, mock_metadata):
        self.builder.relative_path = '/home'
        self.builder.set_metadata(path='test_path', regex='test')
        calls = [mk.call(), mk.call().populate(path.join('/home', 'test_path'), 'test')]
        mock_metadata.assert_has_calls(calls)


class FileWriterTest(unittest.TestCase):
    def test_store(self):
        file_path = 'testpath'
        file_w = cps.FileWriter(file_path)
        self.assertEqual(file_w.file, file_path)
        text = 'Texto'
        file_w.content.append(text)
        mock_open = mk.mock_open()
        with mk.patch('setupam.corpus.open', mock_open, create=True):
            file_w.store()
        handle = mock_open()
        handle.write.assert_called_with(text + '\n')

    def test_add_content(self):
        text = 'text1 text2'.split()
        trans = cps.TranscriptionWriter('test')
        trans.add_content(*text)
        self.assertEqual(trans.content[0], cps.TranscriptionWriter.FORMAT.format(*text))
        fileid = cps.FileidWriter('test')
        fileid.add_content(*text)
        self.assertEqual(fileid.content[0], cps.FileidWriter.FORMAT.format(*text))


class PromptsTest(unittest.TestCase):

    @mk.patch('setupam.corpus.MultiFilePrompts')
    @mk.patch('setupam.corpus.SingleFilePrompts')
    def test_prompts(self, mock_single_prompts, mock_multi_prompts):
        with self.assertRaises(NotImplementedError):
            cps.Prompts().populate()
        with self.assertRaises(KeyError):
            cps.Prompts.create_prompts()
        with self.assertRaises(KeyError):
            cps.Prompts.create_prompts('')

        with mk.patch('setupam.corpus.os.path.exists', return_value=True):
            cps.Prompts.create_prompts('', multi_path='', ext='')
            mock_single_prompts.assert_called_with('')
            mock_multi_prompts.assert_has_calls([])
            mock_single_prompts.reset_mock()

        with mk.patch('setupam.corpus.os.path.exists', return_value=False):
            cps.Prompts.create_prompts('', multi_path='')
            mock_multi_prompts.assert_called_with('', 'txt')
            mock_single_prompts.assert_has_calls([])
            mock_multi_prompts.reset_mock()


class SingleFilePromptsTest(unittest.TestCase):
    def setUp(self):
        self.prompts = cps.SingleFilePrompts('')

    def test_valid_single(self):
        data = "094    Vou tomar um pouquinho d'água. \n095 Para onde a senhora quer ir? \n" + \
               "096   Que horas são? \n\n097 Amanhã é sexta.\n16.       Para onde a senhora quer ir?"
        exp_dict = {'094': "vou tomar um pouquinho d'água.", '095': 'para onde a senhora quer ir?',
                    '096': 'que horas são?', '097': 'amanhã é sexta.', '16': 'para onde a senhora quer ir?'}

        with mk.patch('setupam.corpus.open', mk.mock_open(read_data=data), create=True):
            self.prompts.populate()
            self.assertEqual(self.prompts, exp_dict)

    def test_invalid_single(self):
        data = "094   \nPara onde a senhora quer ir?\n096Que horas são?\n\n"
        with mk.patch('setupam.corpus.open', mk.mock_open(read_data=data), create=True):
            self.prompts.populate()
            self.assertEqual(self.prompts, {})


class MultiFilePromptsTest(unittest.TestCase):
    @mk.patch('setupam.corpus.track_files', return_value=['/home/user/test.txt'])
    @mk.patch('setupam.corpus.open', mk.mock_open(read_data="Vou tomar um pouquinho d'água"), create=True)
    def test_multi(self, mock_track_files):
        multi = cps.MultiFilePrompts('/home/user/', 'txt')
        multi.populate()
        mock_track_files.assert_called_with('/home/user/', 'txt')
        self.assertTrue('test' in multi)
        self.assertEqual(multi['test'], "vou tomar um pouquinho d'água")


class AudiosTest(unittest.TestCase):

    def setUp(self):
        self.audios = cps.Audios()

    def test_populate(self):
        return_list = ('/home/001.wav', '/home/audio.raw', 'file.mp3')
        with mk.patch('setupam.corpus.track_files', return_value=return_list):
            self.audios.populate('', '')
            self.assertEqual(
                tuple(self.audios),
                (('001', 'wav', '/home/001.wav'), ('audio', 'raw', '/home/audio.raw'), ('file', 'mp3', 'file.mp3')))

class MetadataTest(unittest.TestCase):

    def setUp(self):
        self.metadata = cps.Metadata('')

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
        with mk.patch('setupam.corpus.open', mk.mock_open(read_data=content_file), create=True):
            self.metadata.populate('')
            self.assertEqual(self.metadata, exp_dict)

if __name__ == "__main__":
    unittest.main()