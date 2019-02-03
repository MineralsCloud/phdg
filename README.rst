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

Introduction
============

Background
----------

The phase relation business has always been tedious. Even we only consider two elements, they could have already form many compounds and each have a bound of polymorphs. When we are dealing with a real world phase system like that in the earth, it could be nothing but even more annoying. This package hopes to resolve this phase relation problem for scientists. After you have calculated Gibbs free energy for all the phases, this program will consider the possible combinations at each temperature-pressure point at a given grid, and help you build the phase diagrams.

Based on the Gibbs free energy calculated with quasi-harmonic approximation, this package serves the following purposes:

1. Plot the given Gibbs energy pressure temperature field for all of the phases
2. Plot fields for all the possible combinations
3. Plot phase diagrams for a given system
4. Plot energy difference at a given temperature and pressure range

Concepts
--------

Here we introduces three basic abstractions for our program.

System
^^^^^^

System is the ensemble of everything. A system comprises of several substances. Some of them could form combinations.

Combination
^^^^^^^^^^^

Combination is a combination of one or more substances. You can understand it as one side of chemical reaction equation.

Substance
^^^^^^^^^

The substance could be understood as one polymorph for one given chemical formula, it is the basic unit of processing. Substance instance holds the gibbs free energy.

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