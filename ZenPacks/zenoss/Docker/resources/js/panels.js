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
                {name: 'size_used'},
                {name: 'size_free'},
                {name: 'size_used_percents'},
                {name: 'created'},
                {name: 'command'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},
                {name: 'status'},
                {name: 'old_docker'},
                {name: 'usesMonitorAttribute'}
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
                id: 'ports',
                dataIndex: 'ports',
                header: _t('Ports'),
                sortable: true,
                width: 100
            },{
                id: 'created',
                dataIndex: 'created',
                header: _t('Created'),
                sortable: true,
                width: 90
            },{
                id: 'size',
                dataIndex: 'size',
                header: _t('Root FS Size'),
                sortable: true,
                width: 70
            },{
                id: 'size_used',
                dataIndex: 'size_used',
                header: _t('Used'),
                sortable: true,
                width: 50
            },{
                id: 'size_free',
                dataIndex: 'size_free',
                header: _t('Available'),
                sortable: true,
                width: 50
            },{
                id: 'size_used_percents',
                dataIndex: 'size_used_percents',
                header: _t('Use %'),
                sortable: true,
                width: 50
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                renderer: Zenoss.render.pingStatus,
                width: 60
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
        this.store.on('guaranteedrange', function(){
            if (this.loaded) return;
            var items = Ext.getCmp('component_card').componentgrid.getView().store.data.items;

            if (items) {
                if (items[0].data.old_docker) {
                    Ext.ComponentQuery.query("gridcolumn[text=Root FS Size]")[0].hide();
                    Ext.ComponentQuery.query("gridcolumn[text=Used]")[0].hide();
                    Ext.ComponentQuery.query("gridcolumn[text=Available]")[0].hide();
                    Ext.ComponentQuery.query("gridcolumn[text=Use %]")[0].hide();
                }
            }

            this.loaded = true;
        }, this);
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