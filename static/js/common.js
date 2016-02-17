
/**
 *  Notifications for user
 */
$.subscribe('alert-user', function(_, message, level, container, data) {
    var _level = '.alert',
        _container = '.notifications';
    if (level !== undefined)
        _level = _level + '-' + level;
    if (container !== undefined)
        _container = container;
    if (data !== undefined)
        console.log(data);

    $(_level, _container)
        .first()
        .show('fadeIn')
        .find('.text').text(message);
    setTimeout(function(){
        $(_level, _container)
            .first()
            .hide('fadeOut');
    }, 5000)
});

/**
 * Javascript module for common functions.
 */
(function(self, $, undefined) {

  self.show_thumbnail = function(input, image) {
    // Sets selected file of a file field as src of preview image placeholder

    if (typeof image == 'undefined') {
      image = $('#thumbnail_preview');
    }

    if ( window.FileReader ) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();
        //todo: check if its image
        reader.onload = function (e) {
          image.attr('src', e.target.result).show();
        };
        if($('.no_preview')){
          $('.no_preview').hide();
        }
        reader.readAsDataURL(input.files[0]);
      }
    }
  };

  self.hide_thumbnail = function(image) {
    // Hides preview

    if (typeof image == 'undefined') {
      image = $('#thumbnail_preview');
    }
    image.hide();
  };

  self._on_validate_error = function(){
    // Validation request replied with >=400
    console.log('validation request returned server error.');
    self.show_server_error();
  };

  self._on_upload_progress = function (e, data) {
    // Show upload progress
    var progress = parseInt(data.loaded / data.total * 100, 10);
    $('div.progress .bar').css('width', progress + '%').parent().show();
  };

  self._on_upload_error = function(e, data){
    // Upload request replied with >=400
    console.log('upload returned server error.');
    self.show_server_error();
  };

  self._on_form_error_api = function (result, textStatus, jqXHR) {
    // API form submit request replied with >=400
    $('div.progress .bar').parent().hide();
    if (!result) {
      result = jqXHR;
    }
    if (result.status === 400) { // = Validation errors
      self.display_errors($.parseJSON(result.responseText));
    }
    else{
      self.show_server_error();
    }

  };

  self.display_errors = function(errors, parent_element){
    // Django form errors: Place error message into form field's error placeholder if help-line not available

    // Use manual parent_element for placing errors (for pages with multiple identical forms)
    var parent = parent_element == undefined ? $('html') : parent_element;

    parent.find('.error', 'form').removeClass('error');
    parent.find('ul.form-error').empty().hide();
    for (field in errors){
      console.log(field + ': ' + errors[field]);
      if (field == '__all__' || field == 'non_field_errors') {
        parent.find('ul.form-error').append($('<li></li>').text(errors[field])).show();
      }
      else {
        var ele = parent.find('#id_' + field);
        if(ele.length === 0){ // for pages with multiple forms like signage playlist (need to avoid duplicate ids
          ele = parent.find("input."+field);
        }
        var error_ele = ele.closest('.controls').find('.help-inline');
        if(ele.attr('type') == 'file' || ele.is('password')){
          $('#'+ field + '-error').text(errors[field][0]).show();
        } else if( error_ele.length !== 0){
          error_ele.text(errors[field][0]);
          ele.closest('.control-group').addClass('error');
        } else {
          ele.css('border', '1px solid red')
             .attr('placeholder', errors[field][0]);
          ele.val('');
        }
      }
    }
  };

  self.show_server_error = function(text){
    // Unhides predefined server error message box for >=400 responses
    text = typeof text !== 'undefined' ? text : 'Server error, please try again later!';
    $('#server-error').text(text).show();
    $('div.progress .bar').parent().hide();
  };

  self.slide_up = function(complete){
    $('#form').closest('.widget-body').slideUp(1000, complete);
  };

  self.remove_errors = function(){
    // Remove all error messages + markings
    $('div.control-group.error').removeClass('error');
    $('ul.form-error').empty().hide();
    $("#form span.help-inline").text('');
    $('#server-error,#server-noresults').hide();
    $('#form :input[id^=id_]').not(':hidden').removeAttr('style');
    //$(':input[id^=id_]').removeAttr('style');
  };

  self.convert_to_24h = function(time_str) {
    // Convert a string like 10:05:23 PM to 24h format, returns like [22,5,23]
    var time = time_str.match(/(\d+):(\d+):(\d+) (\w)/);
    var hours = Number(time[1]);
    var minutes = Number(time[2]);
    var seconds = Number(time[3]);
    var meridian = time[4].toLowerCase();

    if (meridian == 'p' && hours < 12) {
      hours = hours + 12;
    }
    else if (meridian == 'a' && hours == 12) {
      hours = hours - 12;
    }
    return [hours, minutes, seconds];
  };

  self.get_date_time = function(date, time_str){
    // Convert a datepicker date + a 12h picker string to a datetime str as
    // django accepts it: %Y-%m-%d %H:%M:%S.
    time = self.convert_to_24h(time_str);
    date.setHours(time[0], time[1]);
    date.setSeconds(time[2]);

    var month = date.getMonth()+1 < 10 ? '0' + (date.getMonth()+1) : date.getMonth()+1;
    var day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
    var hour = date.getHours() < 10 ? '0' + date.getHours() : date.getHours();
    var minute = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes();
    var second = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds();

    date = (date.getFullYear() + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second);
    return date;
  };

  self.populate_form = function(form, data, callback){

    if (data === undefined ||
        typeof form !== 'object' )
        return false;

    form.find('input, select, textarea').each(function() {
        if (data[this.name] === undefined)
           return;

        var element = $(this),
        value = data[this.name];

        switch(true){
            case element.is('input:file'):
                $('#' + form.attr('id') + ' input[data-fileplaceholder=' + this.name + ']').val(value.split('/').pop());
                break;
            case element.hasClass('datetimepicker'):
                if (typeof element.datetimepicker === "function") {
                    element.datetimepicker({
                        dateFormat: "dd/mm/yy",
                        timeFormat: "hh:mm tt",
                        showSecond: false,
                        addSliderAccess: true,
                        sliderAccessArgs: {touchonly: true},
                        showTimezone: false
                    });
                    if(value.split(' ').length==3){ // datetime like 26/02/2015 10:00 AM
                        // This is split because chrome and firefox don't accept the same datetime format
                        var date = value.split(' ')[0];
                        var time = value.replace(date + ' ', '');
                        if(time[0]!='1'){
                            time = '0' + time;
                        }
                        element.datetimepicker('setDate', date);
                        element.datetimepicker('setTime', time);
                    }
                    else{
                        element.datetimepicker('setDate', value);
                    }
                } else {
                  element.val(value);
                }
                break;
            case element.hasClass('timepicker'):
                if (typeof element.datetimepicker === "function") {
                    element.datetimepicker({
                        timeFormat: "hh:mm tt",
                        showSecond: false,
                        addSliderAccess: true,
                        sliderAccessArgs: {touchonly: true},
                        showTimezone: false
                    });
                    element.datetimepicker('setTime', value);
                } else {
                  element.val(value);
                }
                break;
            case element.is('input:checkbox') && value === true:
                element.attr('checked', 'checked');
                break;
            default:
                element.val(value);
                break;
        }
    });

    if (callback !== undefined &&
        typeof(callback) === "function") {
      callback(data);
    }
  };

  self.clear_form = function(form){
    form.find('input, select, textarea').each(function() {
      $(this).val('');
    });
  };

  self.init_datatable = function(){
    // Make datatables (sortable/searchable/pagination etc.)
    $('table.dataTable').dataTable({
      "sDom": "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span2'i><'span8'p><'span2'>>",
      "sPaginationType": "bootstrap",
      "oLanguage": {
        "sInfo": "_START_ to _END_ of _TOTAL_ entries",
        "sSearch": "",
        "sLengthMenu": "_MENU_",
        "oPaginate": { "sPrevious": "Prev", "sNext": "Next"}
      }
    });
  };

}(window.OZCommon = window.OZCommon || {}, jQuery));


/*

$('.widget').crudify({
  'api_prefix': '/api/activities'
  'resource': 'activity'
  'template': 'test'
  'datatable' : true | false
})

crudify:
  - create (POST)
  - save (PATCH)
  - delete (DELETE)
  - confrim
  - render
  -
*/

;(function ( $, window, document, undefined ) {

    var pluginName = "Crudify",
        defaults = {
            datatable: false,
        };

    function Crudify( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options) ;
        this._defaults = defaults;
        this._name = pluginName;
        this.init();
    }

    Crudify.prototype = {

        init: function() {
            var self = this;
            $('.btn-danger', '.actions').on('click', function(e){
                e.preventDefault();
                var button = $(this);

                // Item Delete
                if (button.attr('data-pk') !== typeof undefined && button.attr('data-pk') !== undefined &&
                    button.attr('data-pk') !== false) {
                    self.confirm( function(){
                      self.delete(button.attr('data-pk'));
                    });
                }else{
                // List delete
                    // $('.checkboxes', '.table').filter('[checked="checked"]') not work when only one item listed
                    // use this plain way to get how many selected
                    var selected_count=0;
                    $('.checkboxes', '.table').each(function(){
                        var checkbox = $(this);
                        if (checkbox.attr('checked')){
                          selected_count++;
                        }
                    });

                    if (selected_count){
                        self.confirm( function(){
                          $('.checkboxes', '.table').each(function(){
                            var checkbox = $(this);
                              if (checkbox.attr('checked')){
                              self.delete(checkbox.val(), checkbox.closest('tr'));
                            }
                          });
                        });
                    }
                }
            });

            $('table').on('click', '.action > .btn-danger', function(e){
                e.preventDefault();
                var button = $(this);
                self.confirm( function(){
                    self.delete(button.attr('data-pk'), button.closest('tr'));
                });
            });
        },

        delete: function(id, element) {
            $.ajax({
                 dataType: 'json',
                 url: this.options.url + id + '/',
                 type: 'DELETE',
                 headers: { "X-CSRFToken": $.cookie('csrftoken') },
                 success: function(){
                    if (element !== undefined) {
                      element.fadeOut(1000, function(){
                        element.remove();
                      });
                    } else {
                       window.location = $('.btn-danger', '.actions').attr('href');  // return to list
                    }
                 },
                 error: function (){
                    if (element !== undefined)
                        element.addClass("error"); //TODO: make more user friendly
                    if ($('#server-error').length > 0)
                        $('#server-error').show('fadeIn');
                 }
            });
        },

        confirm: function(callback) {
            var confirm_dialog = '#' + this.options.module + 'DeleteModal';
            if ($(confirm_dialog).length > 0){
                $(confirm_dialog).modal('show');
                $('.confirm', confirm_dialog)
                  .off('click')
                  .on('click', function(){
                      $(confirm_dialog).modal('hide');
                      callback();
                  });
            } else {
                callback();
            }
        }
    };
    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName,
                new Crudify( this, options ));
            }
        });
    };

})( jQuery, window, document );

