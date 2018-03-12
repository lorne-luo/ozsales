var CommonFormPageVue = Vue.extend({
    el: function () {
        return 'form#commonForm';
    },
    methods: {
        add_item: function (form_name, fields) {
            var $TOTAL_FORMS = $("input#id_" + form_name + "-TOTAL_FORMS");
            var template_id = form_name + "_template";
            var $template = $("#" + template_id);
            var $template_copy = $template.children().clone(false);
            var base_id = "id_" + form_name + "-" + $TOTAL_FORMS.val();
            var base_name = form_name + "-" + $TOTAL_FORMS.val();

            for (var i in fields) {
                var field = fields[i];
                var input = $("#id_" + form_name + "-" + field, $template_copy);
                input.attr("name", base_name + "-" + field);
                input.attr("id", base_id + "-" + field);
            }

            $template_copy.attr('id', base_name);
            var table_id = form_name + "_table";
            var $element = $("#" + table_id).append($template_copy);
            this.$compile($element.get(0)); // link event for delete button
            $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) + 1);

            this.reset_row_color(form_name);
            $("select[class$='form-control']").not(".hide select[class$='form-control']")
                .chosen({search_contains: true, disable_search_threshold: 10});
        },
        delete_item: function (event, delete_url_tag, fields) {
            var self = this;
            var item = $(event.target).closest('div.form-group');
            var id_input = $("input:hidden[id$='-id']", item);
            var pk = id_input.val();

            if (pk) {
                swal({
                    title: "确定删除",
                    text: "确定删除所选信息?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    closeOnConfirm: true,
                    showLoaderOnConfirm: false,
                    animation: false
                }, function () {
                    var deleteUrl = Urls[delete_url_tag]();
                    $.AdminLTE.apiPost(
                        deleteUrl,
                        $.param({'pk': pk}),
                        function (resp) {
                            self.remove_item(item, fields);
                        }
                    );
                });
            } else {
                self.remove_item(item, fields);
            }
        },
        remove_item: function (item, fields) {
            var arr = item.get(0).id.split('-');
            var number = parseInt(arr[arr.length - 1]);
            var form_name = arr[0];

            if (item.attr('data-pk')) {
                var $INITIAL_FORMS = $("input#id_" + form_name + "-INITIAL_FORMS");
                $INITIAL_FORMS.val(parseInt($INITIAL_FORMS.val()) - 1);
            }
            item.remove();

            var $TOTAL_FORMS = $("input#id_" + form_name + "-TOTAL_FORMS");
            var total = parseInt($TOTAL_FORMS.val());
            for (var i = number + 1; i < total; i++) {
                var item = $("div#" + form_name + "-" + i);
                var base_id = "id_" + form_name + "-" + i;
                var new_base_name = form_name + "-" + (i - 1);
                var new_base_id = "id_" + form_name + "-" + (i - 1);

                for (var j in fields) {
                    var field = fields[j];
                    var input = $("#" + base_id + "-" + field, item);
                    input.attr("name", new_base_name + "-" + field);
                    input.attr("id", new_base_id + "-" + field);
                }
                item.attr("id", new_base_name);
            }
            this.reset_row_color(form_name);
            $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
        },
        reset_row_color: function (form_name) {
            var count = parseInt($("input#id_" + form_name + "-TOTAL_FORMS").val());
            for (var i = 0; i < count; i++) {
                var item = $("div.form-group#" + form_name + "-" + i);
                if (i % 2)
                    item.removeClass('even').addClass('odd');
                else
                    item.removeClass('odd').addClass('even');
            }
        },
        fill_related: function (form_name, member_name, foreign_field) {
            var object_id = $("input#object_id").val();
            var count = parseInt($("input#id_" + form_name + "-TOTAL_FORMS").val());

            for (var i = 0; i < count; i++) {
                var item = $("div.form-group#" + form_name + "-" + i);
                var key_member = $("#id_" + form_name + "-" + i + "-" + member_name, item);
                var related = $("#id_" + form_name + "-" + i + "-" + foreign_field, item);

                if (key_member.val() && !related.val()) {
                    related.val(object_id);
                }
            }
        },
        delete: function (pk, event) {
            var self = this;
            swal({
                title: "确定删除",
                text: "确定删除本条记录? 所有相关数据均会一并删除。",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                closeOnConfirm: true,
                showLoaderOnConfirm: false,
                animation: false
            }, function () {
                var deleteUrl = Urls[self.delete_api_tag]();
                $.AdminLTE.apiPost(
                    deleteUrl,
                    $.param({'pk': pk}),
                    function (resp) {
                        var list_url = Urls[self.list_url_tag]();
                        window.location.replace(list_url);
                    }
                );
            });
        }
    }
});
