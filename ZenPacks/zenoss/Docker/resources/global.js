(function(){

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
