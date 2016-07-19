var CustomerEditPageVue = CommonFormPageVue.extend({
    methods: {
        add_address: function (event) {
            var form_name = "address_set";
            var fields = ["customer", "name", "mobile", "address", "id_number", "id_photo_front", "id_photo_back"];
            this.add_item(form_name, fields);
        },
        delete_address: function (event) {
            var url_tag = 'customer:api-address-delete';
            var fields = ["id", "customer", "name", "mobile", "address", "id_number", "id_photo_front", "id_photo_back"];
            this.delete_item(event, url_tag, fields);
        },
        submit: function (event) {
            this.fill_related('address_set','name','customer');
        }
    }
});
