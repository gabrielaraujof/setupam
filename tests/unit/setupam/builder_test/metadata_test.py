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


class MetadataTest(ResourceTest):
    def setUp(self):
        metadata_patcher = mk.patch('setupam.speaker.Metadata')
        self.addCleanup(metadata_patcher.stop)
        self.mock_metadata = metadata_patcher.start()


class RelativePathTest(MetadataTest):
    def setUp(self):
        super(RelativePathTest, self).setUp()
        self.relative = '/home'
        self.builder = setupam.speaker.SpeakerBuilder('test', self.relative)
        self.args = ('test_path', 're_test')

    def test_no_args(self):
        self.builder.set_metadata()
        self.mock_metadata.assert_has_calls(self.get_calls(path.join(self.relative, 'etc', 'README')))

    def test_regex(self):
        self.builder.set_metadata(regex=self.args[1])
        self.mock_metadata.assert_has_calls(self.get_calls(path.join(self.relative, 'etc', 'README'), self.args[1]))

    def test_only_path(self):
        self.builder.set_metadata(full_path=self.args[0])
        self.mock_metadata.assert_has_calls(self.get_calls(path.join(self.relative, self.args[0])))

    def test_both(self):
        self.builder.set_metadata(full_path=self.args[0], regex=self.args[1])
        self.mock_metadata.assert_has_calls(self.get_calls(path.join(self.relative, self.args[0]), self.args[1]))


class AbsolutePathTest(MetadataTest):
    def setUp(self):
        super(AbsolutePathTest, self).setUp()
        self.builder = setupam.speaker.SpeakerBuilder('test')
        self.args = ('test_path', 're_test')

    def test_fails(self):
        with self.assertRaises(TypeError):
            self.builder.set_metadata()
        with self.assertRaises(TypeError):
            self.builder.set_metadata(regex='')
        with self.assertRaises(TypeError):
            self.builder.set_metadata('something', 'another_thing')

    def test_only_path(self):
        self.builder.set_metadata(full_path=self.args[0])
        self.mock_metadata.assert_has_calls(self.get_calls('test_path'))

    def test_no_source_both(self):
        self.builder.set_metadata(full_path=self.args[0], regex=self.args[1])
        self.mock_metadata.assert_has_calls(self.get_calls(*self.args))
