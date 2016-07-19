/**
 * Javascript module for the news add/edit page.
 */
(function(self, $, undefined) {
    self.url = '/api/member/user/';
    self.urls_to_delete = [];

    self.initialize = function() {
        self.update_event_handlers();
        $('button.delete-selected').off('click').click(self._show_delete_selected_modal);
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
    };

    self.update_event_handlers = function(){
        $('button.delete').off('click').click(self._show_delete_modal);
    };

    self._show_delete_modal = function() {
        // Event Handler: Show confirmation modal to delete
        $('#DeleteModal').modal('show');
        // Identify row and id of where button was clicked:
        var $row = $(this).closest('tr');
        var pk = $row.attr('data-pk');
        $("#DeleteModal button.confirm").off("click").click(
          self.delete_one($row, pk)
        );
      };

      self.delete_one = function($row, pk) {
        // Event handler closure: Deletes single video
        return function(event){
          $.ajax({
            dataType: 'json',
            url: '/api/member/user/' + pk + '/',
            type: 'DELETE',
            headers: {"X-CSRFToken": $.cookie('csrftoken')},
            complete: self.delete_one_callback($row)
          });
        };
      };

      self.delete_one_callback = function($row) {
        // Event handler closure: Removes table row after a delete.
        return function(xhr, textStatus){
          $('#DeleteModal').modal('hide');

          if(xhr.status >= 200 && xhr.status <= 400){
            // Get dataTable row position and delete it
            var row_position = $("table.dataTable").dataTable().fnGetPosition($row[0]);
            $("table.dataTable").dataTable().fnDeleteRow(row_position);
            self.update_event_handlers();
            return $.publish('alert-user', ['User deleted successfully.', 'success']);
          }
          else{
              return $.publish('alert-user', ['User deleting failed.', 'error']);
          }
        };
      };

    self._show_delete_selected_modal = function() {
        var users = self._selected_users();
        if (users.length == 0){
            return $.publish('alert-user', ['Please select users first.', 'error']);
        }else{
            for(var i=0; i<users.length; i++) {
                var url = self.url + users[i] + "/";
                self.urls_to_delete.push(url);
            }
        }

        $('#DeleteModal').modal('show');
        $("#DeleteModal button.confirm").off("click").click(self.delete_selected);
    };

    self.delete_selected = function() {
        if(self.urls_to_delete.length==0) {
            $('#DeleteModal').modal('hide');
        }

        for(; 0<self.urls_to_delete.length;) {
            url=self.urls_to_delete.pop();

            $.ajax({
                dataType: 'json',
                url: url,
                type: 'DELETE',
                headers: {
                  "X-CSRFToken": $.cookie('csrftoken')
                },
                complete: function(xhr, textStatus) {
                  if(xhr.status >= 200 && xhr.status <= 400){
                      //if(self.urls_to_delete.length > 0) {
                      //    return self.delete_one();
                      //}
                  }
                  else {	// there was mistake during deleting previous object, stop process
                      self.urls_to_delete = [];
                      $('#DeleteModal').modal('hide');
                      $.publish('alert-user', ['User deleting failed.', 'error']);
                  }

                  if(self.urls_to_delete.length == 0) {
                      self.delete_selected_callback(xhr, textStatus);
                  }
                }
		    });
        }

        //return self.delete_one();
    };

    self.delete_selected_callback  = function(xhr, textStatus) {
        $('#DeleteModal').modal('hide');
        if(xhr.status >= 200 && xhr.status <= 400){
          window.location = document.URL;
        }
        else{
          OZCommon.show_server_error();
            $.publish('alert-user', ['User deleting failed.', 'error']);
        }
    }

}(window.OZMemberList = window.OZMemberList || {}, jQuery));
/**
 * On ready.
 */
$(document).ready(function() {
    OZMemberList.initialize();
});
