(function () {
    var accessTokenCookie = document.cookie;
    var accessToken = accessTokenCookie.substr(13,accessTokenCookie.length);
//        alert(accessToken);
    var userInfoSource = document.getElementById('userInfoTemplate').innerHTML,
        userInfoTemplate = Handlebars.compile(userInfoSource),
        userInfoPlaceholder = document.getElementById('userInfo');
    if (accessToken){
        $.ajax({
            url: 'https://api.spotify.com/v1/me',
            headers: {
                'Authorization': 'Bearer ' + accessToken
            },
            success: function (response) {
                userInfoPlaceholder.innerHTML = userInfoTemplate(response);
                $('#login').hide();
                $('#loggedin').show();
            },
        });
    }else{
        $('#login').show();
        $('#loggedin').hide();
    }
})();
