var OrderEditPageVue = CommonFormPageVue.extend({
    ready: function () {
        $('input').not('[id$="-DELETE"]').iCheck({
            checkboxClass: 'icheckbox_square-blue',
            radioClass: 'iradio_square-blue',
            increaseArea: '20%' // optional
        });

        $("#address-text").text($("#id_address option:selected").text());
        $("#id_address").change(function () {
            $("#address-text").text($("option:selected", this).text());
        });
    }
});

var orderEditPageVue = new OrderEditPageVue({
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
        list_url: Urls['api:order-list']()
    }
});