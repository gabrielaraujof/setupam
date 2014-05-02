#!/usr/bin/env python3

__author__ = "Gabriel Araujo"
__copyright__ = "Copyright 2014"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Gabriel Araujo"
__email__ = "gabrielaraujof@outlook.com"

import re
from os import path

_verbose = True

def get_prompts(speaker_dir):
	'''Get the list of iriginal prompts of the given speaker.'''
	with open(path.join(speaker_dir, 'etc', 'prompts-original'), mode='r', encoding='utf-8') as p_file:
		prompts =  [x.split(maxsplit=1) for x in p_file.readlines()]
	return {x[0]+'.wav':re.search('[^\n]+', x[1]).group(0) for x in prompts}

def _store(file_path, data):
	'''Store some metadata in a file.'''
	with open(file_path, mode='a', encoding='iso-8859-1') as file:
		if _verbose:
			print("Storing '{}' in {}.".format(data, path.split(file_path)[1]))
		file.write(data + '\n')

def store_fileids(file_path, speaker, wav):
	_store(file_path, 'speaker_{}/{:03}'.format(speaker,wav))

def build_trans(prompt, wav_ref):
	prompt = prompt.lower()
	pattern = re.compile('[,.?!]+')
	prompt = pattern.sub('', prompt)
	return '<s> {} </s> ({:03})'.format(prompt, wav_ref)

def store_trans(file_path, prompt, wav_ref):
	'''Store the transcription of a wav file'''
	trans = build_trans(prompt, wav_ref)
	_store(file_path, trans)