(function(){

var ZC = Ext.ns('Zenoss.component');

ZC.registerName(
    'DockerContainer',
    _t('Docker Container'),
    _t('Docker Containers'));

ZC.DockerContainerPanel = Ext.extend(ZC.ComponentGridPanel, {

    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'DockerContainer',
            fields: [
                {name: 'meta_type'},
                {name: 'uid'},
                {name: 'title'},
                {name: 'severity'},
                {name: 'name'},
                {name: 'image'},
                {name: 'ports'},
                {name: 'size'},
                {name: 'created'},
                {name: 'command'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},
                {name: 'status'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                width: 100
            },{
                id: 'image',
                dataIndex: 'image',
                header: _t('Image')
            },{
                id: 'command',
                dataIndex: 'command',
                header: _t('Command'),
                sortable: true,
                width: 120
            },{
                id: 'ports',
                dataIndex: 'ports',
                header: _t('Ports'),
                sortable: true,
                width: 100
            },{
                id: 'size',
                dataIndex: 'size',
                header: _t('Size'),
                sortable: true,
                width: 60
            },{
                id: 'created',
                dataIndex: 'created',
                header: _t('Created'),
                sortable: true,
                width: 100
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                renderer: Zenoss.render.pingStatus,
                width: 70
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                sortable: true,
                renderer: Zenoss.render.checkbox,
                width: 65
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });
        ZC.DockerContainerPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('DockerContainerPanel', ZC.DockerContainerPanel);

/* Overview Panel Override */
Ext.onReady(function(){
    var DEVICE_DESCRIPTION_PANEL = 'deviceoverviewpanel_descriptionsummary';

    /* Description Panel Override */
    Ext.ComponentMgr.onAvailable(DEVICE_DESCRIPTION_PANEL, function(){
        var descriptionpanel = Ext.getCmp(DEVICE_DESCRIPTION_PANEL);

        descriptionpanel.addField({
            id: 'docker_version-view',
            xtype: 'displayfield',
            name: 'docker_version',
            fieldLabel: _t('Docker Version'),
            permission: 'Manage Device'
        });

    });
});

})();