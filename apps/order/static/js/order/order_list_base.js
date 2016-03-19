var OrderListPageVue = CommonListPageVue.extend({
    ready: function () {
        if (this.appName && this.modelName) {
            this.loadData({}, true);
        }
    },
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
                url = url + '?status_in=CREATED,SHIPPING,DELIVERED&ordering=-id';

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

        },
        page_ongoing: function (event) {
            var num = $(event.target).attr('page');
            this.loadData({'page': num});
        },
        page_finished: function (event) {
            var num = $(event.target).attr('page');
            this.loadData({'page': num});
        },
        detail: function (event) {
            var pk, customer;
            if ($(event.target).data('pk'))
                pk = $(event.target).data('pk');
            else if ($(event.target.parentNode).data('pk'))
                pk = $(event.target.parentNode).data('pk');
            else {
                swal('错误', '无法获取pk', 'error');
                return;
            }
            if ($(event.target).data('customer'))
                customer = $(event.target).data('customer');
            else if ($(event.target.parentNode).data('customer'))
                customer = $(event.target.parentNode).data('customer');
            else {
                swal('错误', '无法获取customer', 'error');
                return;
            }

            var url;
            if (this.detail_url_tag) {
                url = Urls[this.detail_url_tag](customer, pk);
            } else {
                url = Urls['adminlte:common_detail_page'](
                    this.appName,
                    this.modelName,
                    pk
                );
            }
            window.location.href = url;
        }
    }
});
