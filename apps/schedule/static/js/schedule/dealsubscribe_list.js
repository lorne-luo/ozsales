
var dealsubscribeListPageVue = new CommonListPageVue({
        data: {
            // API
            list_api_tag:   'schedule:api-dealsubscribe-list',
            detail_api_tag: 'schedule:api-dealsubscribe-detail',
            delete_api_tag: 'schedule:api-dealsubscribe-delete',
            // page
            create_url_tag: 'schedule:dealsubscribe-add',
            list_url_tag:   'schedule:dealsubscribe-list',
            update_url_tag: 'schedule:dealsubscribe-update',
            detail_url_tag: 'schedule:dealsubscribe-detail',
            list_url:       Urls['schedule:api-dealsubscribe-list']() + '?'
        }
    }
);
