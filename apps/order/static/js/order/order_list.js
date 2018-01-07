
var orderListPageVue = new OrderListPageVue({
        data: {
            // API
            list_api_tag:   'api:order-list',
            detail_api_tag: 'api:order-detail',
            product_detail_api_tag: 'api:orderproduct-detail',
            delete_api_tag: 'api:order-delete',
            // page
            create_url_tag: 'order:order-add',
            list_url_tag:   'order:order-list-short',
            update_url_tag: 'order:order-update',
            detail_url_tag: 'order-detail-short',
            list_url:       Urls['api:order-list'](),

            finished_items: [],
            ongoing_items: [],
            created_items: [],
            finished_currentPage: 1,
            finished_totalPage: 1,
            finished_perPage: 15,
            finished_count: 0,
            ongoing_currentPage: 1,
            ongoing_totalPage: 1,
            ongoing_perPage: 15,
            ongoing_count: 0,
            created_currentPage: 1,
            created_totalPage: 1,
            created_perPage: 20,
            created_count: 0,
            ordering: '-id'
        }
    }
);
