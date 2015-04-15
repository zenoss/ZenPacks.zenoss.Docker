##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

{
    "DockerCollector": [{
        'c5bd2f24206f09583561c6143416a0593cd2c5f67101bbf6113a45280ca3dff1': {
            'id': 'c5bd2f24206f09583561c6143416a0593cd2c5f67101bbf6113a45280ca3dff1',
            'title': 'cranky_ardinghelli',
            'command': '"/bin/bash"',
            'container_state': 'Exited (0) 2 days ago',
            'created': '2 weeks ago',
            'image': 'ubuntu:14.04',
            'modname': 'ZenPacks.zenoss.Docker.DockerContainer',
            'ports': '',
            'size': '',
            'size_free': '',
            'size_used': ''
        },
        '475e044c660890cba691dd5ec573e8bf97c99af0398177139127adb4a882e524': {
            'id': '475e044c660890cba691dd5ec573e8bf97c99af0398177139127adb4a882e524',
            'title': 'berserk_babbage',
            'command': '"bash"',
            'container_state': 'Up 4 days',
            'created': '5 weeks ago',
            'image': 'ubuntu:latest',
            'modname': 'ZenPacks.zenoss.Docker.DockerContainer',
            'ports': '0.0.0.0:80->80/tcp',
            'size': '',
            'size_free': '',
            'size_used': ''
        }
    }]
}