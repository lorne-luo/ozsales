var OrderEditPageVue = Vue.extend({
    el: function(){
        return '#orderproduct';
    },
    data: function(){
        return {
            list_api_tag:undefined,
            create_url_tag:undefined,
            detail_url_tag:undefined,
            update_url_tag:undefined,
            delete_api_tag:undefined,
            list_url_tag:undefined,
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
            var $product_template = $("#product_template");
            var $product_template_copy = $product_template.children().clone(false);
            console.log($product_template_copy);
            $("#product_table").append($product_template_copy);

            $("select[class$='form-control']").not(".hide select[class$='form-control']")
                    .chosen({search_contains: true,disable_search_threshold: 10});
        }
    }
});


