ZenPacks.community.Docker
=========================

Docker monitoring zenpack for Zenoss. Adds "Docker Containers" component to devices.

<img src="https://raw.githubusercontent.com/vsergeyev/ZenPacks.community.Docker/master/screenshot1.png" width=500 alt="Docker Containers modeled in Zenoss device" />

Background: uses `docker ps` to retrieve data about configured/running containers.


Monitoring
==========

For every Docker Container monitored:

 - CPU usage (user, system)
 - Memory usage


Compatibility
=============

Have tested and works on:

- Zenoss Core 4.2.x
- Zenoss Resource Manager 4.2.x
