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
    size_used = ""
    size_free = ""
    size_used_percents = ""

    _properties = DockerComponent._properties + (
        {'id': 'image', 'label': 'Image', 'type': 'string'},
        {'id': 'command', 'label': 'Command', 'type': 'string'},
        {'id': 'created', 'label': 'Created', 'type': 'string'},
        {'id': 'container_state', 'label': 'Container State',
            'type': 'string'},
        {'id': 'ports', 'label': 'Ports', 'type': 'string'},
        {'id': 'size', 'label': 'Root FS Size', 'type': 'string'},
        {'id': 'size_used', 'label': 'Root FS Used', 'type': 'string'},
        {'id': 'size_free', 'label': 'Root FS Available', 'type': 'string'},
        {'id': 'size_used_percents', 'label': 'Root FS Used %',
            'type': 'string'},
    )

    _relations = DockerComponent._relations + (
        ('docker_host', ToOne(
            ToManyCont, 'Products.ZenModel.Device.Device',
            'docker_containers')
        ),
    )

    def device(self):
        return self.docker_host()

    def getStatus(self):
        return not ("up" in self.container_state.lower())

    def _old_docker(self):
        return ("version 1.2" in self.device().docker_version)

    def getRRDTemplates(self):
        if self._old_docker():
            return [self.getRRDTemplateByName('DockerContainer')]
        return [self.getRRDTemplateByName('DockerContainer'),
            self.getRRDTemplateByName('DockerContainerSize')]


class IDockerContainerInfo(IComponentInfo):
    '''
    API Info interface for DockerContainer.
    '''

    image = schema.TextLine(title=_t(u'Image'))
    command = schema.TextLine(title=_t(u'Command'))
    created = schema.TextLine(title=_t(u'Created'))
    container_state = schema.TextLine(title=_t(u'Container State'))
    ports = schema.TextLine(title=_t(u'Ports'))
    size = schema.TextLine(title=_t(u'Root FS Size'))
    size_used = schema.TextLine(title=_t(u'Root FS Used'))
    size_free = schema.TextLine(title=_t(u'Root FS Available'))
    size_used_percents = schema.TextLine(title=_t(u'Root FS Used %'))


class DockerContainerInfo(ComponentInfo):
    ''' API Info adapter factory for DockerContainer '''

    implements(IDockerContainerInfo)
    adapts(DockerContainer)

    image = ProxyProperty('image')
    command = ProxyProperty('command')
    created = ProxyProperty('created')
    container_state = ProxyProperty('container_state')
    ports = ProxyProperty('ports')
    size = ProxyProperty('size')
    size_used = ProxyProperty('size_used')
    size_free = ProxyProperty('size_free')
    size_used_percents = ProxyProperty('size_used_percents')

    @property
    @info
    def old_docker(self):
        return self._object._old_docker()
