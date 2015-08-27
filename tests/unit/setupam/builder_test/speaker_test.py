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

import unittest
import unittest.mock as mk
from os import path

import setupam.speaker


class SpeakerTest(unittest.TestCase):
    def setUp(self):
        self.src_path = '/home/user/source'
        self.speaker = setupam.speaker.Speaker(self.src_path)

        # TODO Will include tests for speaker class when it's extended.


class ResourceTest(unittest.TestCase):

    @staticmethod
    def create_calls(*args, **kwargs):
        # Create proper paths from args
        paths = (path.join(*arg) if isinstance(arg, tuple) else arg for arg in args)
        # Create the calls object with the paths given
        calls = [mk.call(), mk.call().populate(*paths, **kwargs)]
        return calls
