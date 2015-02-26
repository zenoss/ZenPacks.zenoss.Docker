##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import os

from Products.DataCollector.tests.BasePluginsTestCase \
    import BasePluginsTestCase

from ..modeler.plugins.DockerCollector import DockerCollector


class TestDockerCollectorMap(BasePluginsTestCase):

    def runTest(self):
        Plugins = [DockerCollector]
        datadir = "%s/plugindata/docker" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDockerCollectorMap))
    return suite
