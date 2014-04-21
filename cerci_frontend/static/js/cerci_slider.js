(function( $ ){

  $.fn.cerciSlider = function(options) {
    var self = this;
    var defaults = {
       counter: 0,
       first_issue: 0,
       last_issue: 0,
       prev: '#',
       next: '#'
    };
    var options = $.extend(defaults, options);

    var findIssue = function(issues, issue_number) {
        var our_issue;
        issues.each(function(){
            current_number = $('.number', this).attr('data-issue_id');
            if (issue_number == current_number) {
                our_issue = this;
            }
        });
        return our_issue;
    }

    var checkPosition = function(issue_number, slider) {
        if (parseInt(issue_number) >= options.last_issue) {
            $('a.next', slider).hide();
        }
        else {
            $('a.next', slider).show();
        }
        if (parseInt(issue_number) <= options.first_issue) {
            $('a.prev', slider).hide();
        }
        else {
            $('a.prev', slider).show();
        }

    }

    var process = function(){
        if ($(document).width()>979) {
            issue_number = window.location.hash.replace('#issue-', '');
            var $issues_wrapper = $('section.issues_wrapper', self);
            $issues_wrapper.hide();
            slider = $('div.cerciSlider', self);
            slider.show();
            sliderInner = $('div.inner', slider);
            var $issues = $('section.issue', $issues_wrapper.clone());
            $issues.each(function(){
                issue_id = $('.number', this).attr('id');
                $('.number', this).attr('data-issue_id', issue_id.replace('issue-', ''));
                $('.number', this).removeAttr('id');
            });
            if (!issue_number.length) {
                our_issue = $issues.get(options.counter);
                issue_number = $('.number', our_issue).attr('data-issue_id');
            }
            else {
                our_issue = findIssue($issues, issue_number);
            }
            sliderInner.html(our_issue);
            options.counter = $issues.index(our_issue);
            checkPosition(issue_number, slider);

            $('a.prev', slider).click(function(e){
                e.preventDefault();
                if (options.counter<$issues.length-1){
                    options.counter += 1;
                    $current_issue = $issues.get(options.counter);
                    issue_number = $('.number', $current_issue).attr('data-issue_id');
                    checkPosition(issue_number, slider);
                    sliderInner.html($current_issue);
                    issue_id = $('.number', $current_issue).attr('data-issue_id');
                    window.location.hash = 'issue-'+issue_id;
                }
                else {
                    $current_issue = $issues.get(options.counter);
                    issue_number = $('.number', $current_issue).attr('data-issue_id');
                    checkPosition(issue_number, slider);
                    issue_number = parseInt(issue_number)-1;
                    window.location.href = options.prev+'#issue-'+issue_number;
                }
            });

            $('a.next', slider).click(function(e){
                e.preventDefault();
                if (options.counter>0){
                    options.counter -= 1;
                    $current_issue = $issues.get(options.counter);
                    issue_number = $('.number', $current_issue).attr('data-issue_id');
                    checkPosition(issue_number, slider);
                    sliderInner.html($current_issue);
                    issue_id = $('.number', $current_issue).attr('data-issue_id');
                    window.location.hash = 'issue-'+issue_id;
                }
                else {
                    $current_issue = $issues.get(options.counter);
                    issue_number = $('.number', $current_issue).attr('data-issue_id');
                    checkPosition(issue_number, slider);
                    issue_number = parseInt(issue_number)+1;
                    window.location.href = options.next+'#issue-'+issue_number;
                }
            });
        }
        else {
            var $issues_wrapper = $('section.issues_wrapper', self);
            $issues_wrapper.show();
            slider = $('div.cerciSlider');
            slider.hide();
        }
    }

    $(window).resize(function() {
        process();
    });
    process();

  };
})( jQuery );