
jQuery(document).ready(function($) {
    $("select[multiple]").css("width", '300px').attr('data-placeholder', '多选').chosen();
    $("select[id$='customer']").attr('style','width:150px').chosen();
	$("select[id$='address']").attr('style','width:500px').chosen();
    $("select[id$='product']").attr('style','width:400px').chosen();
    $("select[id$='store']").attr('style','width:120px').chosen();
    $("select[id$='carrier']").attr('style','width:120px').chosen();
    $("select[id$='brand']").attr('style','width:150px').chosen();
    $("select[id$='category']").attr('style','width:200px').chosen();
    $("select[id$='country']").attr('style','width:120px').chosen();

});
