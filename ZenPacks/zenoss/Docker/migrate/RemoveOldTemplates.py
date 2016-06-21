##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Removes old monitoring templates.

Version 1.x of this ZenPack installed the following monitoring templates
that are no longer needed in the root (/Devices) device class.

* DockerContainer
* DockerContainerCoreOS
* DockerContainerSize

"""

import logging
LOG = logging.getLogger("zen.Docker")

from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPackMigration

OLD_TEMPLATES = [
    "DockerContainer",
    "DockerContainerCoreOS",
    "DockerContainerSize",
    ]


class RemoveOldTemplates(ZenPackMigration):
    """Migrate step."""

    version = Version(2, 0, 0)

    def migrate(self, pack):
        """Execute migration."""
        devices = pack.getDmdRoot("Devices")

        LOG.info("removing old Docker monitoring templates")
        for template in OLD_TEMPLATES:
            try:
                devices.manage_deleteRRDTemplates(ids=[template])
            except Exception:
                pass
