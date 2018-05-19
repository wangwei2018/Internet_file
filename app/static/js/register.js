function ck_username() {
    var username = document.getElementById("username").value;
    var reg = /^[a-z][a-z0-9]{5,9}$/;
    if (username == null || username.length <= 0) {
        alert("用户名不能为空");
        return false;
    }
    else if (!reg.test(username)) {
        alert("用户名必须以小写字母开头，包含6-10位小写字母或数字");
        return false;
    }
    return true;

}

function ck_password1() {
    var password1 = document.getElementById("password").value;
    var reg = /^[a-zA-Z0-9]{8,10}$/;
    if (password1 == null || password1.length <= 0) {
        alert("密码不能为空");
        return false;
    }
    else if (!reg.test(password1)) {
        alert("密码包含8-10位字母或数字");
        return false;
    }
    return true;

}

function ck_password2() {
    var password1 = document.getElementById("password").value;
    var password2 = document.getElementById("password2").value;
    if(password2!=null&&password2.length>0&&password2==password1)
        return true;
    alert("两次密码不一致")
    return false;

}

function ck_email() {
    var email = document.getElementById("email").value;
    var reg=/^\w+@\w+\.\w+$/;
    if(email==null||email.length<=0){
        alert("邮箱不能为空");
        return false;
    }
    if(!reg.test(email)){
        alert("邮箱格式不正确");
        return false;
    }
    return true;

}

function check(){
    return ck_username()&&ck_password1()&&ck_password2()&&ck_email();
}