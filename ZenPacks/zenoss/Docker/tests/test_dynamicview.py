##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016-2019, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""DynamicView tests."""

from Products.DataCollector.plugins.DataMaps import RelationshipMap

try:
    from ZenPacks.zenoss.DynamicView.tests import DynamicViewTestCase
except ImportError:
    import unittest

    @unittest.skip("tests require DynamicView >= 1.7.0")
    class DynamicViewTestCase(unittest.TestCase):
        """TestCase stub if DynamicViewTestCase isn't available."""


class DynamicViewTests(DynamicViewTestCase):
    """DynamicView tests."""

    # ZenPacks to initialize for testing purposes.
    zenpacks = [
        "ZenPacks.zenoss.Docker",
    ]

    # Expected impact relationships.
    expected_impacts = """
    [container-host]->[container-host/container-1]
    [container-host]->[container-host/container-2]
    """

    device_data = {
        "container-host": {
            "deviceClass": "/Server/Linux",
            "zPythonClass": "Products.ZenModel.Device",
            "dataMaps": [
                RelationshipMap(
                    modname="ZenPacks.zenoss.Docker.DockerContainer",
                    relname="docker_containers",
                    objmaps=[{
                        "id": "container-1",
                    }, {
                        "id": "container-2",
                    }])
            ]},

        "normal-host": {
            "deviceClass": "/Server/Linux",
            "zPythonClass": "Products.ZenModelDevice",
            "dataMaps": [],
        },
    }

    def test_impacts(self):
        self.check_impacts()
