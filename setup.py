#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

try:
    # Since Twisted does not provide egg-info by default, check if we can
    # import it instead of using install_requires in setup()
    import twisted
except ImportError:
    print >>sys.stderr, "PeARS requires Twisted (Core) to be installed"
    sys.exit(3)

from setuptools import setup, find_packages, Command


setup(
      name='PeARS_p2p',
      version='0.1',
      packages=find_packages(),
      test_suite='tests/runalltests',

      author='Nandaja Varma',
      description='A p2p network for PeARS',
      license='LGPLv3+',
      keywords="dht distributed hash table kademlia peer p2p tuple space twisted",

)
