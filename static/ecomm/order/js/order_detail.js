$(function () {
    $('#alipay').click(function () {
        let $orderid = $(this).attr('orderid');
        $.getJSON('/shop/paid/',{'order_id':$orderid},function (data) {
            if(data['status']===700){
                window.open('/shop/mine/','_self');
            }
        })
    })
})