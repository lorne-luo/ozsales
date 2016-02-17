
jQuery(document).ready(function($) {
    $("select[id$='customer']").not(".empty-form select").attr('style','width:150px').chosen({search_contains: true,disable_search_threshold: 10});
	$("select[id$='address']").not(".empty-form select").attr('style','width:500px').chosen({search_contains: true,disable_search_threshold: 10});
    $("select[id$='product']").not(".empty-form select").attr('style','width:400px').chosen({search_contains: true,disable_search_threshold: 10});
    $("select[id$='store']").not(".empty-form select").attr('style','width:120px').chosen({search_contains: true,disable_search_threshold: 10});
    $("select[id$='carrier']").not(".empty-form select").attr('style','width:120px').chosen({search_contains: true,disable_search_threshold: 10});
    $("select[id$='brand']").not(".empty-form select").attr('style','width:150px').chosen({search_contains: true,disable_search_threshold: 10});
    $("select[id$='category']").not(".empty-form select").attr('style','width:300px').chosen({search_contains: true,disable_search_threshold: 10});
    $("select[id$='country']").not(".empty-form select").attr('style','width:120px').chosen({search_contains: true,disable_search_threshold: 10});

});
