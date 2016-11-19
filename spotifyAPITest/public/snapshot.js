/**
 * Created by szh on 11/9/16.
 */
'use strict'
var video = document.getElementById('video');
var videoContainer = document.getElementById('videoContainer')
var mediaStream;
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
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
    context.drawImage(video, 0, 0, 48, 48);
    mediaStream.stop();
    // video.style.display='';
    document.getElementById('videoContainer').style.display="none";
});
document.getElementById("again").addEventListener("click", function() {
    videoContainer.style.display = 'initial';
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
    });
});
document.getElementById("upload").addEventListener('click',function () {

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

});
