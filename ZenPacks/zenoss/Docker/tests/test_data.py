#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Tests for COMMAND datasource parsers in ZenPack's parsers/ directory.

Tests are dynamically added to the ParserTests TestCase based on the contents
of tests/data/*/parsers/ directories.

Example contents of tests/data/:

    data
    └── 1.10.3-coreos-1010.5.0
        └── parsers
            ├── cgroupfs
            │   ├── cpuacct
            │   ├── cpuacct.expected
            │   ├── memory
            │   └── memory.expected
            └── ps
                ├── size
                ├── size.expected
                ├── status
                └── status.expected

Each first level directory under data represents a separate device or
configuration from which sample data has been collected. Within each device
directory must be a parsers/ directory.

Under each */parsers/ directory must be a directory with the name of a parser
from the ZenPack's main parsers/ directory. Within each of these directories
name after a parser must be a pair of files per datasource to be tested. The
first file should be named the same as a datasource using the parser, and a
file by the same name with a .expected extension.

The file named after the datasource should contain the raw output captured from
running the datasource's commandTemplate command on a test system. The same
filename with the .expected extension describes the data expected to be parsed
from that output. The syntax of the .expected file is YAML, and an example
follows:

    events:
      - device: "zendev"
        component: "6bd90ce97a472f1f7d315c43dfaa3e2c3d2828e53ece937cf47a5ec7412b3976"
        summary: "container status: up 24 hours"
        severity: 0
        eventClassKey: "dockerContainerStatus"
        eventKey: "dockerContainerStatus"

    values:
      6bd90ce97a472f1f7d315c43dfaa3e2c3d2828e53ece937cf47a5ec7412b3976:
        size: 2267021.312
        size_virtual: 2423435296.768

"""

import Globals  # noqa: imported only for side effects

import importlib
import logging
import os
import re
import unittest

import yaml

from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap
from Products.ZenRRD.CommandParser import ParsedResults


class ModelerTests(unittest.TestCase):
    """Dynamic modelers test case.

    Test methods are automatically added by the add_checks function below. See
    the module's docstring for details.

    """

    # We do big list and dict diffs and don't want them truncated.
    maxDiff = None


class ParserTests(unittest.TestCase):
    """Dynamic parsers test case.

    Test methods are automatically added by the add_checks function below. See
    the module's docstring for details.

    """

    # We do big list and dict diffs and don't want them truncated.
    maxDiff = None


def add_checks():
    """Add tests from contents of data/ directory."""
    data_dir = local_dir("data")

    file_filter = lambda x: not any([
        x.startswith("."),
        x.endswith(".expected")])

    for root, dirs, files in os.walk(data_dir):
        path_parts = os.path.relpath(root, data_dir).split(os.sep)
        path_len = len(path_parts)
        if path_len < 2:
            continue

        device_name, data_type = path_parts[:2]

        if data_type == "modelers" and path_len == 2:
            testcase = ModelerTests
        elif data_type == "parsers" and path_len == 3:
            testcase = ParserTests
            parser_name = path_parts[2]
        else:
            continue

        for filename in filter(file_filter, os.listdir(root)):
            if data_type == "modelers":
                add_modeler_check(
                    testcase,
                    root,
                    filename,
                    device_name)

            elif data_type == "parsers":
                add_parser_check(
                    testcase,
                    root,
                    filename,
                    device_name,
                    parser_name)


def add_modeler_check(testcase, root, filename, device_name):
    modeler_name = filename
    path = os.path.join(root, filename)

    # Initialize mock DeviceProxy.
    device = Object()
    device.id = device_name

    # Check if there are expected results.
    expected = load_expected(path)
    if expected:
        for k, v in expected.get("device", {}).items():
            setattr(device, k, v)

        command = expected.get("command")
        expected = expected.get("expected")
        output = load_output(path)
    else:
        expected = command = output = None

    # Add test_<modeler>_<device> method to testcase.
    setattr(
        testcase,
        "test_{}_{}".format(modeler_name, device_name),
        modeler_check_fn(
            modeler_name,
            device,
            command,
            output,
            expected))


def modeler_check_fn(modeler_name, device, command, output, expected):
    """Return a modeler test method that closes over our args.

    This function must not have "test" in its name or some testing frameworks
    like nose will discover it as a test and attempt to execute it with no
    arguments.

    """
    def modeler_test(self):
        if expected is None:
            self.fail(
                "missing or bad: {}/modelers/{}.expected".format(
                    device.id,
                    modeler_name))

        if not expected:
            self.fail(
                "no datamaps: {}/modelers/{}.expected".format(
                    device.id,
                    modeler_name))

        modeler_module = importlib.import_module(
            ".modeler.plugins.{}".format(modeler_name),
            zenpack_name())

        modeler_class = getattr(modeler_module, modeler_name.split('.')[-1])
        modeler = modeler_class()

        self.assertEqual(command, modeler.command)

        actual = modeler.process(
            device,
            output,
            logging.getLogger("zen.ZenModeler"))

        self.assertEqual(expected, comparable_from_actual(actual))

    return modeler_test


def comparable_from_actual(actual):
    """Return something comparable give the return of a modeler's process."""
    if actual is None:
        return actual

    if isinstance(actual, ObjectMap):
        comparable = {}
        for k, v in actual.__dict__.items():
            if k in {"_attrs"}:
                pass  # drop these all of the time
            elif not v and k in {"classname", "compname"}:
                pass  # drop these if the value is falsey
            else:
                comparable[k] = v

        return comparable

    if isinstance(actual, RelationshipMap):
        comparable = {}
        for k, v in actual.__dict__.items():
            if k == "maps":
                comparable[k] = comparable_from_actual(v)
            elif not v and k in ("classname", "compname", "parentId"):
                pass  # drop these if the value is falsey
            else:
                comparable[k] = v

        return comparable

    if isinstance(actual, list):
        return [comparable_from_actual(x) for x in actual]


def add_parser_check(testcase, root, filename, device_name, parser_name):
    datasource = filename
    path = os.path.join(root, filename)

    # Check if there are expected results.
    expected = load_expected(path)
    if expected:
        # Gather expected component ids from expected events.
        components = {
            e.get("component")
            for e in expected.get("events", [])
            if e.get("component")}

        # Add components ids from expected values.
        components.update(c for c in expected.get("values", {}))

        # Read the test output data.
        output = load_output(path)
    else:
        expected = components = output = None

    # Add test_<parser>_<datasource>_<device> method to testcase.
    setattr(
        testcase,
        "test_{}_{}_{}".format(parser_name, datasource, device_name),
        parser_check_fn(
            parser_name,
            datasource,
            device_name,
            components,
            output,
            expected))


def parser_check_fn(parser_name, datasource, device, components, output, expected):
    """Return a parser test method that closes over our args.

    This function must not have "test" in its name or some testing frameworks
    like nose will discover it as a test and attempt to execute it with no
    arguments.

    """
    def parser_test(self):
        if expected is None:
            self.fail(
                "missing or bad: {}/parsers/{}/{}.expected".format(
                    device,
                    parser_name,
                    datasource))

        expected_events = expected.get("events", [])
        expected_values = expected.get("values", {})

        if not expected_events and not expected_values:
            self.fail(
                "no events or values: {}/parsers/{}/{}.expected".format(
                    device,
                    parser_name,
                    datasource))

        parser_module = importlib.import_module(
            ".parsers.{}".format(parser_name),
            zenpack_name())

        parser_class = getattr(parser_module, parser_name)
        parser = parser_class()

        results = ParsedResults()

        for component in components:
            cmd = Object()
            cmd.device = device
            cmd.ds = datasource
            cmd.command = expected.get("command", "")
            cmd.component = component
            cmd.points = []
            cmd.result = Object()
            cmd.result.output = output

            for dp, v in expected_values.get(component, {}).items():
                point = Object()
                point.id = dp
                point.component = component
                point.data = parser.dataForParser(Context(component), None)
                point.expected = v
                cmd.points.append(point)

            parser.processResults(cmd, results)

        self.assertItemsEqual(expected_events, results.events)

        actual_values = {}

        for point, value in results.values:
            if point.component not in actual_values:
                actual_values[point.component] = {}

            actual_values[point.component][point.id] = value

        self.assertEqual(expected_values, actual_values)

    return parser_test


class Object(object):
    """Used for mocking up objects."""


class Context(object):
    """Used for mocking up context type objects."""

    def __init__(self, key):
        self.key = key

    def __getattr__(self, name):
        return self.key


def local_dir(*args):
    """Return absolute path to the directory containing this file.

    Any provided arguments will be os.path.joined to the end of the path.

    """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *args)


def zenpack_name():
    """Return the fully-qualified name of the ZenPack containing this file."""
    matcher = re.compile(r'^(ZenPacks\.([^\.]+)\.[^\-]+)').search
    for part in local_dir().split(os.sep):
        match = matcher(part)
        if match:
            return match.group(1)


def load_output(path):
    """Return contents of output file at path.

    Returns None if there's any problem loading the file.

    """
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception:
        return None


def load_expected(path):
    """Return contents of .expected file for path.

    Returns None if there's any problem loading the file.

    """
    try:
        with open("{}.expected".format(path), "r") as expected_file:
            return yaml.load(expected_file)
    except Exception:
        return None


add_checks()


if __name__ == '__main__':
    unittest.main()
