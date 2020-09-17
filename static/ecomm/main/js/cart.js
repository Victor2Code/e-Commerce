$(function () {
    let $confirm = $('.confirm');
    $confirm.click(function () {
        let $div = $(this);
        let cartid = $(this).parents('.menuList').attr('cartid');
        $.get('/shop/change_select_state/', {'cartid': cartid}, function (data) {
            console.log(data);
            let $span = $div.children('span').children('span');
            if(data['is_all_select']){
                $('.all_select').children('span').children('span').html('√')
            }else{
                $('.all_select').children('span').children('span').html('')
            }
            if (data['is_selected']) {
                $span.html('√');
            } else {
                $span.html('');
            }
            $('#total_price').html(data['total_price']);
        })
    });
    $('.delete_in_cart').click(function () {
        let cartid = $(this).parents('.menuList').attr('cartid');
        let $span = $(this).next();
        $.get('/shop/delete_in_cart/', {'cartid': cartid}, function (data) {
            // console.log(data);
            if (data['num'] == 0) {
                $span.parents('li').remove();
            } else {
                $span.html(data['num']);
            }
            $('#total_price').html(data['total_price']);
        });
    });
    $('.add_in_cart').click(function () {
        let cartid = $(this).parents('.menuList').attr('cartid');
        let $span = $(this).prev();
        $.get('/shop/add_in_cart/', {'cartid': cartid}, function (data) {
            console.log(data);
            $span.html(data['num']);
            $('#total_price').html(data['total_price']);
        });
    });
    $('.all_select').click(function () {
        let value = $(this).children('span').children('span').html();
        let $all_select = $(this);
        if (value) {
            $.get('/shop/cart_all_unselect/', {}, function (data) {
                if (data['status'] == 700) {
                    $('.confirm').each(function () {
                            $(this).children('span').children('span').html('');
                            $all_select.children('span').children('span').html('');
                        }
                    )
                }
            })
        } else {
            $.get('/shop/cart_all_select/',{},function (data) {
                if (data['status'] == 700) {
                    $('.confirm').each(function () {
                            $(this).children('span').children('span').html('√');
                            $all_select.children('span').children('span').html('√');
                        }
                    )
                }
            })
        }
    })
});