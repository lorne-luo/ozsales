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
        showShipping: function (pk, event) {
            if (event.target.tagName.toUpperCase() == 'TD' || $(event.target).closest('td').hasClass('show_shipping')) {
                var tr=$(event.target).closest('tr');
                var td =$('td.show_shipping',tr);

                if ($('#shipping_' + pk).hasClass('hide')) {
                    $('#shipping_' + pk).removeClass('hide');
                    td.html('<i class="fa fa-minus-square text-info" aria-hidden="true"></i>');
                } else {
                    $('#shipping_' + pk).addClass('hide');
                    td.html('<i class="fa fa-plus-square text-info" aria-hidden="true"></i>');
                }
            }
        },
        next_ship_status: function (url, next, event) {
            swal({
              title: "确认物流变更",
              text: "确认将物流状态变更为\""+next+"\"?",
              type: "warning",
              showCancelButton: true,
              confirmButtonColor: "#DD6B55",
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              closeOnConfirm: true,
              showLoaderOnConfirm: false,
              animation: false
            }, function () {
              window.location.href = url;
            });
        },
        pay: function (url, event) {
            swal({
              title: "确认支付",
              text: "确认变更为\"已支付\"?",
              type: "warning",
              showCancelButton: true,
              confirmButtonColor: "#DD6B55",
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              closeOnConfirm: true,
              showLoaderOnConfirm: false,
              animation: false
            }, function () {
              window.location.href = url;
            });
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
