$(document).ready(function() {
    // hide checkbox for tags
    $(".tag-filter-wrap input[type='checkbox']").hide();
    // add margin to respect disappeared checkboxes
    $(".tag-filter-wrap").css("margin-left", "20px");
    // hover event
    $(".tag-filter-wrap label").hover(function(){
        $(this).addClass("hover");
    }, function(){
        $(this).removeClass("hover");
    });
    // click event
    $(".tag-filter-wrap").click(function(){
        tag=$(this);
        label=tag.find('label');
        tag_checkbox = tag.find("input[type='checkbox']");
        if(tag_checkbox.is(':checked'))
        {
            label.removeClass("checked");
            tag_checkbox.attr('checked', false);        
        }
        else
        {
            label.addClass("checked");
            tag_checkbox.attr('checked', true);  
        }        
    });    
});