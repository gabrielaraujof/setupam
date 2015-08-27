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


class PromptsTest(ResourceTest):
    def setUp(self):
        prompts_patcher = mk.patch('setupam.speaker.Prompts')
        self.addCleanup(prompts_patcher.stop)
        self.mock_prompts = prompts_patcher.start()


class RelativePathTest(PromptsTest):
    @classmethod
    def setUpClass(cls):
        cls.relative = 'home'
        cls.kwargs = ({'multi_path': path.join('home', 'folder')}, {'multi_path': cls.relative})
        cls.calls = (
            cls.create_calls(*cls.build_paths(), **cls.kwargs[0]),
            cls.create_calls(*cls.build_paths('file1'), **cls.kwargs[0]),
            cls.create_calls(*cls.build_paths('file1', 'file2'), **cls.kwargs[1]),
            cls.create_calls(*cls.build_paths(), **cls.kwargs[1]),
        )

    @staticmethod
    def build_paths(*args):
        file_list = [(file,) for file in args]
        file_list.extend([('etc', 'prompts-original'), ('test.txt',)])
        return [path.join('home', *args) for args in file_list]

    def setUp(self):
        super(RelativePathTest, self).setUp()
        self.builder = setupam.speaker.SpeakerBuilder('test', self.relative)

    def test_multi(self):
        self.builder.set_prompts(multi='folder')
        self.mock_prompts.assert_has_calls(self.calls[0])

    def test_both(self):
        self.builder.set_prompts('file1', multi='folder')
        self.mock_prompts.assert_has_calls(self.calls[1])

    def test_single(self):
        self.builder.set_prompts('file1', 'file2')
        self.mock_prompts.assert_has_calls(self.calls[2])

    def test_no_args(self):
        self.builder.set_prompts()
        self.mock_prompts.assert_has_calls(self.calls[3])


class AbsolutePathTest(PromptsTest):
    @classmethod
    def setUpClass(cls):
        cls.args = ('file1', 'file2')
        cls.kwargs = {'multi_path': 'folder'}
        cls.calls = (
            cls.create_calls((cls.args[0],), (cls.args[1],)),
            cls.create_calls(**cls.kwargs),
            cls.create_calls(*cls.args, **cls.kwargs)
        )

    def setUp(self):
        super(AbsolutePathTest, self).setUp()
        self.builder = setupam.speaker.SpeakerBuilder('test')

    def test_no_source_fails(self):
        with self.assertRaises(TypeError):
            self.builder.set_prompts()

    def test_no_source_only_one(self):
        self.builder.set_prompts('file1', 'file2')
        self.mock_prompts.assert_has_calls(self.calls[0])

    def test_no_source_only_one2(self):
        self.builder.set_prompts(multi='folder')
        self.mock_prompts.assert_has_calls(self.calls[1])

    def test_no_source_both(self):
        self.builder.set_prompts('file1', 'file2', multi='folder')
        self.mock_prompts.assert_has_calls(self.calls[2])
