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
        'docker ps -a'
    )

    def process(self, device, results, log):
        log.info('Collecting docker containers for device %s' % device.id)

        maps = collections.OrderedDict([
            ('docker_containers', []),
        ])

        # TODO: parse results
        print results

        return list(chain.from_iterable(maps.itervalues()))
