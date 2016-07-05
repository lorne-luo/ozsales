
var customerListPageVue = new CommonListPageVue({
        data: {
            add_api_tag: 'customer:api-customer-list',
            list_api_tag: 'customer:api-customer-list',
            delete_api_tag: 'customer:api-customer-delete',
            retrieve_api_tag: 'customer:api-customer-detail',
            update_api_tag: 'customer:api-customer-detail',
            destroy_api_tag: 'customer:api-customer-detail',

            create_url_tag: 'customer:customer-add',
            detail_url_tag: 'customer:customer-detail',
            update_url_tag: 'customer:customer-update'
        }
    }
);
