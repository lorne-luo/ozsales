var OrderListPageVue = CommonListPageVue.extend({
    ready: function () {
        if(this.appName && this.modelName){
            this.loadOngoingData({});
            this.loadFinishedData({});
        }
    },
    methods: {
        loadOngoingData: function (data) {
            var self = this;
            var url;
            if (self.list_api_tag)
                url = Urls[self.list_api_tag]();
            else
                url = $.AdminLTE.getApiUrl(self.appName, self.modelName);

            var ongoing_url=url+'?status_in=CREATED,SHIPPING,DELIVERED';
            $.AdminLTE.apiGet(
                ongoing_url,
                data,
                function (resp) {
                    self.ongoing_items = resp.results;
                    self.ongoing_count = resp.count;
                    self.ongoing_perPage = resp.per_page;
                    self.ongoing_totalPage = resp.total_page;
                    self.ongoing_currentPage = resp.current_page;
                }
            );
        },
        loadFinishedData: function (data) {
            var self = this;
            var url;
            if (self.list_api_tag)
                url = Urls[self.list_api_tag]();
            else
                url = $.AdminLTE.getApiUrl(self.appName, self.modelName);

            var finished_url=url+'?ordering=-id&status=FINISHED';
            $.AdminLTE.apiGet(
                finished_url,
                data,
                function (resp) {
                    self.finished_items = resp.results;
                    self.finished_count = resp.count;
                    self.finished_perPage = resp.per_page;
                    self.finished_totalPage = resp.total_page;
                    self.finished_currentPage = resp.current_page;
                }
            );
        },
        page_ongoing: function () {
            var num = $(event.target).attr('page');
            this.loadOngoingData({'page': num});
        },
        page_finished: function () {
            var num = $(event.target).attr('page');
            this.loadFinishedData({'page': num});
        }
    }
});

var orderListPageVue = new OrderListPageVue({
        data: {
            add_api_tag: 'order:api-order-list',
            list_api_tag: 'order:api-order-list',
            delete_api_tag: 'order:api-order-delete',
            retrieve_api_tag: 'order:api-order-detail',
            update_api_tag: 'order:api-order-detail',
            destroy_api_tag: 'order:api-order-detail',

            create_url_tag: 'order:order-add',
            detail_url_tag: 'order:order-detail',
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
