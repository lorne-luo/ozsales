var OrderListPageVue = CommonListPageVue.extend({
    ready: function () {
        this.loadData(this.get_param(), true);
    },
    methods: {
        loadData: function (data, init) {
            var _init = typeof init !== 'undefined' ? init : false;
            var self = this;
            var url;
            if (self.list_url)
                url = self.list_url;
            else if (self.list_api_tag)
                url = Urls[self.list_api_tag]();
            else
                url = $.AdminLTE.getApiUrl(self.appName, self.modelName);

            if ($('.tab-content #pane-FINISHED').hasClass('active') || _init) {
                url = url + '?status=FINISHED';

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
                url = url + '?status__in=CREATED,SHIPPING,DELIVERED';

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
        reload: function (event) {
            var page;
            if ($('.tab-content #pane-FINISHED').hasClass('active')) {
                page = this.finished_currentPage;
            } else if ($('.tab-content #pane-ONGOING').hasClass('active')) {
                page = this.ongoing_currentPage;
            }
            this.currentPage = page;
            this.loadData(this.get_param());
        },
        page_ongoing: function (event) {
            var num = $(event.target).attr('page');
            this.ongoing_currentPage = num;
            this.currentPage = num;
            this.loadData(this.get_param());
        },
        page_finished: function (event) {
            var num = $(event.target).attr('page');
            this.finished_currentPage = num;
            this.currentPage = num;
            this.loadData(this.get_param());
        },
        show_detail: function (pk, event) {
            if (event.target.tagName.toUpperCase() == 'TD' || $(event.target).closest('td').hasClass('show_detail')) {
                var tr = $(event.target).closest('tr');
                var td = $('td.show_detail', tr);
                if ($('#detail_' + pk).toggleClass('hide').hasClass('hide')) {
                    td.html('<i class="fa fa-plus-square text-primary" aria-hidden="true"></i>');
                } else {
                    td.html('<i class="fa fa-minus-square text-primary" aria-hidden="true"></i>');
                }
            }
        },
        show_all_detail: function (event) {
            var th = $('th#show_all_detail');
            if (th.toggleClass('extend').hasClass('extend'))
                th.html('<i class="fa fa-minus-square text-muted" aria-hidden="true"></i>');
            else
                th.html('<i class="fa fa-plus-square text-muted" aria-hidden="true"></i>');

            var tds = $('td.show_detail');
            tds.each(function (index) {
                var pk = $(this).attr('data-pk');
                if (th.hasClass('extend')) {
                    $('#detail_' + pk).removeClass('hide');
                    $(this).html('<i class="fa fa-minus-square text-primary" aria-hidden="true"></i>');
                } else {
                    $('#detail_' + pk).addClass('hide');
                    $(this).html('<i class="fa fa-plus-square text-primary" aria-hidden="true"></i>');
                }
            });
        },
        next_ship_status: function (pk, next_status, next, event) {
            var self = this;
            var url = Urls[self.detail_api_tag](pk);
            swal({
                title: "确认物流变更",
                text: "确认将物流状态变更为\"" + next + "\"?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                closeOnConfirm: true,
                showLoaderOnConfirm: false,
                animation: false
            }, function () {
                $.AdminLTE.apiPost(
                    url,
                    $.param({'status': next_status}),
                    function (resp) {
                        var status = resp['status'];
                        var td = $(event.target).closest('td');
                        self.update_status_button(td, resp);
                    }
                );
            });
        },
        update_status_button: function (td, resp) {
            var self = this;
            var current_status_name = self.get_status_name(resp['status']);
            var next_status_name = self.get_status_name(resp['next_status']);
            var label_class = '';
            if (resp['status'] == 'SHIPPING')
                label_class = 'success';
            else if (resp['status'] == 'DELIVERED')
                label_class = 'warning';
            else if (resp['status'] == 'FINISHED')
                label_class = 'danger';

            if (resp['status'] == 'FINISHED') {
                var html = '<a class="label label-' + label_class + '" v-on:click="next_ship_status(' + resp['id'] + ',\'DELIVERED\',\'寄达\', $event)">完成</a>';
            } else {
                var html = '<a class="label label-' + label_class + '" v-on:click="next_ship_status(' + resp['id'] + ',\'' + resp['next_status'] + '\',\'' + next_status_name + '\', $event)">' + current_status_name + '</a>';
            }
            td.html(html);
            self.$compile(td.get(0));
        },
        pay: function (pk, event) {
            var self = this;
            var url = Urls[self.detail_api_tag](pk);
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
                $.AdminLTE.apiPost(
                    url,
                    $.param({'is_paid': true}),
                    function (resp) {
                        var is_paid = resp['is_paid'];
                        if (is_paid) {
                            $(event.target).closest('a.pay').remove();
                        }
                    }
                );
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
        },
        get_status_name: function (status) {
            if (status == 'CREATED')
                return '新建';
            else if (status == 'SHIPPING')
                return '在途';
            else if (status == 'DELIVERED')
                return '寄达';
            else if (status == 'FINISHED')
                return '完成';
            else
                return '';
        }
    }
});
