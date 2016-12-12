/**
 * Created by szh on 11/9/16.
 */
'use strict'
var video = document.getElementById('video');
var videoContainer = document.getElementById('videoContainer')
var mediaStream;
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
        mediaStream = stream.getTracks()[0];
    });
}
// Elements for taking the snapshot
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');

// Trigger photo take 
document.getElementById("snap").addEventListener("click", function() {
    // context.drawImage(video, 200, 20, 240, 360,0,0,48,48);
    context.drawImage(video, 0, 0,480,360);
    mediaStream.stop();
    document.getElementById('videoContainer').style.display="none";
    document.getElementById('canvasContainer').style.display="block";
});
document.getElementById("again").addEventListener("click", function() {
    videoContainer.style.display = 'block';
    document.getElementById('canvasContainer').style.display="none";
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
    });
});
document.getElementById("run").addEventListener('click',function () {

    var dataUrl = canvas.toDataURL();
    var blobData = dataURItoBlob(dataUrl);
    var filename = document.getElementById("userId").innerHTML.substr(6);
    function dataURItoBlob(dataURI) {
        var binary = atob(dataURI.split(',')[1]);
        var array = [];
        for(var i = 0; i < binary.length; i++) {
            array.push(binary.charCodeAt(i));
        }
        return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
    }
    var fd = new FormData();

    fd.append('userID',filename);
    fd.append('file',blobData);
    $.ajax({
        url:'http://localhost:8888/upload',
        type:'POST',
        data: fd,
        processData: false,
        contentType: false,
        success:function (data) {
            console.log(data);
        }
    });

    $.ajax({
        url:'http://localhost:8888/runpy/'+filename,

        success: function(res) {
            console.log(res);
            var templateSource = document.getElementById('results-template').innerHTML;
            var template = Handlebars.compile(templateSource);
            $.ajax({
                url: 'https://api.spotify.com/v1/search',
                data: {
                    q: res,
                    type: 'playlist',
                    limit:50
                },
                success: function (response) {
                    var randResponse = {
                        playlists:{
                            items:[{}],
                        }
                    };

                    var randNum = [];
                    for (var i=0; i<8; i++){
                        randNum[i] = Math.floor((Math.random() * 50) + 1);
                        randResponse.playlists.items[i] = response.playlists.items[randNum[i]];
                    }
                    
                    document.getElementById('results').innerHTML = template(randResponse);
                }
            });
            var randTrack = parseInt(20*Math.random());
            console.log(randTrack);
            $.ajax({
                url: 'https://api.spotify.com/v1/search',
                data: {
                    q: res,
                    type: 'track'
                },
                success: function (response) {
                    var audioObject = new Audio(response.tracks.items[randTrack].preview_url);
                    audioObject.play();
                }
            });
        }
    });
    
});

// document.getElementById("pyTest").addEventListener('click',function(){
//     var filename = document.getElementById("userId").innerHTML.substr(6);
//     $.ajax({
//         url:'http://localhost:8888/runpy/'+filename,
//
//         success: function(res) {
//             console.log(res);
//             var templateSource = document.getElementById('results-template').innerHTML;
//             var template = Handlebars.compile(templateSource);
//             $.ajax({
//                 url: 'https://api.spotify.com/v1/search',
//                 data: {
//                     q: res,
//                     type: 'playlist'
//                 },
//                 success: function (response) {
//                     document.getElementById('results').innerHTML = template(response);
//                 }
//             });
//             var randTrack = parseInt(20*Math.random());
//             console.log(randTrack);
//             $.ajax({
//                 url: 'https://api.spotify.com/v1/search',
//                 data: {
//                     q: res,
//                     type: 'track'
//                 },
//                 success: function (response) {
//                     var audioObject = new Audio(response.tracks.items[randTrack].preview_url);
//                     audioObject.play();
//                 }
//             });
//         }
//     });
// });