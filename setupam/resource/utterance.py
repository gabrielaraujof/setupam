# -*- coding: utf-8 -*-

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

import os
import glob
import re


def track_files(path_, file_format):
    return glob.glob('{}/*.{}'.format(path_, re.sub(r'\.', '', file_format, count=1)))


def load_utterance(path_):
    """ Validates and creates a single utterance object."""

    class Utterance(object):
        """ A single speech audio file containing an utterance.

            Public	attributes:
    		- path: The absolute path to the file.
        """

        def __init__(self, file_path):
            self.path_ = file_path
            filename = os.path.basename(self.path_)
            self.name, self.ext = os.path.splitext(filename)

    if os.path.isfile(path_):
        return Utterance(path_)
    else:
        raise ValueError("The path {p} isn't a valid file.".format(p=path_))


def from_dir(path_, format_):
    """Creates a list of utterances from a single directory."""

    if not os.path.isdir(path_):
        raise ValueError("The path {p} isn't a directory.".format(p=path_))

    return (load_utterance(path_) for path_ in track_files(path_, format_))
