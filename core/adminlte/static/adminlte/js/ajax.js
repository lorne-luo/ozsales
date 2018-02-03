(function ($) {
    var getCookie = function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    var csrftoken = getCookie('csrftoken');

    var csrfSafeMethod = function (method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var sendRequest = function (type, url, data, callback) {
        $.ajax({
            type: type,
            url: url,
            data: data,
            dataType: 'json',
            cache: false,
            error: function (response) {
                var text;
                switch (response.status) {
                    case 400:
                        text = '错误请求!';
                        break;
                    case 403:
                        text = '对不起，没有权限进行此操作!';
                        break;
                    case 404:
                        text = '找不到该对象或页面!';
                        break;
                    case 405:
                        text = '不允许该访问方法!';
                        break;
                    case 500:
                        text = '服务器错误!';
                        break;
                    default:
                        text = '操作失败，错误码' + response.status;
                        break;
                }
                swal({
                    title: text,
                    type: "error",
                    animation: false
                });
            },
            success: callback
        });
    };

    $.AdminLTE.getApiUrl = function (app, model) {
        return '/api/' + app + '/' + model + '/';
    };

    $.AdminLTE.apiGet = function (url, data, callback) {
        sendRequest('GET', url, data, callback);
    };

    $.AdminLTE.apiPost = function (url, data, callback) {
        sendRequest('POST', url, data, callback);
    };

    $.AdminLTE.apiPatch = function (url, data, callback) {
        sendRequest('PATCH', url, data, callback);
    };

    $.AdminLTE.apiDelete = function (url, data, callback) {
        sendRequest('DELETE', url, data, callback);
    };

    $.AdminLTE.ajaxPost = function (url, data, callback) {
        sendRequest('POST', url, $.param(data), callback);
    };

}(jQuery));