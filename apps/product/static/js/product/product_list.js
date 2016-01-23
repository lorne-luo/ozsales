var productListPageVue = new CommonListPageVue({
        data:{
            url:Urls['allowany-product-list']()
        }
    }
);
productListPageVue.create_url_tag = 'product-add';
productListPageVue.detail_url_tag = 'product-list-view';
productListPageVue.update_url_tag = 'product-edit';
productListPageVue.delete_url_tag = 'product-add';
