$(function () {
    $('#regis').click(function () {
        window.open('/shop/register/','_self');
    });
    $('#not_login').click(function () {
        window.open('/shop/login/','_self');
    });
    $('#order_not_pay').click(function () {
        window.open('/shop/orderlist_not_pay/','_self');
    })
})