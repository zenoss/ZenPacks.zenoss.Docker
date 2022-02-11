##############################################################################
#
# Copyright (C) Zenoss, Inc. 2022, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Additional function for docker and podman commands output parsing."""


def command_from_commands(*commands):
    """Return a single command given an iterable of commands.

    The results of each command will be separated by __SPLIT__, and the
    results will contain only the commands' stdout.

    """
    return " ; echo __SPLIT__ ; ".join("{} 2>/dev/null".format(c) for c in commands)


def results_from_result(result):
    """Return results split into a list of per-command output."""
    try:
        return [r.strip() for r in result.split("__SPLIT__")]
    except Exception:
        return []
