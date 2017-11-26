
$(document).ready(function () {
    $('input').iCheck({
        checkboxClass: 'icheckbox_square-blue',
        radioClass: 'iradio_square-blue',
        increaseArea: '20%' // optional
    });

    $("#address-text").text($("#id_address option:selected").text());
    $("#id_address").change(function () {
        $("#address-text").text($("option:selected", this).text());
    });
});