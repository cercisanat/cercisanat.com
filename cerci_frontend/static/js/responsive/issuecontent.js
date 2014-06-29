$(document).ready(
function(){
    $('a.tooltipped', tocContainer).tooltip();
    
    $('figure').photobox('a.galleryitem', {counter: false});
    $('.photobox-gallery').photobox('a.galleryitem', {counter: false});

    var tocStarter = $('div.toc-container a.toc-starter');
    var tocContainer = $('div.toc-container');
    if (tocContainer.get(0) !== undefined) {
      tocContainer.css('max-height', ($(window).height() -10 )+'px');
      $(window).resize(function() {
          tocContainer.css('max-height', ($(window).height() -10 )+'px');
      });
      tocStarter.click(function(e) {
          e.preventDefault();
          $('nav.toc').toggle('slow');
      });
      var theLoc = tocContainer.position().top;
      $(window).scroll(function() {
          if(theLoc +100 >= $(window).scrollTop()) {
              if(tocContainer.hasClass('fixed')) {
                  tocContainer.removeClass('fixed');
              }
          } else { 
              if(!tocContainer.hasClass('fixed')) {
                  tocContainer.addClass('fixed');
              }
          }
      });
    }
    
});
