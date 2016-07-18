##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Test cases for DynamicView and Impact."""

from Products.DataCollector.plugins.DataMaps import RelationshipMap

from . import dvi


# Relationships expected in DynamicView and Impact.
EXPECTED_BOTH = """
[container-host]->[container-host/container-1]
[container-host]->[container-host/container-2]
"""

# Relationships only expected in DynamicView.
EXPECTED_DYNAMICVIEW_ONLY = """
"""

# Relationships only expected in Impact.
EXPECTED_IMPACT_ONLY = """
"""

# Devices against which the above relationships will be tested.
DEVICES = {
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


class DVITests(dvi.DVITest):
    """Test case for DynamicView and Impact."""

    device_data = DEVICES
    expected_both = EXPECTED_BOTH
    expected_dynamicview_only = EXPECTED_DYNAMICVIEW_ONLY
    expected_impact_only = EXPECTED_IMPACT_ONLY
