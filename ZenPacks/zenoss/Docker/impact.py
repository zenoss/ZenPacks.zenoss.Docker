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

from Products.ZenRelations.ToManyRelationship import ToManyRelationshipBase
from Products.ZenRelations.ToOneRelationship import ToOneRelationship
from Products.ZenUtils.guid.interfaces import IGlobalIdentifier

from ZenPacks.zenoss.Impact.impactd import Trigger
from ZenPacks.zenoss.Impact.impactd.relations import ImpactEdge
from ZenPacks.zenoss.Impact.impactd.interfaces import IRelationshipDataProvider
from ZenPacks.zenoss.Impact.impactd.interfaces import INodeTriggers

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

    def impact(self, relname):
        relationship = getattr(self._object, relname, None)
        if relationship:
            if isinstance(relationship, ToOneRelationship):
                obj = relationship()
                if obj:
                    yield edge(self.guid(), guid(obj))

            elif isinstance(relationship, ToManyRelationshipBase):
                for obj in relationship():
                    yield edge(self.guid(), guid(obj))

    def impacted_by(self, relname):
        relationship = getattr(self._object, relname, None)
        if relationship:
            if isinstance(relationship, ToOneRelationship):
                obj = relationship()
                if obj:
                    yield edge(guid(obj), self.guid())

            elif isinstance(relationship, ToManyRelationshipBase):
                for obj in relationship():
                    yield edge(guid(obj), self.guid())

    def getEdges(self):
        if self.impact_relationships is not None:
            for impact_relationship in self.impact_relationships:
                for impact in self.impact(impact_relationship):
                    yield impact

        if self.impacted_by_relationships is not None:
            for impacted_by_relationship in self.impacted_by_relationships:
                for impacted_by in self.impacted_by(impacted_by_relationship):
                    yield impacted_by


class BaseTriggers(object):
    implements(INodeTriggers)

    def __init__(self, adapted):
        self._object = adapted


class DockerContainerRelationsProvider(BaseRelationsProvider):
    # impact_relationships = ['docker_host']
    impacted_by_relationships = ['docker_host']

