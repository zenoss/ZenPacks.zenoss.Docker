##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

# stdlib Imports
import functools
import re
import unittest


# Zope Imports
from zope.component import subscribers

# Zenoss Imports
from Products.DataCollector.ApplyDataMap import ApplyDataMap
from Products.ZenUtils.guid.interfaces import IGUIDManager

# DynamicView Imports
try:
    from ZenPacks.zenoss.DynamicView import TAG_IMPACTED_BY, TAG_IMPACTS
    from ZenPacks.zenoss.DynamicView.interfaces import IRelatable
except ImportError:
    DYNAMICVIEW_INSTALLED = False
    TAG_IMPACTED_BY, TAG_IMPACTS, IRelatable = None
else:
    DYNAMICVIEW_INSTALLED = True

# Impact Imports
try:
    from ZenPacks.zenoss.Impact.impactd.interfaces import IRelationshipDataProvider
except ImportError:
    IMPACT_INSTALLED = False
    IRelationshipDataProvider = None
else:
    IMPACT_INSTALLED = True

from .. import zenpacklib

zenpacklib.enableTesting()


class DVITest(zenpacklib.TestCase):

    device_data = None
    expected_both = None
    expected_dynamicview_only = None
    expected_impact_only = None

    def afterSetUp(self):
        super(DVITest, self).afterSetUp()

        if self.device_data:
            self.devices = create_devices(self.dmd, self.device_data)
        else:
            self.fail("DVITest requires device_data to be set")

    @unittest.skipUnless(DYNAMICVIEW_INSTALLED, "DynamicView not installed")
    def test_DynamicView(self):
        expected = set.union(
            *map(triples_from_yuml, (
                self.expected_both,
                self.expected_dynamicview_only)))

        all_expected = complement_triples(expected)

        found = dynamicview_triples_from_devices(
            self.devices,
            tags=(TAG_IMPACTS, TAG_IMPACTED_BY))

        missing = all_expected - found
        extra = found - all_expected

        self.assertFalse(
            missing or extra,
            "DynamicView {}/{} relationship issue(s):\n\n{}".format(
                TAG_IMPACTED_BY, TAG_IMPACTS,
                yuml_from_triples(
                    expected,
                    missing=missing,
                    extra=extra,
                    tag_map={
                        TAG_IMPACTS: TAG_IMPACTED_BY,
                        })))

    @unittest.skipUnless(IMPACT_INSTALLED, "Impact not installed")
    def test_Impact_Edges(self):
        expected = set.union(
            *map(triples_from_yuml, (
                self.expected_both,
                self.expected_impact_only)))

        all_expected = complement_triples(expected)
        found = impact_triples_from_devices(self.devices)
        missing = all_expected - found
        extra = found - all_expected

        self.assertFalse(
            missing or extra,
            "Impact edges issue(s):\n\n{}".format(
                yuml_from_triples(
                    expected,
                    missing=missing,
                    extra=extra,
                    tag_map={
                        TAG_IMPACTS: TAG_IMPACTED_BY,
                        })))


def create_devices(dmd, device_data):
    devices = {}
    for device_id, data in device_data.items():
        devices[device_id] = create_device(dmd, device_id, data)

    return devices.values()


def create_device(dmd, device_id, data):
    device = dmd.Devices.findDeviceByIdExact(device_id)
    if not device:
        deviceclass = dmd.Devices.createOrganizer(data.get("deviceClass", "/"))
        deviceclass.setZenProperty("zPythonClass", data.get("zPythonClass", ""))
        device = deviceclass.createInstance(device_id)

    adm = ApplyDataMap()._applyDataMap
    map(lambda x: adm(device, x), data.get("dataMaps", []))

    return device


def id_from_obj(obj):
    device = obj.device()
    if device == obj:
        return obj.id
    else:
        return "{}/{}".format(device.id, obj.id)


def id_from_path_fn(dmd):
    def id_from_path(path):
        return id_from_obj(dmd.getObjByPath(path))

    return id_from_path


def id_from_guid_fn(dmd):
    guid_manager = IGUIDManager(dmd)

    def id_from_guid(guid):
        return id_from_obj(guid_manager.getObject(guid))

    return id_from_guid


def triples_from_device(device, fn):
    return reduce(set.union, map(fn, [device] + device.getDeviceComponents()))


def dynamicview_triples_from_obj(obj, tags=None):
    if not tags:
        raise ValueError("tags must be a list of DynamicView relationship tags")

    id_from_path = id_from_path_fn(obj.getDmd())

    relatable = IRelatable(obj)

    triples = set()
    for tag in tags:
        for relation in relatable.relations(type=tag):
            triples.add((
                id_from_path(relation.source.id),
                tag,
                id_from_path(relation.target.id)))

    return triples


def dynamicview_triples_from_device(device, tags=None):
    return triples_from_device(
        device,
        functools.partial(dynamicview_triples_from_obj, tags=tags))


def dynamicview_triples_from_devices(devices, tags=None):
    return set.union(
        *[dynamicview_triples_from_device(x, tags=tags) for x in devices])


def impact_triples_from_obj(obj):
    id_from_guid = id_from_guid_fn(obj.getDmd())

    obj_id = id_from_obj(obj)

    triples = set()
    for subscriber in subscribers([obj], IRelationshipDataProvider):
        for edge in subscriber.getEdges():
            impacted_id = id_from_guid(edge.impacted)
            source_id = id_from_guid(edge.source)
            if source_id == obj_id:
                triples.add((obj_id, TAG_IMPACTS, impacted_id))
            elif impacted_id == obj_id:
                triples.add((obj_id, TAG_IMPACTED_BY, source_id))
            else:
                # No else. In practice we don't have an object's
                # IRelationshipDataProvider provide relationships that
                # don't have the object terminating one side of the
                # edge because it's too easy for the edge to not be
                # updated when the object is updated.
                pass

    return triples


def impact_triples_from_device(device):
    return triples_from_device(device, impact_triples_from_obj)


def impact_triples_from_devices(devices):
    return set.union(*map(impact_triples_from_device, devices))


def triples_from_yuml(yuml):
    triples = set()

    if not yuml:
        return triples

    line_matcher = re.compile(
        r"^\s*"
        r"\[(?P<source>[^\]]+)\]"
        r"(?P<connector>[^\[]+)"
        r"\[(?P<target>[^\]]+)\]"
        r"\s*$").search

    for line in yuml.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue

        match = line_matcher(line)
        if match:
            source, connector, target = match.groups()
            if connector == "->":
                triples.add((source, TAG_IMPACTS, target))
            else:
                raise ValueError(
                    "{!r} unsupported connector in {!r}"
                    .format(connector, line))
        else:
            raise ValueError(
                "{!r} isn't a recognized YUML line"
                .format(line))

    return triples


def complement_triple(triple, tag_map=None):
    if tag_map is None:
        tag_map = {
            TAG_IMPACTS: TAG_IMPACTED_BY,
            TAG_IMPACTED_BY: TAG_IMPACTS,
            }

    source, tag, target = triple
    complemented_tag = tag_map.get(tag)
    if complemented_tag:
        return (target, complemented_tag, source)


def complement_triples(triples, tag_map=None):
    complemented_triples = set()
    for triple in triples:
        complemented_triples.add(triple)

        complemented_triple = complement_triple(triple, tag_map)
        if complemented_triple:
            complemented_triples.add(complemented_triple)

    return complemented_triples


def yuml_from_triples(triples, missing=None, extra=None, tag_map=None):
    missing = set() if missing is None else missing
    extra = set() if extra is None else extra

    def filter_triples(ts):
        if tag_map:
            return {t for t in ts if t[1] in tag_map}
        else:
            return ts

    def symbol_for_triple(triple):
        if triple in missing:
            return "XXX"
        elif triple in extra:
            return "!!!"
        else:
            return ""

    lines = []
    for triple in filter_triples(triples | extra):
        source, tag, target = triple

        left = symbol_for_triple(triple)

        if tag in tag_map:
            right = symbol_for_triple(complement_triple(triple))
        else:
            right = ""

        middle = "-.-" if any((left, right)) else "-"

        lines.append(
            "[{}]{}{}{}>[{}]".format(
                source, left, middle, right, target))

    return "\n".join(sorted(lines))


def impact_yuml_from_device(device):
    triples = impact_triples_from_device(device)
    complemented_triples = complement_triples(
        triples,
        tag_map={
            TAG_IMPACTS: TAG_IMPACTED_BY,
            TAG_IMPACTED_BY: TAG_IMPACTS,
            })

    return yuml_from_triples(
        triples,
        missing=complemented_triples - triples,
        tag_map={
            TAG_IMPACTS: TAG_IMPACTED_BY,
            })
