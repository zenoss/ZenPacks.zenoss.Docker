from zope.component import adapts
from zope.interface import implements

from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont

from Products.Zuul.catalog.paths import DefaultPathReporter, relPath
from Products.Zuul.decorators import info
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

from . import CLASS_NAME, MODULE_NAME
from .DockerComponent import DockerComponent


class DockerContainer(DockerComponent):
    meta_type = portal_type = 'DockerContainer'

    image = ""
    command = ""
    created = ""
    container_state = ""
    ports = ""
    size = ""

    _properties = DockerComponent._properties + (
        {'id': 'image', 'label': 'Image', 'type': 'string'},
        {'id': 'command', 'label': 'Command', 'type': 'string'},
        {'id': 'created', 'label': 'Created', 'type': 'string'},
        {'id': 'container_state', 'label': 'Container State', 'type': 'string'},
        {'id': 'ports', 'label': 'Ports', 'type': 'string'},
        {'id': 'size', 'label': 'Size', 'type': 'string'},
    )

    _relations = DockerComponent._relations + (
        ('docker_host', ToOne(
            ToManyCont, 'Products.ZenModel.Device.Device', 'docker_containers')
        ),
    )

    def device(self):
        return self.docker_host()

    def getStatus(self):
        return not ("up" in self.container_state.lower())


class IDockerContainerInfo(IComponentInfo):
    '''
    API Info interface for DockerContainer.
    '''

    image = schema.TextLine(title=_t(u'Image'))
    command = schema.TextLine(title=_t(u'Command'))
    created = schema.TextLine(title=_t(u'Created'))
    container_state = schema.TextLine(title=_t(u'Container State'))
    ports = schema.TextLine(title=_t(u'Ports'))
    # size = schema.TextLine(title=_t(u'Size'))


class DockerContainerInfo(ComponentInfo):
    ''' API Info adapter factory for DockerContainer '''

    implements(IDockerContainerInfo)
    adapts(DockerContainer)

    image = ProxyProperty('image')
    command = ProxyProperty('command')
    created = ProxyProperty('created')
    container_state = ProxyProperty('container_state')
    ports = ProxyProperty('ports')
    # size = ProxyProperty('size')
