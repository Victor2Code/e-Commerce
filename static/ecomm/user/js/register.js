$(function () {
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
        password1 = $('#password').val().trim();
        password2 = $(this).val().trim();
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

})