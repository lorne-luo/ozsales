
var dealtaskListPageVue = new CommonListPageVue({
        data: {
            // API
            list_api_tag:   'schedule:api-dealtask-list',
            detail_api_tag: 'schedule:api-dealtask-detail',
            delete_api_tag: 'schedule:api-dealtask-delete',
            // page
            create_url_tag: 'schedule:dealtask-add',
            list_url_tag:   'schedule:dealtask-list',
            update_url_tag: 'schedule:dealtask-update',
            detail_url_tag: 'schedule:dealtask-detail',
            list_url:       Urls['schedule:api-dealtask-list']() + '?'
        }
    }
);
