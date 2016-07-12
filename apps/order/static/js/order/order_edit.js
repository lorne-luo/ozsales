var OrderEditPageVue = Vue.extend({
  el: function () {
    return 'form#commonForm';
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
  methods: {
    add_product: function (event) {
      var form_name = "products";
      var fields = ["order", "product", "name", "amount", "sell_price_rmb", "sum_price", "cost_price_aud", "store"];
      this.add_item(form_name, fields);
    },
    add_express: function (event) {
      var form_name = "express_orders";
      var fields = ["order", "carrier", "track_id", "fee", "weight", "id_upload"];
      this.add_item(form_name, fields);
    },
    add_item: function (form_name, fields) {
      var order_pk = $("input#order_pk").val();

      var $TOTAL_FORMS = $("input#id_" + form_name + "-TOTAL_FORMS");
      var template_id = form_name + "_template";
      var $template = $("#" + template_id);
      var $template_copy = $template.children().clone(false);
      var base_id = "id_" + form_name + "-" + $TOTAL_FORMS.val();
      var base_name = form_name + "-" + $TOTAL_FORMS.val();
      console.log($template.get(0));

      for (var i in fields) {
        var field = fields[i];
        var input = $("#id_" + form_name + "-" + field, $template_copy);
        console.log(input.get(0));
        input.attr("name", base_name + "-" + field);
        input.attr("id", base_id + "-" + field);
      }
      $("#" + base_id + "-order", $template_copy).val(order_pk); //set up order_id

      $template_copy.attr('id', base_name);
      var table_id = form_name + "_table";
      var $element = $("#" + table_id).append($template_copy);
      this.$compile($element.get(0)); // link event for delete button
      $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) + 1);

      this.reset_row_color(form_name);
      $("select[class$='form-control']").not(".hide select[class$='form-control']")
        .chosen({search_contains: true, disable_search_threshold: 10});
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
          showLoaderOnConfirm: false
        }, function () {
          var deleteUrl = Urls[delete_url_tag]();
          $.AdminLTE.apiDelete(
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
    submit: function (event) {
      var order_pk = $("input#order_pk").val();
      var product_count = parseInt($("input#id_products-TOTAL_FORMS").val());
      var express_count = parseInt($("input#id_express_orders-TOTAL_FORMS").val());

      // add order id for products
      for (var i = 0; i < product_count; i++) {
        var item = $("div.form-group#products-" + i);
        var product = $("#id_products-" + i + "-product", item);
        var product_name = $("#id_products-" + i + "-name", item);

        if (product.val() || product_name.val()) {
          var order = $("#id_products-" + i + "-order", item);
          order.val(order_pk);
        }
      }

      // add order id for express
      for (var i = 0; i < express_count; i++) {
        var item = $("div.form-group#express_orders-" + i);
        var track_id = $("#id_express_orders-" + i + "-track_id", item);

        if (track_id.val()) {
          var order = $("#id_express_orders-" + i + "-order", item);
          order.val(order_pk);
        }
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
    }
  }
});
