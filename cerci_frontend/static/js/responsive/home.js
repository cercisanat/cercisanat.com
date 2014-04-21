$(document).ready(function(){
    var theLoc = $('div.years').position().top;
    $(window).scroll(function() {
        if(theLoc >= $(window).scrollTop()) {
            if($('div.years').hasClass('fixed')) {
                $('div.years').removeClass('fixed');
            }
        } else { 
            if(!$('div.years').hasClass('fixed')) {
                $('div.years').addClass('fixed');
            }
        }
    });
});