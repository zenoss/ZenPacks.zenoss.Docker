'''
Collects information about Docker Containers.
'''

import collections
from itertools import chain
import re

from Products.ZenUtils.Utils import prepId
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap


class DockerCollector(CommandPlugin):
    """
    Modeler plugin for Docker
    """

    def condition(self, device, log):
        return True

    command = (
        # 'docker ps -a -s --no-trunc' may cause timeout on large count of containers
        'docker -v && docker ps -a --no-trunc'
    )

    def process(self, device, results, log):
        log.info('Collecting docker containers for device %s' % device.id)

        if not "CONTAINER" in results:
            log.error("Cann't parse output. "
                "Check that Docker installed "
                "and you have permissions to use it."
            )

        maps = collections.OrderedDict([
            ('docker_containers', []),
            ('device', []),
        ])

        maps['device'].append(ObjectMap({
            'docker_version': results.splitlines()[0]
        }))

        oms = []
        for line in results.splitlines()[2:]:
            bits = [x.strip() for x in \
                filter(lambda x: x.strip(), line.split("   "))]

            if len(bits) == 7:
                container_state = bits[4]
                ports = bits[5]
                title = bits[6]
            elif len(bits) == 6: # No Ports
                ports = ""
                container_state = bits[4]
                title = bits[5]
            elif len(bits) == 5: # No Status & Ports, probably not running or error
                ports = ""
                container_state = ""
                title = bits[4]
            else:
                log.error("Bad format of docker ps output.")
                log.error(bits)
                continue

            oms.append(ObjectMap({
                "id": bits[0],
                "title": title,
                "image": bits[1],
                "command": bits[2],
                "created": bits[3],
                "container_state": bits[4],
                "ports": ports,
                "size": "N/A"
                }))

        maps["docker_containers"].append(RelationshipMap(
            relname='docker_containers',
            modname='ZenPacks.zenoss.Docker.DockerContainer',
            objmaps=oms))

        return list(chain.from_iterable(maps.itervalues()))
