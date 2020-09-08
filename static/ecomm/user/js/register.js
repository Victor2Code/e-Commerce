$(function () {
    //用户名校验
    $('#username').change(function () {
        let username = $(this).val().trim();
        if (username.length) {
            $.getJSON('/shop/checkuser/', {'username': username}, function (data) {
                // console.log(data);
                $('#register_container').find('span[id="username_alert"]').html(data['message']);
                // $('#username_alert').html(data['message']);
                if (data['status']==900){
                    $('#username_alert').css('color','red');
                }else if(data['status']==901){
                    $('#username_alert').css('color','green');
                }
            });

        };
    });

// 密码一致性校验
    $('#password_check').change(function(){
        let password1 = $('#password').val().trim();
        let password2 = $(this).val().trim();
        if (password1==password2){
            $('#password_check_alert').addClass('glyphicon glyphicon-ok').removeClass('glyphicon-remove').css('color','green').html('密码一致')
        }else{
            $('#password_check_alert').removeClass('glyphicon-ok').addClass('glyphicon glyphicon-remove').css('color','red').html('密码不一致')
        }
    })

//  邮箱校验
$('#email').change(function(){
    let email=$(this).val().trim();
    if(email.length){
        $.getJSON('/shop/checkemail/',{'email':email},function(data){
            $('#email_alert').html(data['message']);
            if (data['status']==900){
                    $('#email_alert').css('color','red');
                }else if(data['status']==901){
                    $('#email_alert').css('color','green');
                }
        });
    };
});



}); //不加分号下方的函数无法被识别

// 提交表单的时候检测3个span是否为红色
function check(){
    let username_alert=$('#username_alert').css('color');
    let email_alert = $('#email_alert').css('color');
    let password_check_alert = $('#password_check_alert').css('color');
    console.log(username_alert);
    console.log(username_alert=='rgb(255, 0, 0)') //中间有空格，最好是复制console中打印的内容
    if (username_alert == 'rgb(255, 0, 0)' || email_alert == 'rgb(255, 0, 0)' || password_check_alert =='rgb(255, 0, 0)'){
        alert('请检查标红的输入');
        return false;
    }else {
        return true;
    }
}