var MonthlyReportListPageVue = CommonListPageVue.extend({
    methods: {
        ready: function (event) {
            this.loadData(this.get_param(), true);
        },
        loadData: function (data, isInit) {
            var isInit = isInit === true ? isInit : false;
            var self = this;
            var url;
            if (self.list_url)
                url = self.list_url;
            else if (self.list_api_tag)
                url = Urls[self.list_api_tag]();
            else
                url = $.AdminLTE.getApiUrl(self.appName, self.modelName);

            $.AdminLTE.apiGet(
                url,
                data,
                function (resp) {
                    self.items = resp.results;
                    self.count = resp.count;
                    self.perPage = resp.per_page;
                    self.totalPage = resp.total_page;
                    self.currentPage = resp.current_page;

                    if (isInit) {
                        var tableData = [];
                        for (var i = 0; i < resp.results.length; i++) {
                            tableData.push({
                                month: resp.results[i].month,
                                sell_price_rmb: resp.results[i].sell_price_rmb,
                                profit_rmb: resp.results[i].profit_rmb,
                                shipping_fee: resp.results[i].shipping_fee,
                                order_count: resp.results[i].order_count,
                                parcel_count: resp.results[i].parcel_count
                            });
                        }

                        Morris.Line({
                            element: 'sale-chart',
                            data: tableData,
                            xkey: 'month',
                            ykeys: ['sell_price_rmb', 'profit_rmb', 'shipping_fee'],
                            labels: ['sell_price_rmb', 'profit_rmb', 'shipping_fee'],
                            hideHover: true
                        });

                        Morris.Line({
                            element: 'order-chart',
                            data: tableData,
                            xkey: 'month',
                            ykeys: ['parcel_count', 'order_count'],
                            labels: ['parcel_count', 'order_count'],
                            hideHover: true
                        });
                    }
                }
            );
        }
    }
});

var monthlyreportListPageVue = new MonthlyReportListPageVue({
        data: {
            // API
            list_api_tag: 'api:report-list',
            detail_api_tag: 'api:report-detail',
            delete_api_tag: 'api:report-delete',
            // page
            // create_url_tag: 'report:monthlyreport-add',
            list_url_tag: 'report:monthlyreport-list',
            update_url_tag: 'report:monthlyreport-update',
            detail_url_tag: 'report:monthlyreport-detail',
            list_url: Urls['api:report-list']() + '?ordering=-month'
        }
    }
);
