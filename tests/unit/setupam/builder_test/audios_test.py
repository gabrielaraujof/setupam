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

from tests.unit.setupam.builder_test.speaker_test import ResourceTest
import setupam.speaker


class AudiosTest(ResourceTest):
    module_to_patch = setupam.speaker
    class_to_patch = setupam.speaker.Audios
    method_under_test = setupam.speaker.SpeakerBuilder.set_audios

    def setUp(self):
        super(AudiosTest, self).setUp()
        glob_patcher = mk.patch('{}.{}'.format(self.module_to_patch.__name__, 'glob.glob'), return_value=[''])
        self.addCleanup(glob_patcher.stop)
        self.mock_glob = glob_patcher.start()


class RelativePathTest(AudiosTest):

    @classmethod
    def setUpClass(cls):
        cls.base_path = 'home'
        cls.builder_args = ('test', cls.base_path), {}
        cls.args = 'home', 'wav'
        cls.assertion_values = (
            {'args': (), 'kwargs': {},
             'expected_calls': cls.create_calls((cls.args[0], cls.args[1]), cls.args[1])},
            {'args': (), 'kwargs': {'audio_format': cls.args[1]},
             'expected_calls': cls.create_calls((cls.args[0], cls.args[1]), cls.args[1])},
            {'args': (cls.args[0],), 'kwargs': {},
             'expected_calls': cls.create_calls((cls.args[0], cls.args[0]), cls.args[1])},
        )

    def test_it(self):
        self.check_all_calls()

    def test_only_path(self):
        # For this test we want to force a situation where the first path doesn't return anything
        self.mock_glob.side_effect = (content for content in ([], ['']))
        args = {
            'args': ('sub', self.args[0]), 'kwargs': {'audio_format': self.args[1]},
            'expected_calls': self.create_calls((self.args[0], self.args[0]), self.args[1])}
        self.check_call(**args)


class AbsolutePathTest(AudiosTest):

    @classmethod
    def setUpClass(cls):
        cls.builder_args = ('test',), {}
        cls.method_args = ('home', 'test', 'wav')
        cls.assertion_values = (
            {'args': cls.method_args[:2], 'kwargs': {},
             'expected_calls': cls.create_calls(cls.method_args[0], cls.method_args[2])},
            {'args': cls.method_args[:2], 'kwargs': {'audio_format': cls.method_args[2]},
             'expected_calls': cls.create_calls(cls.method_args[0], cls.method_args[2])},
        )

    def test_fails(self):
        with self.assertRaises(TypeError):
            self.builder.set_audios()
        with self.assertRaises(TypeError):
            self.builder.set_audios(audio_format='')
        with mk.patch('setupam.speaker.glob.glob', return_value=[]):
            with self.assertRaises(ValueError):
                self.builder.set_audios('x', 'y')

    def test_it(self):
        self.check_all_calls()
