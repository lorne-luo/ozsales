
var orderListPageVue = new OrderListPageVue({
        data: {
            list_api_tag:   'order:api-order-list',
            delete_api_tag: 'order:api-order-delete',
            detail_api_tag: 'order:api-order-detail',
            
            create_url_tag: 'order:order-add',
            list_url_tag:   'order:order-list-short',
            detail_url_tag: 'order:order-detail-short',
            update_url_tag: 'order:order-update',
            list_url:       Urls['order:order-list'](),

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
