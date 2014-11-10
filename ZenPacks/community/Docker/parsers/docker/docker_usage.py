"""
Performance parser for Docker Containers
Performance data located in:
    /sys/fs/cgroup/memory/docker/CONTAINER_ID/memory.usage_in_bytes
    /sys/fs/cgroup/cpuacct/docker/CONTAINER_ID/cpuacct.stat
"""

from Products.ZenRRD.CommandParser import CommandParser


class docker_usage(CommandParser):

    def processResults(self, cmd, result):

        lines = cmd.result.output.splitlines()
        if len(lines) > 1:
            cpu_user = 0
            cpu_system = 0

            for line in lines:
                if "user" in line:
                    cpu_user = int(line.replace("user", "").strip())
                if "system" in line:
                    cpu_system = int(line.replace("system", "").strip())

            for point in cmd.points:
                if point.id == 'cpu_user':
                    result.values.append((point, float(cpu_user)))
                if point.id == 'cpu_system':
                    result.values.append((point, float(cpu_system)))

        elif len(lines) == 1:
            try:
                mem_usage = int(cmd.result.output)
                for point in cmd.points:
                    if point.id == 'mem_usage':
                        result.values.append((point, float(mem_usage)))
            except:
                pass

        return result
