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

from unittest import mock as mk
from os import path

import setupam.corpus as cps
from tests.unit.setupam.corpus_test import ResourceTest


class RelativePathTest(ResourceTest):
    def setUp(self):
        self.relative = '/home'
        self.kwargs = ({'multi_path': path.join('/home', 'folder')}, {'multi_path': self.relative})
        self.builder = cps.SpeakerBuilder(0, 'test', self.relative)

    @staticmethod
    def build_paths(*args):
        file_list = [(file,) for file in args]
        file_list.extend([('etc', 'prompts-original'), ('test.txt',)])
        return [path.join('/home', *args) for args in file_list]

    @mk.patch('setupam.corpus.Prompts')
    def test_multi(self, mock_prompts):
        self.builder.set_prompts(multi='folder')
        mock_prompts.assert_has_calls(self.get_calls(*self.build_paths(), **self.kwargs[0]))

    @mk.patch('setupam.corpus.Prompts')
    def test_both(self, mock_prompts):
        self.builder.set_prompts('file1', multi='folder')
        mock_prompts.assert_has_calls(self.get_calls(*self.build_paths('file1'), **self.kwargs[0]))

    @mk.patch('setupam.corpus.Prompts')
    def test_single(self, mock_prompts):
        self.builder.set_prompts('file1', 'file2')
        mock_prompts.assert_has_calls(self.get_calls(*self.build_paths('file1', 'file2'), **self.kwargs[1]))

    @mk.patch('setupam.corpus.Prompts')
    def test_no_args(self, mock_prompts):
        self.builder.set_prompts()
        mock_prompts.assert_has_calls(self.get_calls(*self.build_paths(), **self.kwargs[1]))


class AbsolutePathTest(ResourceTest):
    def setUp(self):
        self.kwargs = {'multi_path': 'folder'}
        self.builder = cps.SpeakerBuilder(0, 'test')

    def test_no_source_fails(self):
        with self.assertRaisesRegex(TypeError, 'Missing arguments.*'):
            self.builder.set_prompts()

    @mk.patch('setupam.corpus.Prompts')
    def test_no_source_only_one(self, mock_prompts):
        self.builder.set_prompts('file1', 'file2')
        mock_prompts.assert_has_calls(self.get_calls('file1', 'file2'))

    @mk.patch('setupam.corpus.Prompts')
    def test_no_source_only_one2(self, mock_prompts):
        self.builder.set_prompts(multi='folder')
        mock_prompts.assert_has_calls(self.get_calls(**self.kwargs))

    @mk.patch('setupam.corpus.Prompts')
    def test_no_source_both(self, mock_prompts):
        self.builder.set_prompts('file1', 'file2', multi='folder')
        mock_prompts.assert_has_calls(self.get_calls('file1', 'file2', **self.kwargs))
