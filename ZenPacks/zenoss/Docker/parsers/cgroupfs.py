##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""cgroupfs parser for Docker container performance data.

See tests for examples of the commands and their output.


"""

import logging
LOG = logging.getLogger("zen.Docker")

import collections
import re

from Products.ZenRRD.CommandParser import CommandParser


PEBIBYTE = pow(1024, 5)


def process_cpuacct(data):
    values = {}

    # cpuacct_processes
    cgroup_procs = data.get("cgroup.procs")
    if cgroup_procs:
        values["processes"] = len(cgroup_procs)

    # cpu_count is required for all other datapoints. The cpuacct.usage_percpu
    # file has a single line with usage nanoseconds for each CPU separated by
    # spaces. We can get the count of CPUs by counting the length of splitting
    # that string.
    cpu_count = len(" ".join(data.get("cpuacct.usage_percpu", [])).split())
    if not cpu_count:
        return values

    # cpuacct_usage
    cpuacct_usage = data.get("cpuacct.usage")
    if cpuacct_usage:
        try:
            # cpuacct.usage is nanoseconds of CPU time used across all CPUs
            # since the system booted or the value was reset. To get to a
            # 0-100 percentage value we must first divide by number of CPUs,
            # then by 1e7 to convert from nanoseconds to centiseconds. It's
            # important to divide by 10000000 instead of 1e7 so the value will
            # remain an integer instead of a float. At least in Zenoss 4 a
            # DERIVE datapoint must be recorded as an integer.
            values["usage"] = int(cpuacct_usage[0]) / cpu_count / 10000000
        except Exception:
            pass

    # cpuacct_user & cpuacct_system
    cpuacct_stat = data.get("cpuacct.stat")
    if cpuacct_stat:
        for line in cpuacct_stat:
            try:
                name, value = line.split()
            except Exception:
                pass
            else:
                try:
                    # The values in cpuacct.stat are already scaled to
                    # centiseconds. They only need to be scaled by number of
                    # CPUs.
                    values["usage_{}".format(name)] = int(value) / cpu_count
                except Exception:
                    pass

    return values


def process_memory(data):
    values = {}

    # memory_usage
    usage_in_bytes = data.get("memory.usage_in_bytes")
    if usage_in_bytes:
        try:
            values["usage"] = int("".join(usage_in_bytes))
        except Exception:
            pass

    # memory_limit
    limit_in_bytes = data.get("memory.limit_in_bytes")
    if limit_in_bytes:
        try:
            value = int("".join(limit_in_bytes))
        except Exception:
            pass
        else:
            # "Very large values" are reported when there is no memory limit
            # for the cgroup. I've seen this as equal to Python's sys.maxint,
            # but it may be lower on some systems. A pebibyte of memory seems
            # like a reasonable upper limit for now.
            if value <= PEBIBYTE:
                values["limit"] = value

    return values


def process_blkio(data):
    values = collections.defaultdict(int)

    def extract_values(filename, datapoint_prefix):
        lines = data.get(filename)
        if lines:
            for line in lines:
                try:
                    _, name, value = line.split()
                except Exception:
                    pass
                else:
                    datapoint_id = "{}_{}".format(
                        datapoint_prefix,
                        name.lower())

                    try:
                        values[datapoint_id] += int(value)
                    except Exception:
                        pass

    extract_values("blkio.io_service_bytes_recursive", "bytes")
    extract_values("blkio.io_serviced_recursive", "io")

    return values


PROCESSORS = {
    "cpuacct": {
        "fn": process_cpuacct,
        "files": [
            "cgroup.procs",
            "cpuacct.usage_percpu",
            "cpuacct.usage",
            "cpuacct.stat",
            ],
        },

    "memory": {
        "fn": process_memory,
        "files": [
            "memory.usage_in_bytes",
            "memory.limit_in_bytes",
            ],
        },

    "blkio": {
        "fn": process_blkio,
        "files": [
            "blkio.io_service_bytes_recursive",
            "blkio.io_serviced_recursive",
            ],
        },
    }


def get_processor_fn(datasource_id):
    return PROCESSORS.get(datasource_id, {}).get("fn")


def get_processor_files(datasource_id):
    return PROCESSORS.get(datasource_id, {}).get("files")


class cgroupfs(CommandParser):

    createDefaultEventUsingExitCode = False

    def processResults(self, cmd, result):
        # Sort the output into a more accessible data structure.
        data = self.dataFromLines(cmd.ds, cmd.component, cmd.result.output)

        # Extract values from the data.
        values = self.valuesFromData(data, cmd.ds)

        # Record values in result to be stored and thresholded.
        point_map = {p.id: p for p in cmd.points}
        result.values.extend(
            (point_map[p_id], v)
            for p_id, v in values.items()
            if p_id in point_map)

    def valuesFromData(self, data, datasource_id):
        processor_fn = get_processor_fn(datasource_id)
        if processor_fn:
            return processor_fn(data)
        else:
            return {}

    def dataFromLines(self, datasource_id, component_id, output):
        """Return a useful data structure given command output.

        Example args:

            datasource_id = "cpuacct"
            component_id = "d4c0ab10352cd990baadc397672da9644ff417743c7a33f5e6077803e5f18301"
            output = ... tons of stuff, see tests ...

        Example return value:

            {
                "cgroup.procs": ["28841", "28846", "30104", "30280"],
                "cpuacct.usage_percpu": ["2086397238 2847429450"],
                "cpuacct.usage: ["142426945994"],
                "cpuacct.stat": ["user 10488", "system 3241"],
            }

        """
        processor_files = get_processor_files(datasource_id)
        if not processor_files:
            return {}

        path_regex = (
            r'^/sys/fs/cgroup/{datasource_id}'
            r'/(?:docker/|system\.slice/docker-)'
            r'{component_id}'
            r'(:?\.scope)?'
            r'/(?P<filename>{filenames})$'
            ).format(
                datasource_id=datasource_id,
                component_id=component_id,
                filenames="|".join(processor_files))

        path_matcher = re.compile(path_regex)

        data = collections.defaultdict(list)

        # Track the filename currently being parsed.
        filename = None

        for line in output.strip().splitlines():
            match = path_matcher.match(line)
            if match:
                # Start of a new file we care about.
                filename = match.group("filename")

            elif line.startswith("/sys/fs/cgroup/"):
                # Start of a new file we don't care about.
                filename = None

            elif filename:
                # A line within a file we care about.
                data[filename].append(line)

        return data
