var OrderEditPageVue = Vue.extend({
    el: function () {
        return '#orderproduct';
    },
    data: function () {
        return {
            list_api_tag: undefined,
            create_url_tag: undefined,
            detail_url_tag: undefined,
            update_url_tag: undefined,
            delete_api_tag: undefined,
            list_url_tag: undefined,
            items: [],
            userName: $("#adminlte_page_user_name").val(),
            appName: $("#adminlte_page_app_name").val(),
            modelName: $("#adminlte_page_model_name").val(),
            currentPage: 1,
            totalPage: 1,
            perPage: 10,
            count: 0
        }
    },
    ready: function () {

    },
    methods: {
        add_product: function (event) {
            var order_pk = $("input#order_pk").val();

            var $TOTAL_FORMS = $("#product_table input#id_form-TOTAL_FORMS");
            $("#product_table input#id_form-" + ($TOTAL_FORMS.val() - 1) + "-order").val(order_pk);

            var $product_template = $("#product_template");
            var $product_template_copy = $product_template.children().clone(false);
            var base_id = "id_form-" + $TOTAL_FORMS.val();
            var base_name = "form-" + $TOTAL_FORMS.val();

            $("input#id_order", $product_template_copy).val(order_pk);
            $("input#id_order", $product_template_copy).attr("name", base_name + "-order");
            $("input#id_order", $product_template_copy).attr("id", base_id + "-order");

            $("select#id_product", $product_template_copy).attr("name", base_name + "-product");
            $("select#id_product", $product_template_copy).attr("id", base_id + "-product");

            $("input#id_name", $product_template_copy).attr("name", base_name + "-name");
            $("input#id_name", $product_template_copy).attr("id", base_id + "-name");

            $("input#id_amount", $product_template_copy).attr("name", base_name + "-amount");
            $("input#id_amount", $product_template_copy).attr("id", base_id + "-amount");

            $("input#id_sell_price_rmb", $product_template_copy).attr("name", base_name + "-sell_price_rmb");
            $("input#id_sell_price_rmb", $product_template_copy).attr("id", base_id + "-sell_price_rmb");

            $("input#id_sum_price", $product_template_copy).attr("name", base_name + "-sum_price");
            $("input#id_sum_price", $product_template_copy).attr("id", base_id + "-sum_price");

            $("input#id_cost_price_aud", $product_template_copy).attr("name", base_name + "-cost_price_aud");
            $("input#id_cost_price_aud", $product_template_copy).attr("id", base_id + "-cost_price_aud");

            $("select#id_store", $product_template_copy).attr("name", base_name + "-store");
            $("select#id_store", $product_template_copy).attr("id", base_id + "-store");

            $product_template_copy.attr('id', 'form-' + $TOTAL_FORMS.val());
            var $element = $("#product_table").append($product_template_copy);
            this.$compile($element.get(0)); // link event for delete button
            $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) + 1);

            $("select[class$='form-control']").not(".hide select[class$='form-control']")
                .chosen({search_contains: true, disable_search_threshold: 10});
        },
        add_express: function (event) {
            var order_pk = $("input#order_pk").val();

            var $TOTAL_FORMS = $("#express_table input#id_form-TOTAL_FORMS");
            $("#express_table input#id_form-" + ($TOTAL_FORMS.val() - 1) + "-order").val(order_pk);

            var $express_template = $("#express_template");
            var $express_template_copy = $express_template.children().clone(false);
            var base_id = "id_form-" + $TOTAL_FORMS.val();
            var base_name = "form-" + $TOTAL_FORMS.val();

            $("input#id_order", $express_template_copy).val(order_pk);
            $("input#id_order", $express_template_copy).attr("name", base_name + "-order");
            $("input#id_order", $express_template_copy).attr("id", base_id + "-order");

            $("select#id_carrier", $express_template_copy).attr("name", base_name + "-carrier");
            $("select#id_carrier", $express_template_copy).attr("id", base_id + "-carrier");

            $("input#id_track_id", $express_template_copy).attr("name", base_name + "-track_id");
            $("input#id_track_id", $express_template_copy).attr("id", base_id + "-track_id");

            $("input#id_fee", $express_template_copy).attr("name", base_name + "-fee");
            $("input#id_fee", $express_template_copy).attr("id", base_id + "-fee");

            $("input#id_weight", $express_template_copy).attr("name", base_name + "-weight");
            $("input#id_weight", $express_template_copy).attr("id", base_id + "-weight");

            $("input#id_id_upload", $express_template_copy).attr("name", base_name + "-id_upload");
            $("input#id_id_upload", $express_template_copy).attr("id", base_id + "-id_upload");

            $express_template_copy.attr('id', 'form-' + $TOTAL_FORMS.val());
            var $element = $("#express_table").append($express_template_copy);
            this.$compile($element.get(0)); // link event for delete button
            $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) + 1);

            $("select[class$='form-control']").not(".hide select[class$='form-control']")
                .chosen({search_contains: true, disable_search_threshold: 10});
        },
        submit: function (event) {
            var total_forms = parseInt($("input#id_form-TOTAL_FORMS").val());
            var order_pk = $("input#order_pk").val();
            // set order id for each form
            for (var i = 0; i < total_forms; i++) {
                if ($("input#id_form-" + i + "-product").val() || $("input#id_form-" + i + "-name").val())
                    $("input#id_form-" + i + "-order").val(order_pk);
            }
            // add next url into form if click save & continue
            if ($(event.target).attr('name') == '_continue') {
                $('<input>').attr({
                    type: 'hidden',
                    id: 'next',
                    name: 'next',
                    value: window.location
                }).appendTo('#commonForm');
            }
            document.getElementById("commonForm").submit();
        },
        delete_product: function (event) {
            var $TOTAL_FORMS = $("#product_table input#id_form-TOTAL_FORMS");
            var product = $(event.target).closest('div.form-group');
            console.log(product[0]);
            var orderProductID = $("input:hidden[id$='-id']", product).val();
            if (orderProductID) {
                swal({
                    title: "确定删除",
                    text: "确定删除所选产品?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    closeOnConfirm: true,
                    showLoaderOnConfirm: false
                }, function () {
                    var deleteUrl = Urls['order:api-orderproduct-delete']();
                    $.AdminLTE.apiDelete(
                        deleteUrl,
                        $.param({'pk': orderProductID}),
                        function (resp) {
                            product.remove();
                            $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
                        }
                    );
                });
            } else {
                product.remove();
                $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
            }
        },
        delete_express: function (event) {
            var $TOTAL_FORMS = $("#express_table input#id_form-TOTAL_FORMS");
            var express = $(event.target).closest('div.form-group');
            console.log(express[0]);
            var orderExpressID = $("input:hidden[id$='-id']", express).val();
            console.log(orderExpressID);
            if (orderExpressID) {
                swal({
                    title: "确定删除",
                    text: "确定删除所选快递信息?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    closeOnConfirm: true,
                    showLoaderOnConfirm: false
                }, function () {
                    var deleteUrl = Urls['express:api-expressorder-delete']();
                    $.AdminLTE.apiDelete(
                        deleteUrl,
                        $.param({'pk': orderExpressID}),
                        function (resp) {
                            express.remove();
                            $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
                        }
                    );
                });
            } else {
                express.remove();
                $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
            }
        }

    }
});


