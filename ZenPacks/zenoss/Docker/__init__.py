##############################################################################
#
# Copyright (C) Zenoss, Inc. 2014-2018, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Initialization for Docker.

All code in this module is executed anytime a Zenoss Python process starts.

"""

import os

from ZenPacks.zenoss.ZenPackLib import zenpacklib


CFG = zenpacklib.load_yaml([
    os.path.join(os.path.dirname(__file__), "zenpack.yaml"),
    ])

schema = CFG.zenpack_module.schema


# Patch last to avoid import recursion problems.
from . import patches  # noqa
