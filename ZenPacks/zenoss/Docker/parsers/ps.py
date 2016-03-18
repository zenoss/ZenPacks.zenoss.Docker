##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""docker ps parser for Docker container performance data.

See tests for examples of the commands and their output.

"""

import logging
LOG = logging.getLogger("zen.Docker")

import re

from Products.ZenEvents import ZenEventClasses
from Products.ZenRRD.CommandParser import CommandParser


class ps(CommandParser):

    createDefaultEventUsingExitCode = False

    def processResults(self, cmd, result):
        point_map = {p.id: p for p in cmd.points}

        matcher_regex = (
            r'^{container_id}\|'
            r'(?P<status>[^\|]+)\|'
            r'(?P<real_num>[\d\.]+) (?P<real_units>\S+) '
            r'\(virtual (?P<virt_num>[\d\.]+) (?P<virt_units>\S+)\)'
            ).format(
                container_id=cmd.component)

        matcher = re.compile(matcher_regex)

        for line in cmd.result.output.strip().splitlines():
            match = matcher.match(line)
            if not match:
                continue

            # Create container up/down status events.
            status = match.group("status").lower()
            if "up" in status or "created" in status:
                severity = ZenEventClasses.Clear
            else:
                severity = ZenEventClasses.Critical

            result.events.append({
                "device": cmd.device,
                "component": cmd.component,
                "summary": "container status: {}".format(status),
                "eventKey": "dockerContainerStatus",
                "eventClassKey": "dockerContainerStatus",
                "severity": severity,
                })

            # Send container size datapoints.
            real_dp = point_map.get("size")
            if real_dp:
                result.values.append((
                    real_dp,
                    to_bytes(
                        match.group("real_num"),
                        match.group("real_units"))))

            virt_dp = point_map.get("size_virtual")
            if virt_dp:
                result.values.append((
                    virt_dp,
                    to_bytes(
                        match.group("virt_num"),
                        match.group("virt_units"))))

            break


def to_bytes(scaled_value, units):
    factors = {
        "B": 1.0,
        "KB": 1024.0,
        "MB": 1048576.0,
        "GB": 1073741824.0,
        "TB": 1099511627776.0,
        }

    factor = factors.get(units.upper())
    if factor:
        try:
            return float(scaled_value) * factor
        except Exception:
            pass
