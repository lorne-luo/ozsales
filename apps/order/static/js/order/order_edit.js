var OrderEditPageVue = CommonFormPageVue.extend({
    data: function () {
        return {
            list_api_tag: 'order:api-order-list',
            delete_api_tag: 'order:api-order-delete',
            detail_api_tag: 'order:api-order-detail',

            create_url_tag: 'order:order-add',
            list_url_tag:   'order:order-list-short',
            detail_url_tag: 'order:order-detail',
            update_url_tag: 'order:order-update'
        }
    },
    methods: {
        add_product: function (event) {
            var form_name = "products";
            var fields = ["id", "order", "product", "name", "amount", "sell_price_rmb", "sum_price", "cost_price_aud", "store"];
            this.add_item(form_name, fields);
        },
        add_express: function (event) {
            var form_name = "express_orders";
            var fields = ["id", "order", "carrier", "track_id", "fee", "weight", "id_upload"];
            this.add_item(form_name, fields);
        },
        delete_product: function (event) {
            var url_tag = 'order:api-orderproduct-delete';
            var fields = ["id", "order", "product", "name", "amount", "sell_price_rmb", "sum_price", "cost_price_aud", "store"];
            this.delete_item(event, url_tag, fields);
        },
        delete_express: function (event) {
            var url_tag = 'express:api-expressorder-delete';
            var fields = ["id", "order", "carrier", "track_id", "fee", "weight", "id_upload"];
            this.delete_item(event, url_tag, fields);
        },
        submit: function (event) {
            var object_id = $("input#object_id").val();
            var product_count = parseInt($("input#id_products-TOTAL_FORMS").val());

            // add order id for products
            for (var i = 0; i < product_count; i++) {
                var item = $("div.form-group#products-" + i);
                var product = $("#id_products-" + i + "-product", item);
                var product_name = $("#id_products-" + i + "-name", item);
                var order = $("#id_products-" + i + "-order", item);

                if (product.val() || product_name.val()) {
                    order.val(object_id);
                }
            }

            this.fill_related('express_orders','track_id','order');

        }
    }
});
