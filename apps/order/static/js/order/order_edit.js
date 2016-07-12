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
  ready: function () {

  },
  methods: {
    add_product: function (event) {
      var order_pk = $("input#order_pk").val();
      var form_name = "products";
      var base = "id_" + form_name;

      var $TOTAL_FORMS = $("#product_table input#" + base + "-TOTAL_FORMS");
      var $product_template = $("#product_template");
      var $product_template_copy = $product_template.children().clone(false);
      var base_id = base + "-" + $TOTAL_FORMS.val();
      var base_name = form_name + "-" + $TOTAL_FORMS.val();

      var fields = ["order", "product", "name", "amount", "sell_price_rmb", "sum_price", "cost_price_aud", "store"];
      for (var i in fields) {
        var field = fields[i];
        var input = $("#" + base + "-" + field, $product_template_copy);
        input.attr("name", base_name + "-" + field);
        input.attr("id", base_id + "-" + field);
      }
      $("#" + base_id + "-order", $product_template_copy).val(order_pk); //set up order_id

      $product_template_copy.attr('id', base_name);
      var $element = $("#product_table").append($product_template_copy);
      this.$compile($element.get(0)); // link event for delete button
      $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) + 1);

      this.reset_row_color(form_name);
      $("select[class$='form-control']").not(".hide select[class$='form-control']")
        .chosen({search_contains: true, disable_search_threshold: 10});
    },
    add_express: function (event) {
      var order_pk = $("input#order_pk").val();
      var form_name = "express_orders";
      var base = "id_" + form_name;

      var $TOTAL_FORMS = $("#express_table input#" + base + "-TOTAL_FORMS");
      var $express_template = $("#express_template");
      var $express_template_copy = $express_template.children().clone(false);
      var base_id = base + "-" + $TOTAL_FORMS.val();
      var base_name = form_name + "-" + $TOTAL_FORMS.val();

      var fields = ["order", "carrier", "track_id", "fee", "weight", "id_upload"];
      for (var i in fields) {
        var field = fields[i];
        var input = $("#" + base + "-" + field, $express_template_copy);
        input.attr("name", base_name + "-" + field);
        input.attr("id", base_id + "-" + field);
      }
      $("#" + base_id + "-order", $express_template_copy).val(order_pk); //set up order_id

      $express_template_copy.attr('id', base_name);
      var $element = $("#express_table").append($express_template_copy);
      this.$compile($element.get(0)); // link event for delete button
      $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) + 1);

      this.reset_row_color(form_name);
      $("select[class$='form-control']").not(".hide select[class$='form-control']")
        .chosen({search_contains: true, disable_search_threshold: 10});
    },
    delete_product: function (event) {
      var self = this;
      var form_name = "products";
      var $TOTAL_FORMS = $("input#id_" + form_name + "-TOTAL_FORMS");
      var total = parseInt($TOTAL_FORMS.val());
      var product = $(event.target).closest('div.form-group');
      var id_input = $("input:hidden[id$='-id']", product);

      var orderProductID = id_input.val();
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
              var arr = id_input.get(0).id.split('-');
              var number = parseInt(arr[arr.length - 2]);
              var fields = ["id", "order", "product", "name", "amount", "sell_price_rmb", "sum_price", "cost_price_aud", "store"];

              product.remove();
              var $INITIAL_FORMS = $("input#id_" + form_name + "-INITIAL_FORMS");
              $INITIAL_FORMS.val(parseInt($INITIAL_FORMS.val()) - 1);

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
              self.reset_row_color(form_name);
              $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
            }
          );
        });
      } else {
        product.remove();
        self.reset_row_color(form_name);
        $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
      }
    },
    delete_express: function (event) {
      var self = this;
      var form_name = "express_orders";
      var $TOTAL_FORMS = $("input#id_" + form_name + "-TOTAL_FORMS");
      var total = parseInt($TOTAL_FORMS.val());
      var express = $(event.target).closest('div.form-group');
      var id_input = $("input:hidden[id$='-id']", express);
      var orderExpressID = id_input.val();

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
              var arr = id_input.get(0).id.split('-');
              var number = parseInt(arr[arr.length - 2]);
              var fields = ["id", "order", "carrier", "track_id", "fee", "weight", "id_upload"];

              express.remove();
              // var $INITIAL_FORMS = $("#express_table input#id_express_orders-INITIAL_FORMS");
              var $INITIAL_FORMS = $("input#id_" + form_name + "-INITIAL_FORMS");
              $INITIAL_FORMS.val(parseInt($INITIAL_FORMS.val()) - 1);

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
              self.reset_row_color(form_name);
              $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
            }
          );
        });
      } else {
        express.remove();
        self.reset_row_color(form_name);
        $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
      }
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


