
var orderListPageVue = new OrderListPageVue({
        data: {
            // API
            list_api_tag:   'order:api-order-list',
            detail_api_tag: 'order:api-order-detail',
            delete_api_tag: 'order:api-order-delete',
            // page
            create_url_tag: 'order:order-add',
            list_url_tag:   'order:order-list-short',
            update_url_tag: 'order:order-update',
            detail_url_tag: 'order:order-detail-short',
            list_url:       Urls['order:api-order-list'](),

            finished_items: [],
            ongoing_items: [],
            finished_currentPage: 1,
            finished_totalPage: 1,
            finished_perPage: 10,
            finished_count: 0,
            ongoing_currentPage: 1,
            ongoing_totalPage: 1,
            ongoing_perPage: 10,
            ongoing_count: 0
        }
    }
);
