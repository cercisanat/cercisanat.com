$(document).ready(function(){
    var url = window.location.href.replace(window.location.hash, '');
    $('ul.auto-active a[href="'+ url +'"]').parent().addClass('active');
    $('ul.auto-active a').filter(function() {
      return this.href == url;
    }).parent().addClass('active');
  
    $(".carousel").swiperight(function() {  
      $(this).carousel('prev');  
      });  
    $(".carousel").swipeleft(function() {  
      $(this).carousel('next');  
    });
    if($(document).width() < 768) {
      var bg_src = 'src-mobile';
    }
    else {
      var bg_src = 'src';
    }
    $('.issuecontent-bg').each(function(){
      $(this).attr('src', $(this).data(bg_src));
    });
    $('.author-bg').each(function(){
      $(this).attr('src', $(this).data(bg_src));
    });


    var subscription_form = $('.subscription-form');
    $('.more').tooltip();
    $('.less').tooltip();
    $('.genres li a.genre').tooltip();
    $('.carousel').carousel('pause');
    if ($.cookie('subscribed_to_newsletters')) {
        $('.subscribe-form').hide();
        $('.subscribe-success', subscription_form).show();
    }
    else {
        $('.subscribe-form').show();
        $('.subscribe-success', subscription_form).hide();
    }

    $('.subscribe-form').validate({
        type: 'bootstrap',
        fields: ['id_email', 'id_name'],
        event: 'focusout',
        fieldSuccessCallback: function(field) {
            field.closest('.controls').addClass('ok');
        },
        formSuccessCallback: function(form) {
            $.cookie("subscribed_to_newsletters", 1, { expires : 999999 });
            form.hide();
            $('.subscribe-success', subscription_form).show();
        }
    });

    $('.another-subscription').on('click', function(e){
        $.removeCookie('subscribed_to_newsletters', { expires : 999999 });
        $('.subscribe-success', subscription_form).hide();
        $('.subscribe-form').show();
        $('#id_email').val('');
        $('#id_email').closest('.controls').removeClass('ok');
        $('#id_email').closest('.controls').removeClass('error');
        $('#id_name').val('');
        $('#id_name').closest('.controls').removeClass('ok');
        $('#id_name').closest('.controls').removeClass('error');
        e.preventDefault();
    });

});
