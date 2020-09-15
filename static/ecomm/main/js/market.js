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
    $('.add_to_cart').click(function(){
        let goodsid = $(this).attr('goodsid');
        let $add = $(this)
        $.get('/shop/add_to_cart/',{'goodsid':goodsid},function(data){
            // 这里不能用$(this)，会指向当前的ajax请求，需要在上层先获取点击事件的对象
            if (data['status']==700){
                $add.prev().html(data['num']);
            }else if(data['status']==701){
                window.open('/shop/login/', target='_self');
            };
        });
    });
    $('.delete_from_cart').click(function(){
        let goodsid = $(this).attr('goodsid');
        let $delete = $(this);
        $.get('/shop/delete_from_cart/',{'goodsid':goodsid},function(data){
            // 这里不能用$(this)，会指向当前的ajax请求，需要在上层先获取点击事件的对象
            if (data['status']==700){
                $delete.next().html(data['num']);
            }else if(data['status']==701){
                window.open('/shop/login/', target='_self');
            };
        });
    });
})