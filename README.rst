.. raw:: html

    <h1 align="center">PHDG</h1>
    <div align="center">
    Thermo phase diagrams with ease.
    </div>
    <div align="center">
    <sub>Build by <a href="https://github.com/chazeon/">Chenxing</a> with :heart:.</sub>
    </div>
    <br />

.. contents:: **Table of Contents**
.. section-numbering::

Background
==========

Based on the Gibbs free energy calculated with quasi-harmonic approximation, this package serves the following purposes:

1. Plot phase diagrams for a given system
2. Plot energy difference at a given temperature and pressure range

Concepts
========

System
------

Combination
-----------

Substance
---------

Usage
=====

Dependencies
------------

This package is build for **Python 3** (>=3.6) with minimalism in mind. It depends only on

- **Numpy**: Math library.
- **Matplotlib**: Afterall, this is a package for ploting, right? :)
- **PyYAML**: Parses configuration file.

You would be able to install these dependencies with

.. code :: bash

  $ pip3 install -r requirements.txt

CLI Interface
-------------

Get the input file ready, and just run the ``src/app.py`` script with Python:

.. code :: bash

  $ python3 src/app.py {PATH/TO/INPUT.yaml}


Licence
=======

To be decided.