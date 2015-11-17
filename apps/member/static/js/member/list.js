/**
 * Javascript module for the news add/edit page.
 */
(function(self, $, undefined) {
    self.url = '/api/member/user/';
    self.users = [];

    self.initialize = function(purchase) {
        self.purchase = purchase;

        $('#AddPackage').click(function(e){
            e.preventDefault();
            var users = self._selected_users();
            if (users.length === 0){
                return $.publish('alert-user', ['Please select users first.', 'error']);
            }
            $('#AddPackageModal').trigger('click');
            self.purchase.setUsers(users);
            omniscreenChannelPackage.initialize(self.purchase);
        });
    };

    self._selected_users = function(){
        var users = [];
        $('.checkboxes', 'table.user-list').each(function(){
            if($(this).is(':checked')){
                var user_id = Number($(this).val());
                users.push(user_id);
            }
        });
        return users;
    }

}(window.omniscreenAccountList = window.omniscreenAccountList || {}, jQuery));
/**
 * On ready.
 */
$(document).ready(function() {
    omniscreenAccountList.initialize(opPurchase);
});
