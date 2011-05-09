(function($)  {

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
      }
    }
  });
  
  css_default_settings = {
    /* common used */
    ajaxWaitPictureClass: "ajax_loader",
    ajaxWaitPictureSource: "/media/img/ajax-loader.gif",
    inputErrorClass:"js_input-error",
    inputValidClass:"jq_input-valid",
    loginId:"login",
    logoutId:"logout",
    logoutURL:"",
    logoutValue:"Выйти",
    signupId: "signup",
    editProfileId: "edit_profile",
    editProfileURL: "",
    editProfileValue: "Редактировать профиль",
    editProfileMessageClass: "ajax_user_message",
    messageErrorClass: "js_errorlist",
    messageSuccess: "Спасибо, вы зарегистрированы",
    messageSuccessFunction: null,
    formPrefix: "",
    hideElemsOnSuccess: "",

    /* pwd validate only used */
    messageDiffers: "Два поля с паролями не совпадают",
    messageEmpty: "Обязательное поле",

    /* get_form only used */
    validateURL: "",
    ajaxWaitFormReceivedPictureSource: "/media/img/ajax-loader-big.gif",
    closePictureSource: "/media/img/close.png",
    backgroundClass: "ajax_background",
    formId: "signup_form",
    formClass: "auth_from_small",
    formWrapInputClass: "auth-field",
    submitClass: "submit_btn",
    submitId: "btSignin",
    submitValue: "Зарегистрироваться &raquo",
    messageSuccessClass: "ajax_success_message"
  }
  /************************************************/
  /***      VALIDATE FIELDS (server access)     ***/
  /************************************************/
  $.fn.validate = function(url, settings, css) {
    settings = $.extend({
      callback: false,
      fields: false,
      dom: this,
      event: 'submit',
      saveOnSubmit: true,
      dataSource: 'signup'
    }, settings);
    css = $.extend({}, css_default_settings, css);

    return this.each(function() {
      var form = $(this);
      big_handler = function()  {
        var params = {};
        if(settings.event!='submit'){
          var wasSubmit=false;
          small_handler = function() {wasSubmit=true;return false;}
          form.unbind('submit', big_handler).bind('submit', small_handler);
          //disable 'change' event in case 'submit' event
          setTimeout(function() {
            form.unbind('submit', small_handler).bind('submit', big_handler);
            if (!wasSubmit){
              // only change event has been raised
              status = ajax_validate(url, form, settings, css, params);
            }else{
              form.submit();
            }
          }, 100);
        }else{
          // submit event handler
          status = ajax_validate(url, form, settings, css, params);
        }
        return false;
      }
      settings.dom.bind(settings.event, big_handler);
    });
    function ajax_validate(url, form, settings, css, params){
      form_data(form).each(function() {
        params[ this.name || this.id || this.parentNode.name || this.parentNode.id ] = this.value;
      });
      var status = false;
      var send_ajax = true;
      var elemWrap;
      if (settings.dom.is('form')){
        elemWrap=settings.dom;
      }else{
        elemWrap=settings.dom.parent();
      }
      if (settings.fields) {
        params.fields = settings.fields;
      }
      if (settings.dom.is(":input")){
        elemWrap.find("."+css.messageErrorClass).remove();
        settings.dom.after('<img class="' + css.ajaxWaitPictureClass + '" src="'+css.ajaxWaitPictureSource+'" />');
      }else{
        if(settings.dom.find("input:password").hasClass(css.inputErrorClass)){
          send_ajax=false;
        }else{
          elemWrap.find("."+css.messageErrorClass).remove();
          elemWrap.find("input:submit").after('<img class="' + css.ajaxWaitPictureClass + '" src="'+css.ajaxWaitPictureSource+'" />');
        }
      }
      if (settings.event=='submit' && settings.saveOnSubmit){
        params.save = true;
      }
      params.formPrefix = css.formPrefix;
      if(send_ajax){
        $.ajax({
          async: true,
          data: params,
          traditional: true,
          dataType: 'json',
          error: function(XHR, textStatus, errorThrown)   {
            status = true;
          },
          success: function(data, textStatus) {
            $("." + css.ajaxWaitPictureClass).remove();
            status = data.valid;
            if (!status){
              if (settings.callback)  {
                settings.callback(data, form);
              }else{
                elemWrap.find('input:not(:submit)').removeClass(css.inputErrorClass).addClass(css.inputValidClass);
                $.each(data.errors, function(key, val)  {
                  if(key=="__all__" && settings.dataSource=='login'){
                    show_message(form, css, val);
                  }else{
                    if (settings.dataSource=='edit_profile'){
                      $('.'+css.editProfileMessageClass).slideUp('slow');
                    }
                    $('#' + key).removeClass(css.inputValidClass).addClass(css.inputErrorClass);
                    $('#' + key).after('<ul class="'+ css.messageErrorClass + '"><li>' + val + '</li></ul>');
                  }
                });
              }
            }else{
              $("."+css.messageErrorClass).remove();
              settings.dom.removeClass(css.inputErrorClass);
              elemWrap.find('input:not(:submit)').addClass(css.inputValidClass).removeClass(css.inputErrorClass);
            }
            if (status && params.save){
              perform_success_action(form, css, settings.dataSource);
            }
            return status;
          },
          type: 'POST',
          url: url
        });
      }
    }

    function form_data(form)   {
      return form.find("input[checked], input[type='text'], input[type='hidden'], input[type='password'], option[selected], textarea");
    }

    function perform_success_action(form, css, dataSource){
      if (css.hideElemsOnSuccess != "")
      {
        css.hideElemsOnSuccess.hide();
      }
      if (dataSource=='signup' || dataSource=='login'){
        if (dataSource=='login'){
          $('.'+css.editProfileMessageClass).remove();
          css.messageSuccess = css.messageSuccess.replace("%username%", form.find("#id_username").val());
        }
        logout_button = $('#'+css.loginId);
        logout_button.slideUp('slow', function(){
          logout_button.find('a').html(css.logoutValue).attr('href', css.logoutURL);
          logout_button.attr('id', css.logoutId);
          logout_button.slideDown()
        });
        editProfile_button = $('#'+css.signupId);
        editProfile_button.slideUp('slow', function(){
          editProfile_button.find('a').html(css.editProfileValue).attr('href', css.editProfileURL);
          editProfile_button.attr('id', css.editProfileId);
          editProfile_button.slideDown('slow')
        });
        if (css.messageSuccessFunction == null){
          form.before("<div>"+css.messageSuccess+"</div>");
        }else{
          css.messageSuccessFunction();
        }
        form.remove();
      }
      else if(dataSource=='edit_profile'){
        show_message(form, css, css.messageSuccess);
      }
    }
    function show_message(form, css, message){
      form.find('input').removeClass(css.inputValidClass).removeClass(css.inputErrorClass);
      ajax_user_message = $('.'+css.editProfileMessageClass);
      if (ajax_user_message.length!=0){
        if(ajax_user_message.is(":hidden")){
          ajax_user_message.slideDown('slow');
        }else{
          message_content = ajax_user_message.find('ul');
          message_content.slideUp('slow', function(){
            message_content.html('<li>'+message+'</li>').slideDown('slow');
          });
        }
      }
      else
      {
        var ajax_user_message;
        if (form.children(":first").find('input').length==0 || form.children(":first").is("not(:input)")){
          // there is some header in form
          first_not_input = form.children().filter(function(){
            return $(this).is(":input") || $(this).find("input").length != 0;
          }).eq(0);
          ajax_user_message = first_not_input.before("<div></div>").prev();
        }else{
          // no header in form, input fields starts immediately
           ajax_user_message= form.prepend("<div></div>").children(":first");
        }


        ajax_user_message.hide();
        ajax_user_message.attr('class', css.editProfileMessageClass).html('<ul><li>'+message+'</li></ul>');
        ajax_user_message.slideDown();
      }
    }
  };
  /************************************************/
  /***      VALIDATE PASSWORD                   ***/
  /************************************************/
  $.fn.pwd_validate = function(css) {
    css = $.extend({}, css_default_settings, css);

    function make_invalid(errMessage){
      html_errMessage = '<ul class="'+ css.messageErrorClass + '"><li>' + errMessage + '</li></ul>'
      this.addClass(css.inputErrorClass).removeClass(css.inputValidClass).next('ul').remove().end().after(html_errMessage);
    }
    function make_valid(){
      this.addClass(css.inputValidClass).removeClass(css.inputErrorClass).next('ul').remove();
    }
    function reset_style(){
      this.removeClass(css.inputErrorClass).removeClass(css.inputValidClass).next('ul').remove();
    }
    return this.each(function() {
      var form = $(this);
      password1 = form.find("input:password:eq(0)");
      password2 = form.find("input:password:eq(1)");
      password1.modified=false;
      password2.modified=false;

      password1.make_invalid = make_invalid;
      password1.make_valid = make_valid;
      password1.reset_style = reset_style;
      password2.make_invalid = make_invalid;
      password2.make_valid = make_valid;
      password2.reset_style = reset_style;

      password1.keyup(function(){
        if (password1.val() != ""){
          password1.reset_style();
        }
        else if(password1.modified){
          password1.make_invalid(css.messageEmpty);
        }
        if(password2.modified){
          password1.make_valid();
          password2.make_valid();
          if(password1.val() != password2.val())
          {
            password2.make_invalid(css.messageDiffers);
            if(password1.val()==""){
              password1.make_invalid(css.messageEmpty);
            }
          }
          else if(password1.val() == ""){
            password1.make_invalid(css.messageEmpty);
            password2.reset_style();
          }
        }
        password1.modified=true;
      });
      password2.keyup(function(){
        if(password2.modified || (password2.hasClass(css.inputErrorClass) && (password2.val()!=""))){
          password2.modified = true;
          password2.make_valid();
          password1.make_valid();
          if(password1.val() != password2.val()){
            password2.make_invalid(css.messageDiffers);
            if(password1.val()==""){
              password1.make_invalid(css.messageEmpty);
            }
          }
          else if(password1.val() == ""){
            password1.make_invalid(css.messageEmpty);
            password2.removeClass(css.inputValidClass);
          }
        }
      });

      password1.change(function(){
        if (password1.val() != ""){
          password1.make_valid();
        }else{
          password1.reset_style();
        }
        password1.modified=true;
      });
      password2.change(function(){
        password2.modified = true;
        password2.make_valid();
        if($(this).val() != password1.val()){
          password2.make_invalid(css.messageDiffers);
        }
      });
    });
  };
  /************************************************/
  /***      GET FORM (server access)            ***/
  /************************************************/
  $.fn.get_form_onclick = function(url, settings, css){
    settings = $.extend({
      dataSource: 'signup'
    }, settings);

    css = $.extend({}, css_default_settings, css);

    return this.each(function() {
      this_elem = $(this)
      this_elem.click(function(){
        /* if form already exists, nothing to do */
        if ($("#"+css.formId).length == 0){
          background = $("<div></div>").appendTo('body').addClass(css.backgroundClass);
          background.css("width", $(document).width() + "px");
          background.css("height", $(document).height() + "px");
          ajax_recieve_loader = $('<img src="'+css.ajaxWaitFormReceivedPictureSource+'" />').appendTo('body').center();
          /* send ajax request */
          $.ajax({
            async: true,
            data: {},
            traditional: true,
            dataType: 'json',
            error: function(XHR, textStatus, errorThrown)   {
              status = true;
            },
            success: function(data, textStatus) {
              ajax_recieve_loader.remove();
              remove_ajax_signup = function(){
                background.remove();
                $("."+css.formClass).remove();
              }
              background.one("click", remove_ajax_signup);

              new_form = $("<form></form>").appendTo('body');
              new_form.addClass(css.formClass);
              new_form.attr("action", css.validateURL);
              new_form.attr("method", "post");
              new_form.attr("id", css.formId);
              new_form.html(data.form);
              new_form.find("div").addClass(css.formWrapInputClass);
              new_form.append('<div class="'+css.submitClass+'"><input type="submit" id="'+css.submitId+'" value="'+css.submitValue+'" /></div>');

              exit_button_wrap = $('<div><img src="'+css.closePictureSource+'" /></div>').prependTo(new_form);
              exit_button_wrap.css('width', '100%').css("text-align", "right").css("background", "#F3F3F3");
              exit_button = exit_button_wrap.find('img');
              exit_button.css("cursor", "pointer").css("padding-top", "2px").css("padding-right", "5px");
              exit_button.one("click", remove_ajax_signup);
              new_form.center();

              css.hideElemsOnSuccess = css.hideElemsOnSuccess.add(new_form);
              css.messageSuccessFunction = function (){
                if(settings.dataSource=='login'){
                  css.messageSuccess = css.messageSuccess.replace("%username%", new_form.find('#id_'+formPrefix+'username').val());
                }
                messageSuccess = $("<div>"+css.messageSuccess+"</div>").appendTo('body').addClass(css.messageSuccessClass).center();
                setTimeout(function() {
                  messageSuccess.remove();
                  background.remove();
                }, 1500);
              };
              var formPrefix;
              if (css.formPrefix==""){
                formPrefix=""
              }else{
                formPrefix=css.formPrefix+"-";
              }
              if(settings.dataSource=='login'){
                new_form.validate(css.validateURL, {fields: ['username', 'password'], dataSource: settings.dataSource}, css);
              }else if(settings.dataSource=='signup'){
                new_form.validate(css.validateURL, {fields: ['username'], dom: $('#id_'+formPrefix+'username'), event: 'change'}, css);
                new_form.validate(css.validateURL, {fields: ['email'], dom: $('#id_'+formPrefix+'email'), event: 'change'}, css);
                new_form.validate(css.validateURL, {fields: ['username', 'password1', 'password2', 'email']}, css);
                new_form.pwd_validate(css);
              }
              $('#id_'+formPrefix+'username').focus();
            },
            type: 'POST',
            url: url
          });
        }
        return false;
      });
    });
  };

  /************************************************/
  /***                MISC                      ***/
  /************************************************/
  jQuery.fn.center = function () {
    this.css("position","absolute");
    this.css("top", ( $(window).height() - this.height() ) / 2+$(window).scrollTop() + "px");
    this.css("left", ( $(window).width() - this.width() ) / 2+$(window).scrollLeft() + "px");
    return this;
  }
})(jQuery);