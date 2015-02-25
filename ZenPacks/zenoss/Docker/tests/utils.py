##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################


import os.path
import pickle
from zope.event import notify
from Products.Zuul.catalog.events import IndexingEvent


def loadPickle(filename):
    f = open(os.path.join(os.path.dirname(__file__), 'data', filename), 'r')
    data = pickle.load(f)
    f.close()
    return data


def add_obj(relationship, obj):
    """
    Add obj to relationship, index it, then returns the persistent
    object.
    """
    relationship._setObject(obj.id, obj)
    obj = relationship._getOb(obj.id)
    obj.index_object()
    notify(IndexingEvent(obj))
    return obj


def test_device(dmd, factor=1):
    """
     Return an example SolarisMonitorDevice with a set of example components.
    """
    from ZenPacks.zenoss.Docker.DockerContainer \
        import DockerContainer

    dc = dmd.Devices.createOrganizer('/Server')

    device = dc.createInstance('docker_test')
    device.setPerformanceMonitor('localhost')
    device.index_object()
    notify(IndexingEvent(device))

    for dc_id in range(factor):
        dc = add_obj(
            device.docker_containers,
            DockerContainer('dc%s' % (dc_id))
        )

    return device
