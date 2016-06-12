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
of the tests/parserdata/ directory.

Example contents of tests/parserdata/:

    parserdata
    └── zendev
        ├── capture
        ├── cgroupfs
        │   ├── blkio
        │   ├── blkio.expected
        │   ├── cpuacct
        │   ├── cpuacct.expected
        │   ├── memory
        │   └── memory.expected
        └── ps
            ├── ps
            └── ps.expected

Each first level directory under parserdata represents a seprate device or
configuration from which sample data has been collected. The name should be
something that would be a valid Python function name because it will be made
into part of a test method's name.

Each directory within the device directory is the name of a parser. This must
match the filename (except the .py part) of a file within the ZenPack's
parsers/ directory.

Each file without a file extension (.???) within the parser directory is the
name of a datasource that uses the parser, and this file should contain the
output of running the commandTemplate for that datasource.

There must be a <datasource>.expected file for each <datasource> file. This
expected file must contain the events and values that are expected to be parsed
from the <datasource> file. Its syntax is Python, and an example follows:

    {
        "events": [{
            "device": "zendev",
            "component": "6bd90ce97a472f1f7d315c43dfaa3e2c3d2828e53ece937cf47a5ec7412b3976",
            "summary": "container status: up 24 hours",
            "severity": 0,
            "eventClassKey": "dockerContainerStatus",
            "eventKey": "dockerContainerStatus",
        }],
        "values": {
            "6bd90ce97a472f1f7d315c43dfaa3e2c3d2828e53ece937cf47a5ec7412b3976": {
                "size": 2267021.312,
                "size_virtual": 2423435296.768,
            },
        },
    }

"""

import Globals  # noqa: imported only for side effects

import importlib
import os
import re
import unittest

from Products.ZenRRD.CommandParser import ParsedResults


class ParserTests(unittest.TestCase):
    """Dynamic parsers test case.

    Test methods are automatically added by the add_checks function below. See
    the module's docstring for details.

    """

    # We do big list and dict diffs and don't want them truncated.
    maxDiff = None


class Object(object):
    pass


class Context(object):
    def __init__(self, key):
        self.key = key

    def __getattr__(self, name):
        return self.key


def zenpack_name():
    """Return the fully-qualified name of the ZenPack containing this file."""
    zenpack_match = re.compile(r'^ZenPacks\.([^\.]+)\..*$').match
    for part in os.path.abspath(__file__).split("/")[::-1]:
        if zenpack_match(part):
            return part


def parser_check_fn(parser_name, datasource, device, components, output, expected):
    """Return a parser test method that closes over our args.

    This function must not have "test" in its name or some testing frameworks
    like nose will discover it as a test and attempt to execute it with no
    arguments.

    """
    def parser_test(self):
        if expected is None:
            self.fail(
                "missing or bad: {}/{}/{}.expected".format(
                    device,
                    parser_name,
                    datasource))

        expected_events = expected.get("events", [])
        expected_values = expected.get("values", {})

        if not expected_events and not expected_values:
            self.fail(
                "no events or values: {}/{}/{}.expected".format(
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


def add_checks():
    """Add tests to ParserTests from contents of parserdata/ directory."""
    testdata_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "parserdata"))

    for root, dirs, files in os.walk(testdata_dir):
        relative_root = os.path.relpath(root, testdata_dir)

        try:
            device, parser_name = relative_root.split("/")
        except Exception:
            continue

        for filename in files:
            if "." in filename:
                continue

            datasource = filename

            path = os.path.join(root, filename)

            # Check if there are expected results.
            expected_filename = "{}.expected".format(path)
            try:
                with open(expected_filename, "r") as expected_file:
                    expected = eval(expected_file.read())
            except Exception:
                components = output = expected = None
            else:
                # Gather expected component ids from expected events.
                components = {
                    e.get("component")
                    for e in expected.get("events", [])
                    if e.get("component")}

                # Add components ids from expected values.
                components.update(c for c in expected.get("values", {}))

                # Read the test output data.
                with open(path, "r") as output_file:
                    output = output_file.read()

            # Add test_<parser>_<datasource>_<device> method to ParserTests.
            setattr(
                ParserTests,
                "test_{}_{}_{}".format(parser_name, datasource, device),
                parser_check_fn(
                    parser_name,
                    datasource,
                    device,
                    components,
                    output,
                    expected))


add_checks()


if __name__ == '__main__':
    unittest.main()
