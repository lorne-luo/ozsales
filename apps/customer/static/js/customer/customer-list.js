(function(self, $, undefined) {
  self.initialize = function() {
    /**
    * Initializes the module and everything on the page.
    */
    self.update_event_handlers();
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
      self.delete($row, pk)
    );
  };

  self.delete = function($row, pk) {
    // Event handler closure: Deletes single video
    return function(event){
      $.ajax({
        dataType: 'json',
        url: '/api/customer/customer/' + pk + '/',
        type: 'DELETE',
        headers: {"X-CSRFToken": $.cookie('csrftoken')},
        complete: self.delete_customer_callback($row)
      });
    };
  };

  self.delete_customer_callback = function($row) {
    // Event handler closure: Removes table row after a delete.
    return function(xhr, textStatus){
      $('#DeleteModal').modal('hide');

      if(xhr.status >= 200 && xhr.status <= 400){
        // Get dataTable row position and delete it
        var row_position = $("table.dataTable").dataTable().fnGetPosition($row[0]);
        $("table.dataTable").dataTable().fnDeleteRow(row_position);
        self.update_event_handlers();
      }
      else{
        OZCommon.show_server_error();
      }
    };
  };

}(window.OZCustomerList = window.OZCustomerList || {}, jQuery));
/**
 * On ready.
 */
$(document).ready(function() {
  OZCustomerList.initialize();
});
