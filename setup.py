#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='pyGOBN',
      version='1.0',
      description='GOBNILP for Python',
      author='Nicholas Cullen',
      author_email='ncullen.th@dartmouth.edu',
      url='sites.dartmouth.edu/ncullen',
      packages=find_packages(),
      #py_modules = ['pyGOBN.pyGOBN'],
      long_description="""Global Optimization of Bayesian Networks through
      	Integer Linear Programming. This module provides
      	wrapper functions for unpacking/making/installing/running
      	the GOBNILP source code. GOBNILP is a project aimed at 
      	solving the EXACT formulation of the Bayesian Network
      	structure learning problem. For further details, see
      	the GOBNILP main website."""
     )