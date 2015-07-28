SetupAM [![Build Status](https://travis-ci.org/gabrielaraujof/setupam.svg)](https://travis-ci.org/gabrielaraujof/setupam)
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
