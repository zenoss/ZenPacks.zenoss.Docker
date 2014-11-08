"""
Docker container status parser
"""

import logging
log = logging.getLogger("zen.DockerContainerStatus")

import zope.interface

from Products.ZenRRD.CommandParser import CommandParser
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.ZenCollector.interfaces import ICollector


class container_status(CommandParser):
    """
    Datasource for Docker components
    """

    def processResults(self, cmd, result):

        created = ""
        container_state= "N/A"

        if cmd.result.stderr:
            log.debug('No received data about status for Docker Container %s' % cmd.component)
            return result

        lines = cmd.result.output.splitlines()
        for line in lines:
            if cmd.component in line:
                bits = [x.strip() for x in \
                    filter(lambda x: x.strip(), line.split("  "))]
                created = bits[3]
                container_state = bits[4]
                break

        maps = [ObjectMap({
            "compname": 'docker_containers/%s' % cmd.component,
            "modname": 'DockerContainer',
            "created": created,
            "container_state": container_state
        })]
        self.apply_maps(cmd, maps=maps)

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
