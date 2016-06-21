##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Test cases for RemoveOldTemplates test module."""

from .. import zenpacklib
from .. import ZenPack
from ..migrate.RemoveOldTemplates import RemoveOldTemplates

zenpacklib.enableTesting()


class migrateTests(zenpacklib.TestCase):
    """Tests for RemoveOldTemplates.migrate."""

    def afterSetUp(self):
        """Setup for tests in this TestCase."""
        super(migrateTests, self).afterSetUp()

        pack = ZenPack("ZenPacks.zenoss.Docker")
        packs = self.dmd.ZenPackManager.packs
        packs._setObject(pack.id, pack)
        self.pack = packs._getOb(pack.id)
        self.step = RemoveOldTemplates()

    def test_templates_missing(self):
        """Test migration when old templates don't exist."""
        self.assertEquals(0, self.dmd.Devices.rrdTemplates.countObjects())

        self.step.migrate(self.pack)

        self.assertEquals(0, self.dmd.Devices.rrdTemplates.countObjects())

    def test_templates_exist(self):
        """Test migration when old templates do exist."""
        self.assertEquals(0, self.dmd.Devices.rrdTemplates.countObjects())

        self.dmd.Devices.manage_addRRDTemplate("DockerContainer")
        self.dmd.Devices.manage_addRRDTemplate("DockerContainerCoreOS")
        self.dmd.Devices.manage_addRRDTemplate("DockerContainerSize")

        self.assertEquals(3, self.dmd.Devices.rrdTemplates.countObjects())

        self.step.migrate(self.pack)

        self.assertEquals(0, self.dmd.Devices.rrdTemplates.countObjects())
