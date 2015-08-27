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

from unittest import mock as mk
from os import path

from tests.unit.setupam.builder_test.speaker_test import ResourceTest
import setupam.speaker


class AudiosTest(ResourceTest):
    def setUp(self):
        audios_patcher = mk.patch('setupam.speaker.Audios')
        glob_patcher = mk.patch('setupam.speaker.glob.glob', return_value=[''])
        self.addCleanup(audios_patcher.stop)
        self.addCleanup(glob_patcher.stop)
        self.mock_audios = audios_patcher.start()
        self.mock_glob = glob_patcher.start()


class RelativePathTest(AudiosTest):
    def setUp(self):
        super(RelativePathTest, self).setUp()
        self.relative = '/home'
        self.builder = setupam.speaker.SpeakerBuilder('test', self.relative)
        self.args = ('test', 'raw', 'wav')

    def test_no_args(self):
        self.builder.set_audios()
        self.mock_audios.assert_has_calls(self.get_calls(path.join('/home', 'wav'), 'wav'))

    def test_only_path(self):
        self.builder.set_audios(self.args[0])
        self.mock_audios.assert_has_calls(self.get_calls(path.join('/home', self.args[0]), self.args[2]))

    def test_only_format(self):
        self.builder.set_audios(audio_format=self.args[1])
        self.mock_audios.assert_has_calls(self.get_calls(path.join('/home', self.args[2]), self.args[1]))

    def test_both(self):
        # For this test we want to force a situation where the first path doesn't return anything
        self.mock_glob.side_effect = (content for content in ([], ['']))
        self.builder.set_audios('sub', self.args[0], audio_format=self.args[1])
        self.mock_audios.assert_has_calls(self.get_calls(path.join('/home', self.args[0]), self.args[1]))


class AbsolutePathTest(AudiosTest):
    def setUp(self):
        super(AbsolutePathTest, self).setUp()
        self.mock_glob.side_effect = (content for content in ([], ['']))
        self.builder = setupam.speaker.SpeakerBuilder('test')
        self.args = ('home', 'test', 'raw', 'wav')

    def test_fails(self):
        with self.assertRaises(TypeError):
            self.builder.set_audios()
        with self.assertRaises(TypeError):
            self.builder.set_audios(audio_format='')
        with mk.patch('setupam.speaker.glob.glob', return_value=[]):
            with self.assertRaises(ValueError):
                self.builder.set_audios('x', 'y')

    def test_only_path(self):
        self.builder.set_audios(*self.args[:2])
        self.mock_audios.assert_has_calls(self.get_calls(self.args[1], self.args[3]))

    def test_both(self):
        self.builder.set_audios(*self.args[:2], audio_format=self.args[2])
        self.mock_audios.assert_has_calls(self.get_calls(*self.args[1:3]))
