var CustomerListPageVue = CommonListPageVue.extend({
    methods: {
        show_address: function (pk, event) {
            if (event.target.tagName.toUpperCase() == 'TD' || $(event.target).closest('td').hasClass('show_address')) {
                var tr = $(event.target).closest('tr');
                var td = $('td.show_address', tr);
                var address_set = $('#address_set_' + pk);

                if (!address_set.size()) {
                    return;
                }
                else if (address_set.toggleClass('hide').hasClass('hide')) {
                    td.html('<i class="fa fa-plus-square text-primary" aria-hidden="true"></i>');
                } else {
                    td.html('<i class="fa fa-minus-square text-primary" aria-hidden="true"></i>');
                }
            }
        },
        show_all_address: function (event) {
            var th = $('th#show_all_address');
            if (th.toggleClass('extend').hasClass('extend'))
                th.html('<i class="fa fa-minus-square text-muted" aria-hidden="true"></i>');
            else
                th.html('<i class="fa fa-plus-square text-muted" aria-hidden="true"></i>');

            var tds = $('td.show_address');
            tds.each(function (index) {
                var pk = $(this).attr('data-pk');
                var address_set = $('#address_set_' + pk);
                if (!address_set.size()) {
                }
                else if (th.hasClass('extend')) {
                    address_set.removeClass('hide');
                    $(this).html('<i class="fa fa-minus-square text-primary" aria-hidden="true"></i>');
                } else {
                    address_set.addClass('hide');
                    $(this).html('<i class="fa fa-plus-square text-primary" aria-hidden="true"></i>');
                }
            });
        }
    }
});

var customerListPageVue = new CustomerListPageVue({
        data: {
            list_api_tag: 'api:customer-list',
            delete_api_tag: 'api:customer-delete',
            detail_api_tag: 'api:customer-detail',

            create_url_tag: 'customer:customer-add',
            list_url_tag: 'customer:customer-list',
            detail_url_tag: 'customer:customer-detail',
            update_url_tag: 'customer:customer-update'
        }
    }
);
