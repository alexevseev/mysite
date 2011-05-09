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
    });