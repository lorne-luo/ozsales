
var expresscarrierListPageVue = new CommonListPageVue({
        data: {
            list_api_tag:   'api:defaultcarrier-list',
            delete_api_tag: 'api:defaultcarrier-delete',
            detail_api_tag: 'api:defaultcarrier-detail',

            create_url_tag: 'default_carrier:defaultcarrier-add',
            list_url_tag:   'default_carrier:defaultcarrier-list',
            detail_url_tag: 'default_carrier:defaultcarrier-detail',
            update_url_tag: 'default_carrier:defaultcarrier-update',
            list_url:       Urls['api:defaultcarrier-list']()+ '?ordering=-is_default'
        }
    }
);
