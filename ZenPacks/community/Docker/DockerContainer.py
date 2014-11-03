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

    container_state = ""

    _properties = DockerComponent._properties + (
        {'id': 'container_state', 'type': 'string'},
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

    container_state = schema.TextLine(title=_t(u'Container State'))


class DockerContainerInfo(ComponentInfo):
    ''' API Info adapter factory for DockerContainer '''

    implements(IDockerContainerInfo)
    adapts(DockerContainer)

    container_state = ProxyProperty('container_state')
