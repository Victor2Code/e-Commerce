$(function(){
    $('#all_types').click(function(){
        // console.log('test!!')
        // $all_types_container=$("#all_types_container").css({'display':'block'})
        $("#all_types_container").toggle();
        $("#type_icon").toggleClass('glyphicon-chevron-down').toggleClass('glyphicon-chevron-up')
    });
    $('#all_types_container').click(function(){
        $(this).toggle();
        $("#type_icon").toggleClass('glyphicon-chevron-down').toggleClass('glyphicon-chevron-up');
    });
    $('#sort_methods').click(function () {
        $('#sort_methods_container').toggle()
    })
})