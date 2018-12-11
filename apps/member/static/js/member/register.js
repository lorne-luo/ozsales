var retryText = ' 秒后重试';
var retrySeconds = 60;
/**
 * On ready.
 */
$(document).ready(function () {
    $("#send_code").click(function () {
        var mobile = $("#id_mobile").val();
        if (!mobile) {
            return;
        }

        var self = this;
        $.ajax({
            method: "POST",
            url: "/api/member/register/verification_code/",
            data: {mobile: mobile}
        })
            .done(function (msg) {
                if (msg.success) {
                    $('#error-alert-div').hide();

                    $(self).attr("disabled", "disabled");
                    $(self).text(retrySeconds + retryText);

                    var timer = setInterval(function () {
                        var seconds = parseInt($(self).text()) - 1;
                        if (seconds === 0) {
                            $(self).text("重发验证码");
                            $(self).prop('disabled', false);
                            clearInterval(timer);
                            return;
                        }
                        $(self).text(seconds + retryText);
                    }, 1000);
                } else {
                    $('#error-alert-div').show();
                    $('#error-msg').text(msg.detail);
                }
            });
    });
});
