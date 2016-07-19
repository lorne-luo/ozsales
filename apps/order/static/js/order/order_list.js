
var orderListPageVue = new OrderListPageVue({
        data: {
            add_api_tag: 'order:api-order-list',
            list_api_tag: 'order:api-order-list',
            delete_api_tag: 'order:api-order-delete',
            retrieve_api_tag: 'order:api-order-detail',
            update_api_tag: 'order:api-order-detail',
            create_url_tag: 'order:order-add',
            detail_url_tag: 'order:order-detail-short',
            update_url_tag: 'order:order-update',
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
