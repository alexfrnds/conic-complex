# Conic-complex
This module accompanies the following article : https://arxiv.org/abs/2408.01065

## Summary
Computes the gamma-linear projected barcode of conic complex with (potentially) the use of the projected barcode template.

## Installation
Run the command :

`pip install .`

from now on the algorithm are accessible with the module _ccomplex_.

See __tests/__ for further examples. 

## Requirement
The following module is required:
- [phat python bindings](https://github.com/xoltar/phat)

Bug fix : if __pybind11__ is not recognized just reinstall __setuptools__,__wheel__,__pybind11__ from pip.

## Requirements (examples)
The repository contains notebooks to generate examples using the python binding of [2pac](https://gitlab.com/flenzen/2pac).

