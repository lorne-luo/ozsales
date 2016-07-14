var sitemailListPageVue = new CommonListPageVue({
    el: '#siteMailContentRow',
    data: {
        firstCount: true,
        unReadItemsCount: 0,
        showBox: 'in',
        add_api_tag: 'messageset:api-sitemailreceive-list',
        list_api_tag: 'messageset:api-sitemailreceive-list',
        delete_api_tag: 'messageset:api-sitemailreceive-delete',
        retrieve_api_tag: 'messageset:api-sitemailreceive-detail',
        update_api_tag: 'messageset:api-sitemailreceive-detail',
        destroy_api_tag: 'messageset:api-sitemailreceive-detail',

        create_url_tag: 'messageset:sitemail-add',
        receive_detail_url_tag: 'messageset:sitemailreceive-detail',
        send_detail_url_tag: 'messageset:sitemailsend-detail',
        update_url_tag: 'messageset:sitemailreceive-update'
    },
    ready: function () {
        if (this.appName && this.modelName) {
            this.loadData({});
        }
    },
    methods: {
        newMail: function(event){
            window.location.href = Urls[this.create_url_tag]();
        },
        inBox: function (event) {
            $(event.target).parent().siblings().removeClass('active');
            $(event.target).parent().addClass('active');
            this.showBox = 'in';
            this.modelName = 'sitemailreceive';
            this.list_api_tag = 'messageset:api-sitemailreceive-list';
            this.loadData({});
        },
        sendBox: function (event) {
            $(event.target).parent().siblings().removeClass('active');
            $(event.target).parent().addClass('active');
            this.showBox = 'send';
            this.modelName = 'sitemailsend';
            this.list_api_tag = 'messageset:api-sitemailsend-list';
            this.loadData({});
        },
        trashBox: function (event) {
            $(event.target).parent().siblings().removeClass('active');
            $(event.target).parent().addClass('active');
            this.loadData({});
        },
        mailDetail: function (event) {
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
            if (this.showBox == 'in')
                url = Urls[this.receive_detail_url_tag](pk);
            else
                url = Urls[this.send_detail_url_tag](pk);
            window.location.href = url;
        },
        filterStatus: function (status, event) {
            var self = this, data = {};
            if (status !== -1) {
                data = {'status': status};
            }
            self.loadData(data);
            $(event.target).siblings('.btn-primary').removeClass('btn-primary').addClass('btn-link');
            $(event.target).addClass('btn-primary').removeClass('btn-link');
        },
        allStatus: function (event) {
            this.filterStatus(-1, event);
        },
        unReadStatus: function (event) {
            this.filterStatus(0, event);
        },
        readStatus: function (event) {
            this.filterStatus(1, event);
        },
        markAllRead: function () {
            var self = this;
            swal({
                title: "您确定要全部标记为已读吗?",
                type: "info",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确定!",
                cancelButtonText: "取消",
                closeOnConfirm: false,
                showLoaderOnConfirm: true,
                animation: false
            }, function () {
                $.AdminLTE.apiPatch(
                    Urls['messageset:api-sitemail_markall'](), {},
                    function (resp) {
                        swal({
                            title: "标识更新成功!",
                            type: "success",
                            animation: false
                        }, function () {
                            self.loadData({});
                        });
                    }
                );
            });
        }
    }
});


sitemailListPageVue.$watch('items', function (items) {
    if (sitemailListPageVue.firstCount) {
        var count = 0;
        if (sitemailListPageVue.unReadItemsCount === 0) {
            $.each(items, function (i, item) {
                if (item.status_value === 0 ) {
                    count++;
                }
            });
        }
        sitemailListPageVue.unReadItemsCount = count;
    }
    sitemailListPageVue.firstCount = false;
});