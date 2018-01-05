var productListPageVue = new CommonListPageVue({
        data: {
            // API
            list_api_tag:   'api:product-list',
            detail_api_tag: 'api:product-detail',
            delete_api_tag: 'api:product-delete',
            // page
            create_url_tag: 'product:product-add',
            list_url_tag:   'product:product-list',
            update_url_tag: 'product:product-update',
            detail_url_tag: 'product:product-detail',
            list_url:       Urls['api:product-list']()
        }
    }
);
