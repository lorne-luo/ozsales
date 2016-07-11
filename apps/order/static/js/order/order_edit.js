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

      $("select[class$='form-control']").not(".hide select[class$='form-control']")
        .chosen({search_contains: true, disable_search_threshold: 10});
    },
    add_express: function (event) {
      var order_pk = $("input#order_pk").val();
      var form_name = "express_orders";
      var base = "id_" + form_name;

      var $TOTAL_FORMS = $("#express_table input#" + base + "-TOTAL_FORMS");
      // $("#express_table input#id_express_orders-" + ($TOTAL_FORMS.val() - 1) + "-order").val(order_pk);

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

      $("select[class$='form-control']").not(".hide select[class$='form-control']")
        .chosen({search_contains: true, disable_search_threshold: 10});
    },
    submit: function (event) {
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
      var $TOTAL_FORMS = $("#product_table input#id_products-TOTAL_FORMS");
      var product = $(event.target).closest('div.form-group');

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
              // product.remove();
              // $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
              location.reload();
            }
          );
        });
      } else {
        product.remove();
        $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
      }
    },
    delete_express: function (event) {
      var $TOTAL_FORMS = $("#express_table input#id_express_orders-TOTAL_FORMS");
      var express = $(event.target).closest('div.form-group');

      var orderExpressID = $("input:hidden[id$='-id']", express).val();
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
              // express.remove();
              // $TOTAL_FORMS.val(parseInt($TOTAL_FORMS.val()) - 1);
              location.reload();
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


