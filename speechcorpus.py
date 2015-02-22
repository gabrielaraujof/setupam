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

class Speaker:

    def __init__(self, srddir, trgdir):
        self.source = srcdir
        self.target = trgdir
        self.samples = []

    def load(self):
        '''Load the speaker data.'''
        pass

    def _gatherspkinfo(self):
        '''Gather all info about that speaker.'''
        pass

    def _gatherprompts(self):
        '''Gather all the transcriptions for that speaker.'''
        pass

    def _gatheraudios(self):
        '''Gather all the speech audios for that speaker.'''
        pass

    def export(self, target):
        '''Save the speaker data in the target folder.'''
        pass

    def _copywavs(self, srcpath, trgname):
        '''Copy a wav file to the target directory.'''
        try:
            trgpath = os.path.join(self.target, '%s.wav' % trgname)
            if not os.path.exists(trgpath):
                sh.copy2(srcpath, trgpath)
		except Exception as err:
			print("Error while copying the file '%s'.\n" % namefile, err)

    def _saveinfo(self):
        '''Save information to some target file.'''
        pass

#class AudioSample:

#    def __init__(self, path, name):
#        self.path = path
#        self.name = name
