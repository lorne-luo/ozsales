
var expresscarrierListPageVue = new CommonListPageVue({
        data: {
            list_api_tag:   'express:api-expresscarrier-list',
            delete_api_tag: 'express:api-expresscarrier-delete',
            detail_api_tag: 'express:api-expresscarrier-detail',

            create_url_tag: 'express:expresscarrier-add',
            list_url_tag:   'express:expresscarrier-list',
            detail_url_tag: 'express:expresscarrier-detail',
            update_url_tag: 'express:expresscarrier-update',
            list_url:       Urls['express:api-expresscarrier-list']()+ '?ordering=-is_default'
        }
    }
);
