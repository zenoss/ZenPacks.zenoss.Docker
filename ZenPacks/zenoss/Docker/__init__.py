##############################################################################
#
# Copyright (C) Zenoss, Inc. 2014, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Initialization for Docker.

All code in this module is executed anytime a Zenoss Python process starts.

"""

from . import zenpacklib

CFG = zenpacklib.load_yaml()


# Patch last to avoid import recursion problems.
from . import patches  # noqa
