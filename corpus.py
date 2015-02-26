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
        self._load()

    def _load(self):
        '''Load the speaker data.'''
        try:
            self._gatherspkinfo()
            self._gatherprompts()
            self._gatheraudios()
        except IOError as e:
            print('I/O error(%s): %s %s' % (e.errno, e.strerror, e.filename))

    def _gatherspkinfo(self):
        '''Gather all info about that speaker.'''
        filepath = os.path.join(self.source, 'etc', 'README')
        with open(filepath, mode='r', encoding='utf-8') as f:
            tinfo = f.read()
        self.info = {m.lastgroup:m.group(m.lastgroup) for m in spkinfo_p.finditer(tinfo)}

    def _gatherprompts(self):
        '''Gather all the transcriptions for that speaker.'''
        filepath = os.path.join(self.source, 'etc', 'prompts-original')
        with open(filepath, mode='r', encoding='utf-8') as f:
            promptlist =  [(line.split('\n')[0]).split(maxsplit=1) for line in f.readlines()]
        self.prompts = {prompt[0]:prompt[1] for prompt in promptlist}

    def _gatheraudios(self):
        '''Gather all the speech audios for that speaker.'''
        pass

    def export(self, target):
        '''Save the speaker data in the target folder.'''
        pass

    def _copywav(self, srcwavname, trgwavid):
        '''Copy a wav file to the target directory.'''
        srcpath = os.path.join(self.source, 'wav', '%s.wav' % srcwavname)
        trgpath = os.path.join(self.target, 'wav', '%04d' % self.id, '%04d_%03d.wav' % (self.id, trgwavid))
        if not os.path.exists(trgpath):
            sh.copy2(srcpath, trgpath)

    def _saveinfo(self):
        '''Save information to some target file.'''
        pass
