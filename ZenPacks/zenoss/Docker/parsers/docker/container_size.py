"""
Docker container size parser
"""

import logging
log = logging.getLogger("zen.DockerContainerSize")

import zope.interface

from Products.ZenRRD.CommandParser import CommandParser
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.ZenCollector.interfaces import ICollector
from Products.ZenEvents import ZenEventClasses


class container_size(CommandParser):
    """
    Datasource for Docker components
    """

    def processResults(self, cmd, result):

        size = ""
        size_used = ""
        size_free = ""
        size_used_percents = ""

        if cmd.result.stderr:
            log.warning('No received data about size for '
                'Docker Container %s' % cmd.component)
            return result

        for line in cmd.result.output.splitlines():
            if ' /' in line:
                bits = line.split()
                size = bits[1]
                size_used = bits[2]
                size_free = bits[3]
                size_used_percents = bits[4]
                break

        om_data = {
            "compname": 'docker_containers/%s' % cmd.component,
            "modname": 'DockerContainer',
        }

        if size:
            om_data.update({
                "size": size,
                "size_used": size_used,
                "size_free": size_free,
                "size_used_percents": size_used_percents
            })

        self.apply_maps(cmd, maps=[ObjectMap(om_data)])
        return result

    def apply_maps(self, cmd, maps=[]):
        """
        Call remote CommandPerformanceConfig instance to apply maps.

        @param cmd: cmd instance
        @type cmd: instance
        @param maps: list of RelationshipMap|ObjectMap
        @type maps: list
        @param state: health state of the component (Normal or Dead)
        @type state: str
        @return: None
        """

        collector = zope.component.queryUtility(ICollector)
        remoteProxy = collector.getRemoteConfigServiceProxy()

        dev_id = cmd.deviceConfig.configId
        changed = remoteProxy.callRemote('applyDataMaps', dev_id, maps)
        changed.addBoth(
            lambda msg: self.callback(cmd.component, msg)
        )

    def callback(self, comp, message):
        """Called for suppressing unhandled errors in Deferred"""
        # If necessary, can be be extended with additional functionality,
        # for example creating event or log
