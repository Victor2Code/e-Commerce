$(function(){
    $('#all_types').click(function(){
        // console.log('test!!')
        // $all_types_container=$("#all_types_container").css({'display':'block'})
        $all_types_container=$("#all_types_container").toggle()
    });
    $('#sort_methods').click(function () {
        $('#sort_methods_container').toggle()
    })
})