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
        addone: function (event) {
            var order_pk = $("input#order_pk").val();

            var $TOTAL_FORMS = $("input#id_form-TOTAL_FORMS");
            $("input#id_form-" + ($TOTAL_FORMS.val() - 1) + "-order").val(order_pk);

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
            $("#product_table").append($product_template_copy);
            $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) + 1);

            $("select[class$='form-control']").not(".hide select[class$='form-control']")
                .chosen({search_contains: true, disable_search_threshold: 10});
        }
    }
});


