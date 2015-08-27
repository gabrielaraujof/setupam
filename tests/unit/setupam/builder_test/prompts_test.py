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

from os import path

from tests.unit.setupam.builder_test.speaker_test import ResourceTest
import setupam.speaker


class PromptsTest(ResourceTest):
    module_to_patch = setupam.speaker
    class_to_patch = setupam.speaker.Prompts
    method_under_test = setupam.speaker.SpeakerBuilder.set_prompts


class RelativePathTest(PromptsTest):

    @classmethod
    def setUpClass(cls):
        cls.base_path = 'home'
        cls.builder_args = ('test', cls.base_path), {}
        cls.method_args = {'multi_path': path.join('home', 'folder')}, {'multi_path': cls.base_path}
        cls.assertion_values = (
            {'args': (), 'kwargs': {'multi': 'folder'},
             'expected_calls': cls.create_calls(*cls.build_paths(), **cls.method_args[0])},
            {'args': ('file1',), 'kwargs': {'multi': 'folder'},
             'expected_calls': cls.create_calls(*cls.build_paths('file1'), **cls.method_args[0])},
            {'args': ('file1', 'file2'), 'kwargs': {},
             'expected_calls': cls.create_calls(*cls.build_paths('file1', 'file2'), **cls.method_args[1])},
            {'args': (), 'kwargs': {},
             'expected_calls': cls.create_calls(*cls.build_paths(), **cls.method_args[1])}
        )

    @staticmethod
    def build_paths(*args):
        file_list = [(file,) for file in args]
        file_list.extend([('etc', 'prompts-original'), ('test.txt',)])
        return [path.join('home', *args) for args in file_list]

    def test_it(self):
        self.check_all_calls()


class AbsolutePathTest(PromptsTest):

    @classmethod
    def setUpClass(cls):
        cls.builder_args = ('test',), {}
        cls.method_args = ('file1', 'file2'), {'multi_path': 'folder'}
        cls.assertion_values = (
            {'args': ('file1', 'file2'), 'kwargs': {},
             'expected_calls': cls.create_calls(*cls.method_args[0])},
            {'args': (), 'kwargs': {'multi': 'folder'},
             'expected_calls': cls.create_calls(**cls.method_args[1])},
            {'args': ('file1', 'file2'), 'kwargs': {'multi': 'folder'},
             'expected_calls': cls.create_calls(*cls.method_args[0], **cls.method_args[1])},
        )

    def test_no_source_fails(self):
        with self.assertRaises(TypeError):
            self.builder.set_prompts()

    def test_it(self):
        self.check_all_calls()
