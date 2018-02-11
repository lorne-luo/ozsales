var sitemailreceiveListPageVue = new CommonListPageVue({
    data: {
        list_api_tag: 'api:sitemailreceive-list',
        delete_api_tag: 'api:sitemailreceive-delete',
        detail_api_tag: 'api:sitemailreceive-detail',

        create_url_tag: 'messageset:sitemailreceive-add',
        list_url_tag: 'messageset:sitemailreceive-list',
        detail_url_tag: 'messageset:sitemailreceive-detail',
        update_url_tag: 'messageset:sitemailreceive-update',
        ordering: 'status,-send_time'
    }
});
