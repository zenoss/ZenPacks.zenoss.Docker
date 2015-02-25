##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from pprint import pformat

from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.ZenRRD.CommandParser import ParsedResults
from Products.ZenRRD.tests.BaseParsersTestCase \
    import createPoints, filenames


class Object(object):
    exitCode = 0

    def __repr__(self):
        return pformat(dict(
            (attr, getattr(self, attr))
            for attr in dir(self)
            if not attr.startswith('__')
        ))

class BaseParsersTestCase(BaseTestCase):

    def _testParser(self, parserMap, filename, component=None):

        # read the data file
        with open(filename) as datafile:
            command = datafile.readline().rstrip("\n")
            output = "".join(datafile.readlines())

        # read the file containing the expected values
        with  open('%s.py' % (filename,)) as expectedfile:
            expected = eval("".join(expectedfile.readlines()))

        results = ParsedResults()
        Parser = parserMap.get(command)

        if Parser:
            parser = Parser()
        else:
            self.fail("No parser for %s" % command)

        cmd = Object()
        cmd.points = createPoints(expected, parser)
        cmd.result = Object()
        cmd.result.output = output
        cmd.result.stderr = None
        cmd.component = component

        parser.processResults(cmd, results)

        self.assertEqual(len(cmd.points), len(results.values),
            "%s expected %s values, actual %s" % (filename, len(cmd.points),
            len(results.values)))

        counter = 0

        for expected, actual in results.values:
            expectedValue = expected.expected
            msg = '%s: %s expected %s but parsed out %s' % (
                   filename, expected.id, expectedValue, actual)
            self.assertEqual(expectedValue, actual, msg)
            counter += 1

        return counter


    def _testParsers(self, datadir, parserMap, component=None):
        """
        Test all of the parsers that have test data files in the data
        directory.
        """
        counter = 0

        for filename in filenames(datadir):
            counter += self._testParser(parserMap, filename, component)

        print "testParsers made", counter, "assertions."
