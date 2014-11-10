"""
Performance parser for Docker Containers
Performance data located in:
    /sys/fs/cgroup/memory/docker/CONTAINER_ID/memory.usage_in_bytes
    /sys/fs/cgroup/cpuacct/docker/CONTAINER_ID/cpuacct.stat
"""

from Products.ZenRRD.CommandParser import CommandParser


class docker_usage(CommandParser):

    def processResults(self, cmd, result):
        print "DOCKER USAGE MEMORY:"
        print cmd.result.output
        # for point in cmd.points:
        #     if point.id == 'pset_min':
        #         result.values.append((point, to_units(data[2])))
        #     if point.id == 'pset_max':
        #         result.values.append((point, to_units(data[3][:-1])))
        #     if point.id == 'pset_size':
        #         result.values.append((point, to_units(data[4])))
        #     if point.id == 'pset_used':
        #         result.values.append((point, to_units(data[5])))
        #     if point.id == 'pset_load':
        #         result.values.append((point, to_units(data[6])))
        return result
