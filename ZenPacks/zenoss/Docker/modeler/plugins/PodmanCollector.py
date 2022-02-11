##############################################################################
#
# Copyright (C) Zenoss, Inc. 2022, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Collects information about Podman Containers."""

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

from ZenPacks.zenoss.Docker import parsing
from ZenPacks.zenoss.Docker.utils import command_from_commands, results_from_result


class PodmanCollector(CommandPlugin):

    relname = "podman_containers"
    modname = "ZenPacks.zenoss.Docker.PodmanContainer"

    command = command_from_commands(
        "podman -v",
        "sudo podman ps -a --no-trunc",
        "cat /proc/self/mountinfo",
        )

    def process(self, device, results, log):
        log.info('Collecting podman containers for device %s' % device.id)
        # Change results into a list of of results. One element per command.

        results = results_from_result(results)

        maps = []

        # Map device "podman_version" property.
        if results[0].startswith("podman version"):
            log.info("%s: %s", device.id, results[0])
            maps.append(ObjectMap({'podman_version': results[0]}))
        else:
            log.info("%s: no podman version", device.id)
            maps.append(ObjectMap({"podman_version": None}))

        try:
            rows = parsing.rows_from_output(
                results[1],
                expected_columns=[
                    "CONTAINER ID",
                    "IMAGE",
                    "COMMAND",
                    "CREATED",
                    "PORTS",
                    "NAMES",
                    ])

        except parsing.MissingColumnsError:
            log.info("%s: unexpected podman ps output", device.id)
            return maps

        rm = self.relMap()
        maps.append(rm)

        if not rows:
            log.info("%s: no podman containers found", device.id)
            return maps

        try:
            cgroup_path = parsing.cgroup_path_from_output(results[2])
        except parsing.CgroupPathNotFound:
            log.info("%s: no cgroup path found. The default value '/sys/fs/cgroup' is set", device.id)
            cgroup_path = "/sys/fs/cgroup"

        for row in rows:
            rm.append(
                self.objectMap({
                    "id": row["CONTAINER ID"],
                    "title": row["NAMES"],
                    "image": row["IMAGE"],
                    "command": row["COMMAND"],
                    "created": row["CREATED"],
                    "ports": row["PORTS"],
                    "cgroup_path": cgroup_path,
                    }))

        log.info("%s: found %s Podman containers", device.id, len(rm.maps))
        log.info("Podman RM maps: %s", rm.maps)
        return maps
