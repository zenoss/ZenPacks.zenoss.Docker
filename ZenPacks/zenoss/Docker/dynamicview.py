##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""DynamicView adapters.

These adapters are required to satisfy the other side of
impacts/impacted_by relationships to classes not controlled by this
ZenPack. Relationships strictly between classes controlled by this
ZenPack are specified exclusively in zenpack.yaml.

This module depends on DynamicView implicitly and assumes it won't be
imported unless DynamicView is installed. This is accomplished by being
registered in a conditional ZCML section in configure.zcml.

"""

# DynamicView Imports
from ZenPacks.zenoss.DynamicView import TAG_ALL, TAG_IMPACTS
from ZenPacks.zenoss.DynamicView.model.adapters import BaseRelationsProvider


class DeviceRelationsProvider(BaseRelationsProvider):
    """Provides relationships for Products.ZenModel.Device.Device."""

    def relations(self, type=TAG_ALL):
        """Generate IRelation providing objects for adapted object."""
        device = self._adapted

        if type in (TAG_ALL, TAG_IMPACTS):
            if not device.aqBaseHasAttr("docker_containers") and not device.aqBaseHasAttr("podman_containers"):
                return

            for container in device.docker_containers():
                yield self.constructRelationTo(container, TAG_IMPACTS)

            for container in device.podman_containers():
                yield self.constructRelationTo(container, TAG_IMPACTS)
