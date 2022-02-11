##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Platform patches."""

from Products.ZenModel.Device import Device
from Products.Zuul import form
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.interfaces import IDeviceInfo

# Patch docker_version and podman_version properties onto Device and its IInfo/Info.
Device.docker_version = ""
Device.podman_version = ""
Device._properties = Device._properties + ({
    'id': 'docker_version',
    'type': 'string',
    'mode': 'w',
    'label': 'Docker Version',
    },
   {
   'id': 'podman_version',
   'type': 'string',
   'mode': 'w',
   'label': 'Podman Version',
   },
)

IDeviceInfo.docker_version = form.schema.TextLine(
    title=u"Docker Version",
    group="Details")
IDeviceInfo.podman_version = form.schema.TextLine(
    title=u"Podman Version",
    group="Details")

DeviceInfo.docker_version = ProxyProperty('docker_version')
DeviceInfo.podman_version = ProxyProperty('podman_version')
