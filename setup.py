# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='setupam',
    version='0.1.3',
    packages=['setupam'],
    url='https://github.com/gabrielaraujof/setupam',
    license='GPL v2',
    author='Gabriel Araujo',
    author_email='contato@gabrielaraujo.me',
    keywords=["cmu sphinx", "speech", "corpus"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        'console_scripts': ['setupam=setupam.cli:main'],
    },
    description='Command-line tool for setup a speech corpus for training an acoustic model for CMU Sphinx.'
)
