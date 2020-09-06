$(function(){
    function typeToggle(){
        $("#all_types_container").toggle();
        $("#type_icon").toggleClass('glyphicon-chevron-down').toggleClass('glyphicon-chevron-up');
    };
    function typeHide(){
        $("#all_types_container").hide();
        $("#type_icon").removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    };
    function sortToggle(){
        $('#sort_methods_container').toggle();
        $("#sort_icon").toggleClass('glyphicon-chevron-down').toggleClass('glyphicon-chevron-up');
    };
    function sortHide(){
        $('#sort_methods_container').hide();
        $("#sort_icon").addClass('glyphicon-chevron-down').removeClass('glyphicon-chevron-up');
    };
    $('#all_types').click(function(){
        // console.log('test!!')
        // $all_types_container=$("#all_types_container").css({'display':'block'}
        sortHide();
        typeToggle();
    });
    $('#all_types_container').click(function(){
        typeToggle();
    });
    $('#sort_methods').click(function () {
        typeHide();
        sortToggle();
    });
    $('#sort_methods_container').click(function(){
        sortToggle();
    });
})