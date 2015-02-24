"""
Docker container status parser
"""

import logging
log = logging.getLogger("zen.DockerContainerStatus")

import zope.interface

from Products.ZenRRD.CommandParser import CommandParser
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.ZenCollector.interfaces import ICollector
from Products.ZenEvents import ZenEventClasses

CUT_SEPARATOR = '--cut--'


class container_status(CommandParser):
    """
    Datasource for Docker components
    """

    def processResults(self, cmd, result):

        created = ""
        container_state= "Down"
        ports = ""
        size = ""
        size_used = ""
        size_free = ""
        size_used_percents = ""

        if cmd.result.stderr:
            log.warning('No received data about status for '
                'Docker Container %s' % cmd.component)
            return result

        statuses_info, sizes_info = cmd.result.output.split(CUT_SEPARATOR)

        for line in statuses_info.splitlines():
            if cmd.component in line:
                bits = [x.strip() for x in \
                    filter(lambda x: x.strip(), line.split("   "))]
                created = bits[3]
                container_state = bits[4]
                if len(bits) == 7:
                    ports = bits[5]
                break

        for line in sizes_info.splitlines():
            if ' /' in line:
                bits = line.split()
                size = bits[1]
                size_used = bits[2]
                size_free = bits[3]
                size_used_percents = bits[4]
                break

        if not ("up" in container_state.lower()):
            result.events.append(dict(
                severity=ZenEventClasses.Error,
                summary="Container status is " + container_state,
                eventClassKey='docker_error',
                eventClass='/Status',
                component=cmd.component
            ))
        else:
            result.events.append(dict(
                severity=ZenEventClasses.Clear,
                summary="Container status is Up",
                eventClassKey='docker_error',
                eventClass='/Status',
                component=cmd.component
            ))

        om_data = {
            "compname": 'docker_containers/%s' % cmd.component,
            "modname": 'DockerContainer',
            "created": created,
            "container_state": container_state,
            "ports": ports
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
