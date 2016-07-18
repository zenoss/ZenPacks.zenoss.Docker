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

# Patch docker_version property onto Device and its IInfo/Info.
Device.docker_version = ""
Device._properties = Device._properties + ({
    'id': 'docker_version',
    'type': 'string',
    'mode': 'w',
    'label': 'Docker Version',
    },)

IDeviceInfo.docker_version = form.schema.TextLine(
    title=u"Docker Version",
    group="Details")

DeviceInfo.docker_version = ProxyProperty('docker_version')
