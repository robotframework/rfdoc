$(document).ready(function() {
    $('.versions-current').click(function(){
        $('#versions dl').toggle();
    });

    $('a.help').click(function(){
       $('div.help').toggle();
    });
});