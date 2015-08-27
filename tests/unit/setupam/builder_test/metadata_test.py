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


class RelativePathTest(ResourceTest):
    def setUp(self):
        self.relative = '/home'
        self.builder = setupam.speaker.SpeakerBuilder('test', self.relative)
        self.args = ('test_path', 're_test')

    @mk.patch('setupam.speaker.Metadata')
    def test_no_args(self, mock_metadata):
        self.builder.set_metadata()
        mock_metadata.assert_has_calls(self.get_calls(path.join(self.relative, 'etc', 'README')))

    @mk.patch('setupam.speaker.Metadata')
    def test_regex(self, mock_metadata):
        self.builder.set_metadata(regex=self.args[1])
        mock_metadata.assert_has_calls(self.get_calls(path.join(self.relative, 'etc', 'README'), self.args[1]))

    @mk.patch('setupam.speaker.Metadata')
    def test_only_path(self, mock_metadata):
        self.builder.set_metadata(full_path=self.args[0])
        mock_metadata.assert_has_calls(self.get_calls(path.join(self.relative, self.args[0])))

    @mk.patch('setupam.speaker.Metadata')
    def test_both(self, mock_metadata):
        self.builder.set_metadata(full_path=self.args[0], regex=self.args[1])
        mock_metadata.assert_has_calls(self.get_calls(path.join(self.relative, self.args[0]), self.args[1]))


class AbsolutePathTest(ResourceTest):
    def setUp(self):
        self.builder = setupam.speaker.SpeakerBuilder('test')
        self.args = ('test_path', 're_test')

    def test_fails(self):
        with self.assertRaises(TypeError):
            self.builder.set_metadata()
        with self.assertRaises(TypeError):
            self.builder.set_metadata(regex='')
        with self.assertRaises(TypeError):
            self.builder.set_metadata('something', 'another_thing')

    @mk.patch('setupam.speaker.Metadata')
    def test_only_path(self, mock_metadata):
        self.builder.set_metadata(full_path=self.args[0])
        mock_metadata.assert_has_calls(self.get_calls('test_path'))

    @mk.patch('setupam.speaker.Metadata')
    def test_no_source_both(self, mock_metadata):
        self.builder.set_metadata(full_path=self.args[0], regex=self.args[1])
        mock_metadata.assert_has_calls(self.get_calls(*self.args))
