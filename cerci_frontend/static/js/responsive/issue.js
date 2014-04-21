$(document).ready(function(){
    $('.ellipsis').expander({
        slicePoint: 1000, 
        expandText: '<img class="more" src="' + static_url + 'images/more.png" data-toggle="tooltip" data-placement="top" title="Devamını oku"/>',
        userCollapseText: '<img class="less" src="' + static_url + 'images/less.png" data-toggle="tooltip" data-placement="top" title="Eski haline dön"/>'
    });
    $('.subject').tooltip();
    $('.issue-subject').tooltip();
    $('.more').tooltip();
    $('.less').tooltip();
    $('.files .file').tooltip();
    $('.content-body').ellipsis({row: 7});

    var onlySubjects = false;
    var $subjectContents = $('.content:not(.is-subject)');
    $('.issue-subject').click(
        function() {
            if (!onlySubjects){
                $subjectContents.hide('slow');
                onlySubjects = true;
                $('.onhover', this).html('Tümünü göster');
            }
            else {
                $subjectContents.show('slow');
                onlySubjects = false;
                $('.onhover', this).html("Yalnızca Günebakan'ları göster");
            }
        }
    );
    $('.image-files-wrapper').photobox('a.galleryitem', {counter: false});
});
