
var monthlyreportListPageVue = new CommonListPageVue({
        data: {
            // API
            list_api_tag:   'report:api-monthlyreport-list',
            detail_api_tag: 'report:api-monthlyreport-detail',
            delete_api_tag: 'report:api-monthlyreport-delete',
            // page
            create_url_tag: 'report:monthlyreport-add',
            list_url_tag:   'report:monthlyreport-list',
            update_url_tag: 'report:monthlyreport-update',
            detail_url_tag: 'report:monthlyreport-detail',
            list_url:       Urls['report:api-monthlyreport-list']() + '?ordering=-month'
        }
    }
);
