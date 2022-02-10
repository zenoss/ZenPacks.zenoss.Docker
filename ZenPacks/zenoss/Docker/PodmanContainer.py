##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

# ZenPack Imports
from . import schema


class PodmanContainer(schema.PodmanContainer):
    """Model class for PodmanContainer.

    Extends the definition of PodmanContainer in zenpack.yaml.

    """

    def getRRDTemplates(self):
        """Return RRDTemplate list to bind to this component."""
        monitor_status = self.zPodmanMonitorContainerStatus
        monitor_stats = self.zPodmanMonitorContainerStats
        monitor_size = self.zPodmanMonitorContainerSize

        templates = []
        for template in super(PodmanContainer, self).getRRDTemplates():
            # Prefix matching is done to support the -replacement and
            # -addition custom templates that may come from super.
            if template.id.endswith("-Status") and not monitor_status:
                continue
            elif template.id.endswith("-Stats") and not monitor_stats:
                continue
            elif template.id.endswith("-Size") and not monitor_size:
                continue

            # Any templates that made it this far get used.
            templates.append(template)

        return templates
