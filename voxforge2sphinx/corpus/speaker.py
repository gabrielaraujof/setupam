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

__author__ = "Gabriel Araujo"
__copyright__ = "Copyright 2014"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Gabriel Araujo"

import shutil as sh
import os
import re

def not_implemented(f):
    """A decorator that raises NotImplementedError exception when called.
    Keeps the docstring of the original function.
    """
    def decorated(*args, **kw):
        message = 'The method %s() is not implemented yet.' % f.func_name
        raise NotImplementedError(message)
    decorated.__doc__ == f.__doc__
    return decorated

def io_access(f):
    """A decorator that handles IOError for functions that access files and directories.
    Keeps the docstring of the original function.
    """
    def decorated(*args, **kw):
        try:
            f(*args, **kw)
        except IOError as e:
            print('I/O error(%s): %s %s' % (e.errno, e.strerror, e.filename))

    decorated.__doc__ == f.__doc__
    return decorated

spkinfo_patterns = [
    ('USERNAME',  r'(?<=User Name:).*(?=\n)'),
    ('GENDER',  r'(?<=Gender:).*(?=\n)'),
    ('AGE',     r'(?<=Age Range:).*(?=\n)'),
    ('LANGUAGE', r'(?<=Language:).*(?=\n)')
]
spkinfo_regex = '|'.join('(?P<%s>%s)' % pair for pair in spkinfo_patterns)
spkinfo_p = re.compile(spkinfo_regex)

class Speaker:

    def __init__(self, spkid, srcdir, trgdir):
        self.id = spkid
        self.source = srcdir
        self.target = trgdir
        self.prompts = self.info = self.audios = None

    def _gatherspkinfo(self):
        """Gather all info about that speaker."""
        filepath = os.path.join(self.source, 'etc', 'README')
        with open(filepath, mode='r', encoding='utf-8') as f:
            tinfo = f.read()
        self.info = {m.lastgroup:m.group(m.lastgroup) for m in spkinfo_p.finditer(tinfo)}

    @io_access
    def _gather_prompts(self):
        """Gather all the transcriptions for that speaker."""
        file_path = os.path.join(self.source, 'etc', 'prompts-original')
        with open(file_path, mode='r', encoding='utf-8') as f:
            self.prompts = {} # initialization
            for line in f.readlines():
                m = re.search(r"(?P<id>^\d+)[ ]+(?P<prompt>\S+( \S+)*)", line)
                if m:
                    self.prompts[m.group('id')] = m.group('prompt')

    @not_implemented
    def _gatheraudios(self):
        """Gather all the speech audios for that speaker."""

    @not_implemented
    def export(self, target):
        """Save the speaker data in the target folder."""

    def _copywav(self, srcwavname, trgwavid):
        """Copy a wav file to the target directory."""
        srcpath = os.path.join(self.source, 'wav', '%s.wav' % srcwavname)
        trgpath = os.path.join(self.target, 'wav', '%04d' % self.id, '%04d_%03d.wav' % (self.id, trgwavid))
        if not os.path.exists(trgpath):
            sh.copy2(srcpath, trgpath)

    @not_implemented
    def _saveinfo(self):
        """Save information to some target file."""