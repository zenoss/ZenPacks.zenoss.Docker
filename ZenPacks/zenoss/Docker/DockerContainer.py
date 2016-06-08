##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from zope.component import adapts
from zope.interface import implements

from Products.ZenRelations.RelSchema import ToOne, ToManyCont

from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

from .DockerComponent import DockerComponent


class DockerContainer(DockerComponent):
    meta_type = portal_type = 'DockerContainer'

    image = ""
    command = ""
    created = ""
    ports = ""

    _properties = DockerComponent._properties + (
        {'id': 'image', 'label': 'Image', 'type': 'string'},
        {'id': 'command', 'label': 'Command', 'type': 'string'},
        {'id': 'created', 'label': 'Created', 'type': 'string'},
        {'id': 'ports', 'label': 'Ports', 'type': 'string'},
    )

    _relations = DockerComponent._relations + (
        ('docker_host', ToOne(
            ToManyCont, 'Products.ZenModel.Device.Device',
            'docker_containers')
        ),
    )

    def device(self):
        return self.docker_host()


class IDockerContainerInfo(IComponentInfo):
    '''
    API Info interface for DockerContainer.
    '''

    image = schema.TextLine(title=_t(u'Image'))
    command = schema.TextLine(title=_t(u'Command'))
    created = schema.TextLine(title=_t(u'Created'))
    ports = schema.TextLine(title=_t(u'Ports'))


class DockerContainerInfo(ComponentInfo):
    ''' API Info adapter factory for DockerContainer '''

    implements(IDockerContainerInfo)
    adapts(DockerContainer)

    image = ProxyProperty('image')
    command = ProxyProperty('command')
    created = ProxyProperty('created')
    ports = ProxyProperty('ports')
