
var orderproductListPageVue = new CommonListPageVue({
        data: {
            // API
            list_api_tag:   'api:orderproduct-list',
            detail_api_tag: 'api:orderproduct-detail',
            delete_api_tag: 'api:orderproduct-delete',
            // page
            // create_url_tag: 'order:orderproduct-add',
            list_url_tag:   'order:orderproduct-list',
            // update_url_tag: 'order:orderproduct-update',
            detail_url_tag: 'order:orderproduct-detail',
            list_url:       Urls['api:orderproduct-list']() + '?',
            ordering: '-create_time'
        }
    }
);
