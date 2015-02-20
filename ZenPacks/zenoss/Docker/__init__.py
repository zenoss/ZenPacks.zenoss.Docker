"""
Docker zenpack
"""

import logging
log = logging.getLogger('zen.Docker')

import Globals
import os
import re
from Products.ZenUtils.Utils import monkeypatch, unused
from Products.ZenModel.Device import Device
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.interfaces import IDeviceInfo
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

unused(Globals)


# Modules containing model classes. Used by zenchkschema to validate
# bidirectional integrity of defined relationships.
productNames = (
    'DockerContainer',
    )

# Useful to avoid making literal string references to module and class names
# throughout the rest of the ZenPack.
ZP_NAME = 'ZenPacks.zenoss.Docker'
MODULE_NAME = {}
CLASS_NAME = {}
for product_name in productNames:
    MODULE_NAME[product_name] = '.'.join([ZP_NAME, product_name])
    CLASS_NAME[product_name] = '.'.join([ZP_NAME, product_name, product_name])

# Define new device relations.
NEW_DEVICE_RELATIONS = (
    ('docker_containers', 'DockerContainer'),
    )

NEW_COMPONENT_TYPES = (
    'ZenPacks.zenoss.Docker.DockerContainer.DockerContainer',
    )

# Add new relationships to Device if they don't already exist.
for relname, modname in NEW_DEVICE_RELATIONS:
    if relname not in (x[0] for x in Device._relations):
        Device._relations += (
            (relname,
             ToManyCont(ToOne, '.'.join((ZP_NAME, modname)), 'docker_host')),
        )


# Add new properties to Device
Device.docker_version = ""
Device._properties = Device._properties + (
    {'id':'docker_version', 'type':'string', 'mode':'w',
        'label': 'Docker Version'},
)
IDeviceInfo.docker_version = schema.TextLine(
    title=u"Docker Version", group="Details")
DeviceInfo.docker_version = ProxyProperty('docker_version')


class ZenPack(ZenPackBase):
    """
    ZenPack loader that handles custom installation and removal tasks.
    """

    packZProperties = [
    ]

    def install(self, app):
        super(ZenPack, self).install(app)

        log.info('Adding Docker relationships to existing devices')
        self._buildDeviceRelations()

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            log.info('Removing Docker components')

            # Remove our Device relations additions.
            Device._relations = tuple(
                [x for x in Device._relations
                    if x[0] not in NEW_DEVICE_RELATIONS])

            log.info('Removing Docker device relationships')
            self._buildDeviceRelations()

        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

    def _buildDeviceRelations(self):
        for d in self.dmd.Devices.getSubDevicesGen():
            d.buildRelations()


@monkeypatch('Products.ZenHub.services.CommandPerformanceConfig.CommandPerformanceConfig')
def remote_applyDataMaps(self, device, datamaps):
    """Patching command datasource to add partial remodeling"""
    from Products.DataCollector.ApplyDataMap import ApplyDataMap
    device = self.getPerformanceMonitor().findDevice(device)
    applicator = ApplyDataMap(self)

    changed = False
    for datamap in datamaps:
        if applicator._applyDataMap(device, datamap):
            changed = True

    return changed
