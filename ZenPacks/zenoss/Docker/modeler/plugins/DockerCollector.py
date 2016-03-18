##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Collects information about Docker Containers."""

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap


def command_from_commands(*commands):
    """Return a single command given an iterable of commands.

    The results of each command will be separated by __SPLIT__, and the
    results will contain the commands stdout and stderr.

    """
    return " ; echo __SPLIT__ ; ".join("{} 2>&1".format(c) for c in commands)


def results_from_result(result):
    """Return results split into a list of per-command output."""
    try:
        return [r.strip() for r in result.split("__SPLIT__")]
    except Exception:
        return []


class DockerCollector(CommandPlugin):

    relname = "docker_containers"
    modname = "ZenPacks.zenoss.Docker.DockerContainer"

    command = command_from_commands(
        "docker -v",
        "sudo docker ps -a --no-trunc",
        )

    def process(self, device, results, log):
        log.info('Collecting docker containers for device %s' % device.id)

        # Change results into a list of of results. One element per command.
        results = results_from_result(results)

        maps = []

        # Map device "docker_version" property.
        if results[0].startswith("Docker version"):
            maps.append(
                ObjectMap({
                    'docker_version': results[0],
                    }))
        else:
            log.info("%s: no docker version: %s", device.id, results[0])

        # Map containers.
        if results[1].startswith("CONTAINER"):
            rm = self.relMap()
            for line in results[1].splitlines()[1:]:
                bits = [x.strip() for x in \
                    filter(lambda x: x.strip(), line.split("   "))]

                # Full output.
                if len(bits) == 7:
                    ports = bits[5]
                    title = bits[6]

                # No ports.
                elif len(bits) == 6:
                    ports = ""
                    title = bits[5]

                # No status or ports. Probably not running, or in error.
                elif len(bits) == 5:
                    ports = ""
                    title = bits[4]

                else:
                    log.error(
                        "%s: unrecognized docker ps output line: %s",
                        device.id,
                        line)

                    continue

                rm.append(
                    self.objectMap({
                        "id": bits[0],
                        "title": title,
                        "image": bits[1],
                        "command": bits[2],
                        "created": bits[3],
                        "ports": ports,
                        }))

            maps.append(rm)

        else:
            log.info("%s: no docker containers: %s", device.id, results[1])

        return maps
