##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""docker ps parser for Docker and Podman container performance data.

See tests for examples of the commands and their output.

"""

import logging
LOG = logging.getLogger("zen.Docker")

import re

from Products.ZenEvents import ZenEventClasses
from Products.ZenRRD.CommandParser import CommandParser

from ZenPacks.zenoss.Docker import parsing


# Some Docker versions show real and virtual size. Others only show real.
SIZE_MATCHERS = [
    re.compile(
        r'(?P<real_num>[\d\.]+)\s?(?P<real_units>\S+) '
        r'\(virtual (?P<virt_num>[\d\.]+)\s?(?P<virt_units>\S+)\)'
        ).match,

    re.compile(
        r'(?P<real_num>[\d\.]+)\s?(?P<real_units>\S+)'
        ).match,
    ]


class ps(CommandParser):

    createDefaultEventUsingExitCode = False

    def sendEventOnce(self, result, event):
        """Sent event, but only once per-device-per-cycle.

        This is useful for component parsers that need to raise events on the
        device rather than on the components.

        """
        if not hasattr(result, "sentEventSet"):
            result.sentEventSet = set()

        key = frozenset(event)
        if key in result.sentEventSet:
            # The event has already been added to result.
            return

        result.events.append(event)
        result.sentEventSet.add(key)

    def processResults(self, cmd, result):
        point_map = {p.id: p for p in cmd.points}

        engine_type = 'podman' if 'podman' in cmd.command else 'docker'
        ps_event = {
            "device": cmd.device,
            "component": "{}".format(engine_type),
            "eventKey": "{}-ps-status".format(engine_type),
            "eventClassKey": "{}-ps-status".format(engine_type),
            "{}_command".format(engine_type): cmd.command,
            "{}_output".format(engine_type): cmd.result.output,
            }

        try:
            rows = parsing.rows_from_output(
                cmd.result.output,
                expected_columns=[
                    "CONTAINER ID",
                    "STATUS",
                    ])

        except Exception:
            self.sendEventOnce(result, dict({
                "summary": "received unexpected output from {} ps".format(engine_type),
                "severity": ZenEventClasses.Error,
                }, **ps_event))

            return

        else:
            self.sendEventOnce(result, dict({
                "summary": "received expected output from {} ps".format(engine_type),
                "severity": ZenEventClasses.Clear,
                }, **ps_event))

        for row in rows:
            if row.get("CONTAINER ID", "") != cmd.component:
                continue

            status = row.get("STATUS", "").lower()
            if "up" in status or "created" in status:
                severity = ZenEventClasses.Clear
            else:
                severity = ZenEventClasses.Critical

            result.events.append({
                "device": cmd.device,
                "component": cmd.component,
                "summary": "container status: {}".format(status),
                "eventKey": "{}ContainerStatus".format(engine_type),
                "eventClassKey": "{}ContainerStatus".format(engine_type),
                "severity": severity,
                })

            # Optionally send container size datapoints.
            if "size" in point_map or "size_virtual" in point_map:
                for matcher in SIZE_MATCHERS:
                    match = matcher(row.get("SIZE", ""))
                    if match:
                        match_gd = match.groupdict()
                        size_dp = point_map.get("size")
                        if size_dp:
                            real_num = match_gd.get("real_num")
                            real_units = match_gd.get("real_units")

                            if real_num is not None:
                                result.values.append((
                                    size_dp,
                                    to_bytes(real_num, real_units)))

                        size_virtual_dp = point_map.get("size_virtual")
                        if size_virtual_dp:
                            virt_num = match_gd.get("virt_num")
                            virt_units = match_gd.get("virt_units")

                            if virt_num is not None:
                                result.values.append((
                                    size_virtual_dp,
                                    to_bytes(virt_num, virt_units)))

            # We found our component's row. Don't process more rows.
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
            return int(float(scaled_value) * factor)
        except Exception:
            pass
