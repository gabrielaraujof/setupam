SetupAM  [![Build Status](https://travis-ci.org/gabrielaraujof/setupam.svg)](https://travis-ci.org/gabrielaraujof/setupam) [![Coverage Status](https://coveralls.io/repos/gabrielaraujof/setupam/badge.svg?branch=master&service=github)](https://coveralls.io/github/gabrielaraujof/setupam?branch=master) [![Code Climate](https://codeclimate.com/github/gabrielaraujof/setupam/badges/gpa.svg)](https://codeclimate.com/github/gabrielaraujof/setupam)
===================

A command-line tool to setup a speech corpus for training an acoustic model for CMU Sphinx.

TODO
----

- One `Corpus` object must be composed of training and testing parts.
- Split the collection of audios in training and testing parts by audio's count (unlike the currently speaker's count).
- Increase the coverage of the tests.
- Create a `Audio` class.
- Compile information about the database ( *total hours, train/test percentage, last update, etc* )
- Remove the hard-coded formats in classes.
- Enhance the logging.
- Support configuration file.

Authors
-------

The tool was developed and it's being maintained by [Gabriel Araujo](http://gabrielaraujo.me). For any help, please contact on his [e-mail](mailto:contato@gabrielaraujo.me) address.
