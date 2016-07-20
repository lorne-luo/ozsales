var CustomerListPageVue = CommonListPageVue.extend({
    methods: {
        show_address: function (pk, event) {
            // alert(pk);
            // return;
            if (event.target.tagName.toUpperCase() == 'TD' || $(event.target).closest('td').hasClass('show_address')) {
                // $('#address_set_' + pk).toggleClass('hide');
                var tr = $(event.target).closest('tr');
                var td = $('td.show_address', tr);
                if ($('#address_set_' + pk).toggleClass('hide').hasClass('hide')) {
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
                if (th.hasClass('extend')) {
                    $('#address_set_' + pk).removeClass('hide');
                    $(this).html('<i class="fa fa-minus-square text-primary" aria-hidden="true"></i>');
                } else {
                    $('#address_set_' + pk).addClass('hide');
                    $(this).html('<i class="fa fa-plus-square text-primary" aria-hidden="true"></i>');
                }
            });
        },
    }
});

var customerListPageVue = new CustomerListPageVue({
        data: {
            list_api_tag:   'customer:api-customer-list',
            delete_api_tag: 'customer:api-customer-delete',
            detail_api_tag: 'customer:api-customer-detail',

            create_url_tag: 'customer:customer-add',
            list_url_tag:   'customer:customer-list',
            detail_url_tag: 'customer:customer-detail',
            update_url_tag: 'customer:customer-update'
        }
    }
);
