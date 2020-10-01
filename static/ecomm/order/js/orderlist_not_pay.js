$(function () {
    $('.order').click(function () {
        let $order=$(this);
        let $orderid = $order.attr('orderid');
        window.open('/shop/orderdetails/?order_id='+$orderid,'_self');
    })
})