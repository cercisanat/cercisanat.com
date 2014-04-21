$(document).ready(function(){
    var ShowMenu = function(exclude) {
        $('.starter-target:not(' + exclude + ')').removeClass('active');
        $(exclude).toggleClass('active');
    }

    $('.menu-starter').click(function(){
        ShowMenu('header .primary-menu');
    });

    $('.genres-starter').click(function(){
        ShowMenu('nav.genres');
    });

    $('.search-starter').click(function(){
        ShowMenu('.form-search');
    });
});
