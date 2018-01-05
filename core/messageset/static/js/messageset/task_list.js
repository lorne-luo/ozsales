
var taskListPageVue = new CommonListPageVue({
        data: {
            list_api_tag: 'api:task-list',
            delete_api_tag: 'api:task-delete',
            detail_api_tag: 'api:task-detail',

            create_url_tag: 'messageset:task-add',
            list_url_tag:   'messageset:task-list',
            detail_url_tag: 'messageset:task-detail',
            update_url_tag: 'messageset:task-update'
        }
    }
);
