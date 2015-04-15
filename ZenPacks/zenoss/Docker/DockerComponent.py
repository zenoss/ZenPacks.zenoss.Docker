from Products.ZenModel.Device import Device
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE


class DockerComponent(DeviceComponent, ManagedEntity):
    ''' Base class for all components in this ZenPack.  '''

    # Explicit inheritence.
    _properties = ManagedEntity._properties
    _relations = ManagedEntity._relations

    # Meta-data: Zope object views and actions
    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE,),
            },),
        },)

    def getIconPath(self):
        '''
        Return the path to an icon for this component.
        '''
        return '/++resource++docker/img/%s.png' \
               % self.meta_type
