jQuery.fn.dataTableExt.aTypes.push(
  function ( sData ){
    var sValidStrings = 'monday,tuesday,wednesday,thursday,friday,saturday,sunday';

    if (sValidStrings.indexOf(sData.toLowerCase()) >= 0){
      return 'weekdays-sort';
    }

    return null;
  }
);

var weekdays = new Array();
weekdays['monday'] = 1;
weekdays['tuesday'] = 2;
weekdays['wednesday'] = 3;
weekdays['thursday'] = 4;
weekdays['friday'] = 5;
weekdays['saturday'] = 6;
weekdays['sunday'] = 7;

jQuery.fn.dataTableExt.oSort['weekdays-sort-asc']  = function(a,b) {
    a = a.toLowerCase();
    b = b.toLowerCase();
    return ((weekdays[a] < weekdays[b]) ? -1 : ((weekdays[a] > weekdays[b]) ?  1 : 0));
};

jQuery.fn.dataTableExt.oSort['weekdays-sort-desc'] = function(a,b) {
    a = a.toLowerCase();
    b = b.toLowerCase();
    return ((weekdays[a] < weekdays[b]) ? 1 : ((weekdays[a] > weekdays[b]) ?  -1 : 0));
};