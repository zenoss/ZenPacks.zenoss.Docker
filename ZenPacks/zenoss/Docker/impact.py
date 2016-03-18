######################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is
# installed.
#
######################################################################

from zope.component import adapts
from zope.interface import implements

from Products.ZenUtils.guid.interfaces import IGlobalIdentifier

from ZenPacks.zenoss.Impact.impactd import Trigger
from ZenPacks.zenoss.Impact.impactd.relations import ImpactEdge
from ZenPacks.zenoss.Impact.impactd.interfaces import IRelationshipDataProvider
from ZenPacks.zenoss.Impact.impactd.interfaces import INodeTriggers

from ZenPacks.zenoss.Docker.DockerComponent import DockerComponent
from Products.ZenModel.Device import Device

AVAILABILITY = 'AVAILABILITY'
PERCENT = 'policyPercentageTrigger'
THRESHOLD = 'policyThresholdTrigger'
RP = 'ZenPacks.zenoss.Docker'


def guid(obj):
    return IGlobalIdentifier(obj).getGUID()


def edge(source, target):
    return ImpactEdge(source, target, RP)


class BaseRelationsProvider(object):
    implements(IRelationshipDataProvider)

    relationship_provider = RP
    impact_relationships = None
    impacted_by_relationships = None

    def __init__(self, adapted):
        self._object = adapted

    def belongsInImpactGraph(self):
        return True

    def guid(self):
        if not hasattr(self, '_guid'):
            self._guid = guid(self._object)

        return self._guid


class BaseTriggers(object):
    implements(INodeTriggers)

    def __init__(self, adapted):
        self._object = adapted


class DockerContainerRelationsProvider(BaseRelationsProvider):
    adapts(DockerComponent)

    def getEdges(self):
        yield ImpactEdge(guid(self._object.device()), guid(self._object), RP)


class DeviceRelationsProvider(BaseRelationsProvider):
    adapts(Device)

    def getEdges(self):
        for container in self._object.docker_containers():
            yield ImpactEdge(guid(container), guid(self._object.device()), RP)
