function logOut() {
    $.ajax({
        url: logOutUrl,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            window.location.href = "/login";
        },
        error: function(response) {
            alert('Çıkış işlemi sırasında bir hata oluştu.');
        }
    });
}

function logOutAdmin() {
    $.ajax({
        url: logOutAdminUrl,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            window.location.href = "/admin-login";
        },
        error: function(response) {
            alert('Çıkış işlemi sırasında bir hata oluştu.');
        }
    });
}

function adminLogin() {
    var email = $('#email').val();
    var password = $('#password').val();
    
    $.ajax({
        url: adminLoginApiUrl,
        type: 'POST',
        data: JSON.stringify({
            email: email,
            password: password
        }),
        contentType: 'application/json',
        success: function(response) {
            if (response.success) {
                window.location.href = adminHomeUrl;
            } else {
                alert(response.message);
            }
        },
        error: function(response) {
            alert('An error occurred');
        }
    });
}

function adminRegister(){
    var email = $('#email').val();
    var password = $('#password').val();
    var name = $('#name').val();
    var surname = $('#surname').val();
    
    $.ajax({
        url: adminRegisterApiUrl,
        type: 'POST',
        data: JSON.stringify({
            email: email,
            password:  password,
            name: name,
            surname: surname,
            is_admin: true
        }),
        contentType: 'application/json',
        success: function(response) {
            if (response.success) {
                window.location.href = adminHomeUrl;
            } else {
                alert(response.message);
            }
        },
        error: function(response) {
            alert('An error occurred');
        }
    });

}
function userSignUp() {    
    var email = $('#email').val();
    var password = $('#password').val();
    var name = $('#name').val();
    var surname = $('#surname').val();
    
    $.ajax({
        url: userSignUpApiUrl,
        type: 'POST',
        data: JSON.stringify({
            email: email,
            password: password,
            name: name,
            surname: surname
        }),
        contentType: 'application/json',
        success: function(response) {
            if (response.success) {
                window.location.href = userHomeUrl;
            } else {
                alert(response.message);
            }
        },
        error: function(response) {
            alert('An error occurred');
        }
    });
}


function userLogin() {    
    var email = $('#email').val();
    var password = $('#password').val();
    
    
    $.ajax({
        url: userLoginApiUrl,
        type: 'POST',
        data: JSON.stringify({
            email: email,
            password: password,
          
        }),
        contentType: 'application/json',
        success: function(response) {
            if (response.success) {
                window.location.href = userHomeUrl;
            } else {
                alert(response.message);
            }
        },
        error: function(response) {
            alert('An error occurred');
        }
    });
}
