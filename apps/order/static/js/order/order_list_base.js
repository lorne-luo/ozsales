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
                var api_url = url + '?status=FINISHED';

                $.AdminLTE.apiGet(
                    api_url,
                    data,
                    function (resp) {
                        self.finished_items = resp.results;
                        self.finished_count = resp.count;
                        self.finished_perPage = resp.per_page;
                        self.finished_totalPage = resp.total_page;
                        self.finished_currentPage = resp.current_page;
                    }
                );
            }
            if ($('.tab-content #pane-CREATED').hasClass('active') && !_init) {
                var api_url = url + 'new/';

                $.AdminLTE.apiGet(
                    api_url,
                    data,
                    function (resp) {
                        self.created_items = resp.results;
                        self.created_count = resp.count;
                        self.created_perPage = resp.per_page;
                        self.created_totalPage = resp.total_page;
                        self.created_currentPage = resp.current_page;
                    }
                );
            }
            if ($('.tab-content #pane-ONGOING').hasClass('active') || _init) {
                var api_url = url + 'shipping/';

                $.AdminLTE.apiGet(
                    api_url,
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
            } else if ($('.tab-content #pane-CREATED').hasClass('active')) {
                page = this.created_currentPage;
            } else if ($('.tab-content #pane-ONGOING').hasClass('active')) {
                page = this.ongoing_currentPage;
            }
            this.currentPage = page;
            this.loadData(this.get_param());
        },
        makr_as_purchased: function (event) {
            var productID = $(event.target).val();
            var value = $(event.target).prop("checked")
            var url = Urls[this.product_detail_api_tag](productID);
            $.AdminLTE.apiPost(
                url,
                $.param({'is_purchased': value}),
                function (resp) {
                }
            );
        },
        page_ongoing: function (event) {
            var num = $(event.target).attr('page');
            this.ongoing_currentPage = num;
            this.currentPage = num;
            this.loadData(this.get_param());
        },
        page_created: function (event) {
            var num = $(event.target).attr('page');
            this.created_currentPage = num;
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
            if (event.target.tagName.toUpperCase() == 'TD' || $(event.target).hasClass('show_detail')) {
                var table = $(event.target).closest('table');
                var tr = $(event.target).closest('tr');
                var icon = $('i.show_detail', tr);
                if ($('#detail_' + pk, table).toggleClass('hide').hasClass('hide')) {
                    icon.removeClass("fa-minus-square");
                    icon.addClass("fa-plus-square");
                } else {
                    icon.addClass("fa-minus-square");
                    icon.removeClass("fa-plus-square");
                }
            }
        },
        show_all_detail: function (event) {
            var table = $(event.target).closest('table');
            var icon_all = $('i.show_all_detail', table);
            if (icon_all.toggleClass('extend').hasClass('extend')) {
                icon_all.addClass("fa-minus-square");
                icon_all.removeClass("fa-plus-square");
            }
            else {
                icon_all.removeClass("fa-minus-square");
                icon_all.addClass("fa-plus-square");
            }

            var icons = $('i.show_detail', table);
            icons.each(function (index) {
                var pk = $(this).attr('data-pk');
                if (icon_all.hasClass('extend')) {
                    $('#detail_' + pk).removeClass('hide');
                    $(this).addClass("fa-minus-square");
                    $(this).removeClass("fa-plus-square");
                } else {
                    $('#detail_' + pk).addClass('hide');
                    $(this).removeClass("fa-minus-square");
                    $(this).addClass("fa-plus-square");
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
