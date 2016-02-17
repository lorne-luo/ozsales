/**
 * Javascript module for the 'movies' page.
 */
(function(self, $, undefined) {
  self.initialize = function() {
    /**
    * Initializes the module and everything on the page.
    */
    self.update_event_handlers();
    //$.getJSON('/api/channels/channel/?limit=max',
    //  self._load_callback
    //);
  };

  //self._load_callback = function(video_list){
  //  // Receives list of channels
  //  if (video_list.results.length === 0) {
  //      $("#no_records").show();
  //      $("table.dataTable").hide();
  //      return;
  //  }
  //
  //  $(video_list.results).each(function(i, entry){
  //    var row = omniscreenTmpl.channel_table_row(entry);
  //    $('table.table-list').DataTable().row.add($(row)).draw();
  //  });
  //
  //  // Hook up new delete buttons etc.
  //  self.update_event_handlers();
  //};


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
        url: '/api/order/order/' + pk + '/',
        type: 'DELETE',
        headers: {"X-CSRFToken": $.cookie('csrftoken')},
        complete: self.delete_order_callback($row)
      });
    };
  };

  self.delete_order_callback = function($row) {
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

}(window.OZOrderList = window.OZOrderList || {}, jQuery));
/**
 * On ready.
 */
$(document).ready(function() {
  OZOrderList.initialize();
});
