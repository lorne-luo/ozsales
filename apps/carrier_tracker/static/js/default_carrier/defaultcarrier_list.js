
var expresscarrierListPageVue = new CommonListPageVue({
        data: {
            list_api_tag:   'api:carriertracker-list',
            delete_api_tag: 'api:carriertracker-delete',
            detail_api_tag: 'api:carriertracker-detail',

            create_url_tag: 'carriertracker:carriertracker-add',
            list_url_tag:   'carriertracker:carriertracker-list',
            detail_url_tag: 'carriertracker:carriertracker-detail',
            update_url_tag: 'carriertracker:carriertracker-update',
            list_url:       Urls['api:carriertracker-list']()+ '?ordering=-is_default'
        }
    }
);
