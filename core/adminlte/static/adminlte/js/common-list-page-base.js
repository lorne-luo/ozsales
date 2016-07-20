var CommonListPageVue = Vue.extend({
    el: function(){
        return '#commonDataTableRow';
    },
    data: function(){
        return {
            // api
            list_api_tag:undefined,
            delete_api_tag:undefined,
            detail_api_tag:undefined,
            // page
            create_url_tag:undefined,
            list_url_tag:undefined,
            detail_url_tag:undefined,
            update_url_tag:undefined,
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
        if(this.appName && this.modelName){
            this.loadData({});
        }

        var create_btn=$('a#create');
        create_btn.prop('href',Urls[this.create_url_tag]());
    },
    methods: {
        toggleAllBox: function (event) {
            var table=$(event.target).closest('table');
            $("input[name='checkboxRow']", table).prop(
                'checked',
                $(event.target).prop('checked')
            );
        },
        detail: function (event) { // to be removed
            var pk;
            if ($(event.target).data('pk'))
                pk = $(event.target).data('pk');
            else if ($(event.target.parentNode).data('pk'))
                pk = $(event.target.parentNode).data('pk');
            else{
                swal('错误', '无法获取pk', 'error');
                return;
            }

            var url;
            if (this.detail_url_tag){
                url = Urls[this.detail_url_tag](pk);
            }else{
                url = Urls['adminlte:common_detail_page'](
                    this.appName,
                    this.modelName,
                    pk
                );
            }
            window.location.href = url;
        },
        update: function (event) { // to be removed
            var pk;
            if ($(event.target).data('pk'))
                pk = $(event.target).data('pk');
            else if ($(event.target.parentNode).data('pk'))
                pk = $(event.target.parentNode).data('pk');
            else{
                swal('错误', '无法获取pk', 'error');
                return;
            }

            var url;
            if (this.update_url_tag)
                url = Urls[this.update_url_tag](pk);
            else
                url = Urls['adminlte:common_update_page'](
                    this.appName,
                    this.modelName,
                    pk
                );
            window.location.href = url;
        },
        remove: function (ids) {
            var self = this;
            var delUrl;
            if (this.delete_api_tag)
                delUrl = Urls[this.delete_api_tag]();
            else
                delUrl = Urls['adminlte:common_delete_page'](self.appName, self.modelName);
            swal({
                    title: "确定要删除吗?",
                    text: "您确定要删除所选数据吗?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    closeOnConfirm: false,
                    showLoaderOnConfirm: true,
                    animation: false
                }, function () {
                    $.AdminLTE.apiDelete(
                        delUrl,
                        $.param({'pk': ids.toString()}),
                        function (resp) {
                            self.loadData({});
                            swal({
                                title: "删除成功!",
                                type: "success",
                                animation: false
                            });
                            $('input.checkboxAllRow').prop( "checked", false);
                        }
                    );
                });
        },
        removeSelected: function () {
            var ids = [], box = null;
            if($(".content .tab-pane.active").size()>0)
                box = $(".content .tab-pane.active input[name='checkboxRow']:checked");
            else
                box = $(".content input[name='checkboxRow']:checked");

            $.each(box, function (i, b) {
                ids.push($(b).val());
            });
            
            if (ids.length === 0) {
                swal({
                    title: "请选择数据!",
                    type: "warning",
                    animation: false
                });
                return;
            }
            this.remove(ids);
        },
        removeOne: function (event) {
            var pk;
            if ($(event.target).data('pk'))
                pk = $(event.target).data('pk');
            else if ($(event.target.parentNode).data('pk'))
                pk = $(event.target.parentNode).data('pk');
            else{
                swal('错误', '无法获取pk', 'error');
                return;
            }
            this.remove(pk);
        },
        search: function (event) {
            this.loadData(
                $.param({'search': $("#tableSearch").val()})
            );
        },
        resetSearch: function (event) {
            $("#tableSearch").val('');
            this.search(event);
        },
        page: function (event) {
            var num = $(event.target).attr('page');
            this.loadData({'page': num});
        },
        loadData: function (data) {
            var self = this;
            var url;
            if (self.list_api_tag)
                url = Urls[self.list_api_tag]();
            else
                url = $.AdminLTE.getApiUrl(self.appName, self.modelName);

            $.AdminLTE.apiGet(
                url,
                data,
                function (resp) {
                    self.items = resp.results;
                    self.count = resp.count;
                    self.perPage = resp.per_page;
                    self.totalPage = resp.total_page;
                    self.currentPage = resp.current_page;
                }
            );
        }
    }
});