$(document).ready(function() {
    // Search field blur/focus
	$("#ajax_srch_fld").focus(function(srcc) {
		if ($(this).val() == $(this)[0].title) {
		    $(this).val("");
		}});
	$("#ajax_srch_fld").blur(function() {
		if ($(this).val() == "") {
		    $(this).val($(this)[0].title);
		}});
	$("#ajax_srch_fld").blur();
  
  
  
  var text = $(".jquery-version").html();
  $(".jquery-version").html(text + " " + jqueryVersion());
  var title = $(".jquery-version").attr("title");
  $(".jquery-version").attr("title", title + " " + jqueryVersion());  

});

function jqueryVersion() {
  return $().jquery;
}