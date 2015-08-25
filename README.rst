SetupAM: A command-line tool for setup a speech corpus.
-------------------------------------------------------

.. image:: https://travis-ci.org/gabrielaraujof/setupam.svg
   :alt: Build status
   :target: https://travis-ci.org/gabrielaraujof/setupam

.. image:: https://coveralls.io/repos/gabrielaraujof/setupam/badge.svg?branch=master&service=github
    :alt: Coverage status
    :target: https://coveralls.io/github/gabrielaraujof/setupam?branch=master

.. image:: https://codeclimate.com/github/gabrielaraujof/setupam/badges/gpa.svg
    :alt: Code climate
    :target: https://codeclimate.com/github/gabrielaraujof/setupam


Requires Python 3.4 or later

Installation
------------

Install from `PyPI <https://pypi.python.org/pypi/setupam>`_::

    pip3 install setupam

Usage
-----

SetupAM comes with a command-line script that helps you on setting up a basic speech corpus::

    setupam -s source_dir corpus_name 

You can also specify the target directory and the train-test ratio::

    setupam -s source_dir -t target_dir -r 0.15 corpus_name 

TODO
----

- One `Corpus` object must be composed of training and testing parts.
- Split the collection of audios in training and testing parts by audio's count (unlike the currently speaker's count).
- Increase the coverage of the tests.
- Create a `Audio` class.
- Compile information about the database ( *total hours, train/test ratio, last update, etc* )
- Remove the hard-coded formats in classes.
- Enhance the logging.
- Support for configuration file.

LICENSE
-------

SteupAM is licensed under `GPLv2`_.

.. _GPLv2: LICENSE

About
-----

SetupAM was developed and it's being maintained by Gabriel Araujo. For any help, please `contact me`_.

.. _contact me: contato@gabrielaraujo.me
