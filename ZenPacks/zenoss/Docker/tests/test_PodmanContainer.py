##############################################################################
#
# Copyright (C) Zenoss, Inc. 2022, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Test cases for DockerContainer module."""

from .. import zenpacklib

zenpacklib.enableTesting()


class getRRDTemplatesTests(zenpacklib.TestCase):
    """Tests for DockerContainer.getRRDTemplates."""

    def afterSetUp(self):
        """Setup for tests in this TestCase."""
        super(getRRDTemplatesTests, self).afterSetUp()

        self.root_dc = self.dmd.Devices
        self.linux_dc = self.dmd.Devices.createOrganizer("/Server/SSH/Linux")
        self.linux_dc.setZenProperty("zPythonClass", "ZenPacks.zenoss.LinuxMonitor")

        self.device = self.linux_dc.createInstance("test-podman")
        self.device.setManageIp("192.0.2.78")
        self.device.setPerformanceMonitor("localhost")

        from ZenPacks.zenoss.Docker.PodmanContainer import PodmanContainer
        container = PodmanContainer("test-container")
        self.device.podman_containers._setObject(container.id, container)
        self.container = self.device.podman_containers._getOb(container.id)

    def test_missing_templates(self):
        """Test with monitoring enabled without matching templates.

        Only one of the templates that should be used exists. So it's
        the only thing that should be in the list. This is mostly
        testing that the list only contains one item.

        """
        self.root_dc.manage_addRRDTemplate("PodmanContainer-Status")
        self.device.setZenProperty("zPodmanMonitorContainerStatus", True)
        self.device.setZenProperty("zPodmanMonitorContainerStats", True)
        self.device.setZenProperty("zPodmanMonitorContainerSize", True)

        self.assertEqual(
            ["PodmanContainer-Status"],
            [x.id for x in self.container.getRRDTemplates()])

    def test_everything_enabled(self):
        """Test with all templates and all monitoring enabled."""
        self.root_dc.manage_addRRDTemplate("PodmanContainer-Status")
        self.root_dc.manage_addRRDTemplate("PodmanContainer-Stats")
        self.root_dc.manage_addRRDTemplate("PodmanContainer-Size")
        self.device.setZenProperty("zPodmanMonitorContainerStatus", True)
        self.device.setZenProperty("zPodmanMonitorContainerStats", True)
        self.device.setZenProperty("zPodmanMonitorContainerSize", True)

        self.assertEqual(
            ["PodmanContainer-Status", "PodmanContainer-Stats", "PodmanContainer-Size"],
            [x.id for x in self.container.getRRDTemplates()])

    def test_size_disabled(self):
        """Test with all templates, but size monitoring disabled."""
        self.root_dc.manage_addRRDTemplate("PodmanContainer-Status")
        self.root_dc.manage_addRRDTemplate("PodmanContainer-Stats")
        self.root_dc.manage_addRRDTemplate("PodmanContainer-Size")
        self.device.setZenProperty("zPodmanMonitorContainerStatus", True)
        self.device.setZenProperty("zPodmanMonitorContainerStats", True)
        self.device.setZenProperty("zPodmanMonitorContainerSize", False)

        self.assertEqual(
            ["PodmanContainer-Status", "PodmanContainer-Stats"],
            [x.id for x in self.container.getRRDTemplates()])

    def test_user_template(self):
        """Test with a user-created template."""
        self.root_dc.manage_addRRDTemplate("PodmanContainer")
        self.device.setZenProperty("zPodmanMonitorContainerStatus", True)
        self.device.setZenProperty("zPodmanMonitorContainerStats", True)
        self.device.setZenProperty("zPodmanMonitorContainerSize", False)

        self.assertEqual(
            ["PodmanContainer"],
            [x.id for x in self.container.getRRDTemplates()])
