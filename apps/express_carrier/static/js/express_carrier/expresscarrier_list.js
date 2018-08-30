
var expresscarrierListPageVue = new CommonListPageVue({
        data: {
            list_api_tag:   'api:expresscarrier-list',
            delete_api_tag: 'api:expresscarrier-delete',
            detail_api_tag: 'api:expresscarrier-detail',

            create_url_tag: 'express_carrier:expresscarrier-add',
            list_url_tag:   'express_carrier:expresscarrier-list',
            detail_url_tag: 'express_carrier:expresscarrier-detail',
            update_url_tag: 'express_carrier:expresscarrier-update',
            list_url:       Urls['api:expresscarrier-list']()+ '?ordering=-is_default'
        }
    }
);
