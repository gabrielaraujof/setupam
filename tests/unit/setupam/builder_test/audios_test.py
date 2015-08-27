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
import setupam.speaker

__author__ = 'Gabriel Araujo'

from unittest import mock as mk
from os import path

from tests.unit.setupam.builder_test.speaker_test import ResourceTest


def glob_side_effect():
    yield []
    yield ['']


class RelativePathTest(ResourceTest):
    def setUp(self):
        self.relative = '/home'
        self.builder = setupam.speaker.SpeakerBuilder('test', self.relative)
        self.args = ('test', 'raw', 'wav')

    @mk.patch('setupam.speaker.Audios')
    @mk.patch('setupam.speaker.glob.glob', return_value=[''])
    def test_no_args(self, mock_glob, mock_audios):
        self.builder.set_audios()
        mock_audios.assert_has_calls(self.get_calls(path.join('/home', 'wav'), 'wav'))

    @mk.patch('setupam.speaker.Audios')
    @mk.patch('setupam.speaker.glob.glob', return_value=[''])
    def test_only_path(self, mock_glob, mock_audios):
        self.builder.set_audios(self.args[0])
        mock_audios.assert_has_calls(self.get_calls(path.join('/home', self.args[0]), self.args[2]))

    @mk.patch('setupam.speaker.Audios')
    @mk.patch('setupam.speaker.glob.glob', return_value=[''])
    def test_only_format(self, mock_glob, mock_audios):
        self.builder.set_audios(audio_format=self.args[1])
        mock_audios.assert_has_calls(self.get_calls(path.join('/home', self.args[2]), self.args[1]))

    @mk.patch('setupam.speaker.Audios')
    @mk.patch('setupam.speaker.glob.glob', side_effect=glob_side_effect())
    def test_both(self, mock_glob, mock_audios):
        self.builder.set_audios('sub', self.args[0], audio_format=self.args[1])
        mock_audios.assert_has_calls(self.get_calls(path.join('/home', self.args[0]), self.args[1]))


class AbsolutePathTest(ResourceTest):
    def setUp(self):
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

    @mk.patch('setupam.speaker.Audios')
    @mk.patch('setupam.speaker.glob.glob', side_effect=glob_side_effect())
    def test_only_path(self, mock_glob, mock_audios):
        self.builder.set_audios(*self.args[:2])
        mock_audios.assert_has_calls(self.get_calls(self.args[1], self.args[3]))

    @mk.patch('setupam.speaker.Audios')
    @mk.patch('setupam.speaker.glob.glob', side_effect=glob_side_effect())
    def test_both(self, mock_glob, mock_audios):
        self.builder.set_audios(*self.args[:2], audio_format=self.args[2])
        mock_audios.assert_has_calls(self.get_calls(*self.args[1:3]))
