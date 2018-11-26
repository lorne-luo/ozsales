var OrderPurchasePageVue = CommonListPageVue.extend({
    el: function () {
        return '#purchase-mode-table';
    },
    ready: function (event) {
        console.log(4);
    },
    methods: {
        ready: function (event) {
            console.log(3);
        },
        makr_as_purchased: function (event) {
            console.log(2);
            var productID = $(event.target).val();
            var value = $(event.target).prop("checked");
            var url = Urls[this.product_detail_api_tag](productID);
            $.AdminLTE.apiPost(
                url,
                $.param({'is_purchased': value}),
                function (resp) {
                }
            );
        },
        show_detail: function (pk, event) {
            console.log(1);
            if (event.target.tagName.toUpperCase() == 'TD' || $(event.target).hasClass('show_detail')) {
                var table = $(event.target).closest('table');
                var tr = $(event.target).closest('tr');
                var icon = $('i.show_detail', tr);
                if ($('.detail_' + pk, table).toggleClass('hide').hasClass('hide')) {
                    icon.removeClass("fa-minus-square");
                    icon.addClass("fa-plus-square");
                } else {
                    icon.addClass("fa-minus-square");
                    icon.removeClass("fa-plus-square");
                }
            }
        },
        show_all_detail: function (event) {
            var table = $(event.target).closest('table');
            var icon_all = $('i.show_all_detail', table);
            if (icon_all.toggleClass('extend').hasClass('extend')) {
                icon_all.addClass("fa-minus-square");
                icon_all.removeClass("fa-plus-square");
            }
            else {
                icon_all.removeClass("fa-minus-square");
                icon_all.addClass("fa-plus-square");
            }

            var icons = $('i.show_detail', table);
            icons.each(function (index) {
                var pk = $(this).attr('data-pk');
                if (icon_all.hasClass('extend')) {
                    $('#detail_' + pk).removeClass('hide');
                    $(this).addClass("fa-minus-square");
                    $(this).removeClass("fa-plus-square");
                } else {
                    $('#detail_' + pk).addClass('hide');
                    $(this).removeClass("fa-minus-square");
                    $(this).addClass("fa-plus-square");
                }
            });
        },
    }
});

var orderPurchasePageVue = new OrderPurchasePageVue({
        data: {
            // API
            list_api_tag: 'api:order-list',
            detail_api_tag: 'api:order-detail',
            product_detail_api_tag: 'api:orderproduct-detail',
            delete_api_tag: 'api:order-delete',
            // page
            create_url_tag: 'order:order-add',
            list_url_tag: 'order:order-list-short',
            update_url_tag: 'order:order-update',
            detail_url_tag: 'order-detail-short',
            list_url: Urls['api:order-list'](),
        }
    }
);
