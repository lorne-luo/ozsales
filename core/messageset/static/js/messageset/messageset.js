/**
 * messageset app js
 * 右上角站内消息、系统通知通知js
 */
var messagesetVue = new Vue({
    el: '.messagesetVue',
    data: {
        sitemailreceive: [],
        notification: [],
        task: [],
        appName: 'messageset'
    },
    ready: function () {
        var status_data = {'status': 0};
        this.loadData('sitemailreceive');
        // this.loadData('notification', status_data);
        // this.loadData('task', status_data);
    },
    methods: {
        detail: function (model, event) {
            var self = this;
            window.location.href = Urls[self.appName + ":" + model + "-detail"](
                $(event.target).data('pk')
            );
        },
        sitemailDetail: function (event) {
            this.detail('sitemailreceive', event);
        },
        taskDetail: function (event) {
            this.detail('task', event);
        },
        notificationDetail: function (event) {
            this.detail('notification', event);
        },
        loadData: function (modelName, data) {
            var self = this,
                url = $.AdminLTE.getApiUrl(self.appName, modelName);
            $.ajax({
                type: 'GET',
                url: url,
                data: data,
                dataType: 'json',
                error: function (response) {
                    if (response.status == 403) {
                    }
                    switch (modelName) {
                        case 'sitemailreceive':
                            $('li.messages-menu').hide();
                            break;
                        case 'notification':
                            $('li.notifications-menu').hide();
                            break;
                        case 'task':
                            $('li.tasks-menu').hide();
                            break;
                        default:
                            break;
                    }
                },
                success: function (resp) {
                    self[modelName] = resp.results;
                }
            });
        },
        mark_readed:function(){
            $.AdminLTE.apiPost(
                Urls['api:sitemail_markall'](), {},
                function (resp) {
                    //todo remove number badge
                    console.log("todo remove number badge");
                }
            );
        }
    }
});
