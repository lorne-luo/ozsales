/**
 * Javascript module for the news add/edit page.
 */
(function(self, $, undefined) {
  self.url = '/api/member/user/';
  self.avatar = undefined; // set to '' to clear on submit
  self.initialize = function() {
    /**
    * Initializes the module and everything on the page.
    */

    // For edititing existing instance, load data from the api
    var pk = $('#form').attr('data-pk');
    if (pk) {
//      $.getJSON(self.url + pk + '/', self._populate_form);
    }

    $('#form').submit(function (e) {
      e.preventDefault(); // cancels the form submission but gives us HTML5 validation
      self.save(pk);
    });

    $('button.avatar_browse').click(function(){$('#id_avatar').click();});
    $('#id_avatar').change(function(e) {
      self.avatar = e.target.files[0];
      OZCommon.show_thumbnail(this, $('#avatar_preview'));
    });

    $('button.avatar_delete').click(function(){
      // Clearing file input: http://stackoverflow.com/a/13351234/640916
      $('#id_avatar').wrap('<form>').closest('form').get(0).reset();
      $('#id_avatar').unwrap();
      self.avatar = '';
      OZCommon.hide_thumbnail($('#avatar_preview'));
    });

    $("#id_timezone").chosen({search_contains:true});
  };

  self._populate_form = function(data){
    // Populate form inputs with instance data
    var value;
    if (data !== undefined){
      $('#form').find('input, select').each(function() {
        value = data[this.name];
        if ($(this).is('input:file') && value) {
          $('#form input[data-fileplaceholder='+this.name+']').val(value.split('/').pop());
        }
        else if ($(this).is('input:checkbox')){
          if( value === true) {
            $(this).attr('checked', 'checked');
            $(this).parent().toggleButtons('setState', true);
          }
          else{// Necessary to un-check form checkboxes which are true by default
            $(this).attr('checked', '');
            $(this).parent().toggleButtons('setState', false);
          }
        }
        else if(value){
          $(this).val(value);
        }

      });

      if (data.avatar_display) {
        $('#avatar_preview').show().attr('src', data.avatar_display);
        $('button.avatar_delete').show();
      }

        // bugfix 624: the text changing should let chosen know
        $('#id_timezone').trigger("chosen:updated");
    }
  };

  self.get_form_data = function() {
    // Collect form data
    var data = new FormData();
    if($('#form').attr('data-pk')){
      data.append('pk', $('#form').attr('data-pk'));
    }
    data.append('name', $('#id_name').val());
    data.append('email', $('#id_email').val());
    data.append('mobile', $('#id_mobile').val());

    if($('#id_username').length){
      data.append('username', $('#id_username').val());
    }
    if($('#id_is_active').length){ //checkbox may not be there, depends on user privileges
      data.append('is_active', $('#id_is_active:checked').length !== 0);
    }
    if($('#id_password').length){
      data.append('password', $('#id_password').val());
    }
    if($('#id_password2').length){
      data.append('password2', $('#id_password2').val());
    }

    if ($('#id_groups').length != 0) {
      if($('#id_groups option:selected').length === 0){
          data.append('groups', ''); // direct backend to clear
      }
      else{
          $('#id_groups option:selected').each(function(){
              data.append('groups', $(this).val());
          });
      }
    }

    return data;
  };

  self.save = function(pk) {
    var url = self.url;
    var type = 'POST';
    if (pk) {
      url += pk + '/';
      type = 'PATCH';
    }

    OZCommon.remove_errors();

    $.ajax({
      dataType: 'json',
      url: url,
      type: type,
      processData: false, //needed when one uses FormData
      contentType: false,
      data: self.get_form_data(),
      headers: {
        "X-CSRFToken": $.cookie('csrftoken')
      },
      success: function(data, textStatus, xhr){
        if(xhr.status === 200){
          window.location.reload();
        }
        else if(xhr.status === 201){
          window.location = '/member/users/';
        }
        else{
          OZCommon.display_errors(data.responseText);
        }
      },
      error: OZCommon._on_form_error_api
    });
  };

}(window.OZProfileSave = window.OZProfileSave || {}, jQuery));
/**
 * On ready.
 */
$(document).ready(function() {
  OZProfileSave.initialize();
});
