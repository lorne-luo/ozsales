var OrderMemberListPageVue = OrderListPageVue.extend({
    methods: {
        loadData: function (data, init) {
            var _init = typeof init !== 'undefined' ? init : false;
            var self = this;
            var url;
            if (self.list_api_tag)
                url = Urls[self.list_api_tag]();
            else
                url = $.AdminLTE.getApiUrl(self.appName, self.modelName);

            if ($('.tab-content #pane-FINISHED').hasClass('active') || _init) {
                url = url + '?ordering=-id&status=FINISHED';
                $.AdminLTE.apiGet(
                    url,
                    data,
                    function (resp) {
                        self.finished_items = resp.results;
                        self.finished_count = resp.count;
                        self.finished_perPage = resp.per_page;
                        self.finished_totalPage = resp.total_page;
                        self.finished_currentPage = resp.current_page;
                    }
                );
            } else if ($('.tab-content #pane-ONGOING').hasClass('active') || _init) {
                url = url + '?status__in=CREATED,SHIPPING,DELIVERED&ordering=-id';
                $.AdminLTE.apiGet(
                    url,
                    data,
                    function (resp) {
                        self.ongoing_items = resp.results;
                        self.ongoing_count = resp.count;
                        self.ongoing_perPage = resp.per_page;
                        self.ongoing_totalPage = resp.total_page;
                        self.ongoing_currentPage = resp.current_page;
                    }
                );
            }
        }
    }
});

var orderListPageVue = new OrderMemberListPageVue({
        data: {
            add_api_tag: 'order:api-order-list',
            list_api_tag: 'order:api-order-list',
            delete_api_tag: 'order:api-order-delete',
            retrieve_api_tag: 'order:api-order-detail',
            update_api_tag: 'order:api-order-detail',
            create_url_tag: 'order:order-add',
            list_url_tag:   'order:order-list-short',
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
