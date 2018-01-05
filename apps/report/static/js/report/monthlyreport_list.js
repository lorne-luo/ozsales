
var monthlyreportListPageVue = new CommonListPageVue({
        data: {
            // API
            list_api_tag:   'api:report-list',
            detail_api_tag: 'api:report-detail',
            delete_api_tag: 'api:report-delete',
            // page
            // create_url_tag: 'report:monthlyreport-add',
            list_url_tag:   'report:monthlyreport-list',
            update_url_tag: 'report:monthlyreport-update',
            detail_url_tag: 'report:monthlyreport-detail',
            list_url:       Urls['api:report-list']() + '?ordering=-month'
        }
    }
);
