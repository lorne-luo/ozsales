
jQuery(document).ready(function($) {
    $("select[id$='customer']").not(".empty-form select").attr('style','width:150px').chosen();
	$("select[id$='address']").not(".empty-form select").attr('style','width:500px').chosen();
    $("select[id$='product']").not(".empty-form select").attr('style','width:400px').chosen();
    $("select[id$='store']").not(".empty-form select").attr('style','width:120px').chosen();
    $("select[id$='carrier']").not(".empty-form select").attr('style','width:120px').chosen();
    $("select[id$='brand']").not(".empty-form select").attr('style','width:150px').chosen();
    $("select[id$='category']").not(".empty-form select").attr('style','width:300px').chosen();
    $("select[id$='country']").not(".empty-form select").attr('style','width:120px').chosen();

});
