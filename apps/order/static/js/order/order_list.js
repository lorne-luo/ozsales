
var orderListPageVue = new CommonListPageVue({
        data: {
            add_api_tag: 'order:api-order-list',
            list_api_tag: 'order:api-order-list',
            delete_api_tag: 'order:api-order-delete',
            retrieve_api_tag: 'order:api-order-detail',
            update_api_tag: 'order:api-order-detail',
            destroy_api_tag: 'order:api-order-detail',

            create_url_tag: 'order:order-add',
            detail_url_tag: 'order:order-detail',
            update_url_tag: 'order:order-update'
        }
    }
);
