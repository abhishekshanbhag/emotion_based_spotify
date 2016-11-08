/**
 * Created by szh on 10/11/16.
 */
'use strict';
var url = "https://api.spotify.com/v1/search?q=sad&type=album&limit=1";
var templateSource = document.getElementById('template').innerHTML;
var template = Handlebars.compile(templateSource);
var get = function(url, callback) {
    var xhp = new XMLHttpRequest();
    xhp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200){
            if(typeof callback === "function"){
                callback(xhp.responseText);
            }
        }
    };
    xhp.open("GET",url,true);
    xhp.send();
};

function  mycallback(response) {
    response = JSON.parse(response);

    document.getElementById('test').innerHTML = template(response);
    // document.getElementById('test').innerHTML = response;
}

get(url,mycallback);