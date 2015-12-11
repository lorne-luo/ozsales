/**
 * Javascript module for the categories setup
 */
(function(self, $, undefined) {
  self.url = '/api/channels/channel/';
  self.logo = undefined;

  self.initialize = function() {
    /**
    * Initializes the module and everything on the page.
    */

    $('button.delete').click(self._show_delete_modal);

    $('#form').submit(function (e) {
      e.preventDefault(); // cancels the form submission but gives us HTML5 validation
      self.save();
    });

    self.pk = $('#form').attr('data-pk');
    if (self.pk) {
      self.url = self.url + self.pk + '/';
      $.getJSON(self.url, function(data){
        OZCommon.populate_form($('form'), data, function(data){
            // $('#id_star_rating').rating();
            // $("#id_advisories").chosen({search_contains:true});
            if (data.logo_display) {
              $('#thumbnail_preview').show().attr('src', data.logo_display);
            }
            $("#id_categories").chosen({search_contains:true});
            $('div.service_active').toggleButtons('setState', data.service_active);
            $("#id_is_hidden").prop( "checked", data.is_hidden );
        });
      });
    }
    else{
      // Set service to active by default
      $('div.service_active').toggleButtons('setState', true);
    }

    $('a.logo_browse').click(function(){$('#id_logo').click();});
    $('#id_logo').change(function(e) {
      // Writes file name into dummy input on file-select
      $('#id_logo_dummy').val($(this).val());
      OZCommon.show_thumbnail(this);
      self.logo = e.target.files[0];
    });


  };


  self.save = function(){
    var data = new FormData();

    data.append('name', $('#id_name').val());
    data.append('number', $('#id_number').val());
    data.append('service_active', $('#id_service_active').is(":checked"));
    data.append('is_hidden', $('#id_is_hidden').is(":checked"));

    if ($('#id_categories').length != 0) {
      if($('#id_categories option:selected').length === 0){
          data.append('categories', ''); // direct backend to clear
      }
      else{
          $('#id_categories option:selected').each(function(){
              data.append('categories', $(this).val());
          });
      }
    }

    if (self.logo) {
      data.append('logo', self.logo);
    }

    $.ajax({
      dataType: 'json',
      headers: {
        "X-CSRFToken": $.cookie('csrftoken')
      },
      url: self.url,
      type: self.pk ? 'PATCH' : 'POST',
      processData: false, //needed when one uses FormData
      contentType: false,
      data: data,
      success: function(data){
        window.location = '/admin/channels/';
      },
      error: OZCommon._on_form_error_api
    });

  };


  self._show_delete_modal = function() {
    // Event Handler: Show confirmation modal before delete
    $('#DeleteModal').modal('show');
    $("#DeleteModal button.confirm").off("click").click(
      self.delete_channel()
    );
  };

  self.delete_channel = function() {
    // Event handler closure: Deletes current channel
    return function(event){
      $.ajax({
        dataType: 'json',
        url: self.url,
        type: 'DELETE',
        headers: {
          "X-CSRFToken": $.cookie('csrftoken')
        },
        complete: self.delete_channel_callback()
      });
    };
  };

  self.delete_channel_callback  = function() {
    // Event handler closure: Removes table row
    return function(xhr, textStatus){
      $('#DeleteModal').modal('hide');

      if(xhr.status >= 200 && xhr.status <= 400){
        window.location = '/admin/channels/';
      }
      else{
        OZCommon.show_server_error();
      }
    };
  };

}(window.OZOrderEdit = window.OZOrderEdit || {}, jQuery));
/**
 * On ready.
 */
$(document).ready(function() {
  OZOrderEdit.initialize();
});
