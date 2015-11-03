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

from tests.unit.setupam.builder_test.speaker_test import ResourceTest
import setupam.speaker


class MetadataTest(ResourceTest):
    module_to_patch = setupam.speaker
    class_to_patch = setupam.speaker.Metadata
    method_under_test = setupam.speaker.SpeakerBuilder.set_metadata


class RelativePathTest(MetadataTest):

    @classmethod
    def setUpClass(cls):
        cls.base_path = 'home'
        cls.builder_args = ('test', cls.base_path), {}
        cls.method_args = ('test_path', 're_test')
        cls.assertion_values = (
            {'args': (), 'kwargs': {},
             'expected_calls': cls.create_calls((cls.base_path, 'etc', 'README'))},
            {'args': (), 'kwargs': {'regex': cls.method_args[1]},
             'expected_calls': cls.create_calls((cls.base_path, 'etc', 'README'), cls.method_args[1])},
            {'args': (), 'kwargs': {'full_path': cls.method_args[0]},
             'expected_calls': cls.create_calls((cls.base_path, cls.method_args[0]))},
            {'args': (), 'kwargs': {'full_path': cls.method_args[0], 'regex': cls.method_args[1]},
             'expected_calls': cls.create_calls((cls.base_path, cls.method_args[0]), cls.method_args[1])}
        )

    def test_it(self):
        self.check_all_calls()


class AbsolutePathTest(MetadataTest):
    @classmethod
    def setUpClass(cls):
        cls.builder_args = ('test',), {}
        cls.method_args = ('test_path', 're_test')
        cls.assertion_values = (
            {'args': (), 'kwargs': {'full_path': cls.method_args[0]},
             'expected_calls': cls.create_calls(cls.method_args[0])},
            {'args': (), 'kwargs': {'full_path': cls.method_args[0], 'regex': cls.method_args[1]},
             'expected_calls': cls.create_calls(cls.method_args[0], cls.method_args[1])}
        )

    def test_fails(self):
        with self.assertRaises(TypeError):
            self.builder.set_metadata()
        with self.assertRaises(TypeError):
            self.builder.set_metadata(regex='')

    def test_it(self):
        self.check_all_calls()
