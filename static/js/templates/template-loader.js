// Pre-compiles all handlebar templates it can find and registers it for quick
// access, e.g. tmpl.my_template_id(data)

(function(self){

  self.load = function() {
    $("script[type='text\/x-handlebars-template']").each(function(i, script){
      self[$(this).attr('id')] = Handlebars.compile($(this).html());
      if ($(this).is("[partial]")) {
        Handlebars.registerPartial($(this).attr('id'), $(this).html());
      }
     });
  };

}(window.OZTmpl = window.OZTmpl || {}));
