
var expresscarrierListPageVue = new CommonListPageVue({
        data: {
            list_api_tag:   'api:expresscarrier-list',
            delete_api_tag: 'api:expresscarrier-delete',
            detail_api_tag: 'api:expresscarrier-detail',

            create_url_tag: 'express:expresscarrier-add',
            list_url_tag:   'express:expresscarrier-list',
            detail_url_tag: 'express:expresscarrier-detail',
            update_url_tag: 'express:expresscarrier-update',
            list_url:       Urls['api:expresscarrier-list']()
        }
    }
);
