##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################


import os

from .BaseParsersTestCase import BaseParsersTestCase

from Products.ZenRRD.parsers.uptime import uptime
from ZenPacks.zenoss.Docker.parsers.docker.container_status \
    import container_status
from ZenPacks.zenoss.Docker.parsers.docker.docker_usage \
    import docker_usage


class DockerParsersTestCase(BaseParsersTestCase):

    def testParsers(self):
        """
        Test all of the parsers that have test data files in the data
        directory.
        """
        datadir = "%s/parserdata/docker" % os.path.dirname(__file__)

        container_status.apply_maps = lambda x, y, maps: True

        parserMap = {
            "/usr/bin/docker ps --no-trunc && echo '--cut--'"
                " && docker exec {here/id} df -h 2> /dev/null": container_status,
            "/usr/bin/test -f "
                "/sys/fs/cgroup/cpuacct/docker/${here/id}/cpuacct.stat"
                " && /bin/grep '.'"
                " /sys/fs/cgroup/cpuacct/docker/${here/id}/cpuacct.stat || echo '0'": docker_usage
        }
        self._testParsers(datadir, parserMap, \
            component='b611ec9c33826c35eb316397942421b04e4e3af7bacc4bfe40c420d6788dee90')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(DockerParsersTestCase))
    return suite
