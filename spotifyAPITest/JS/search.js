// find template and compile it
var templateSource = document.getElementById('results-template').innerHTML;
var template = Handlebars.compile(templateSource),
    resultsPlaceholder = document.getElementById('results'),
    playingCssClass = 'playing',
    audioObject = null;

// var fetchTracks = function(albumId, callback) {
//     $.ajax({
//         url: 'https://api.spotify.com/v1/albums/' + albumId,
//         success: function(response) {
//             callback(response);
//         }
//     });
// };

var searchAlbums = function(query) {
    $.ajax({
        url: 'https://api.spotify.com/v1/search',
        data: {
            q: query,
            type: 'playlist'
        },

        success: function(response) {
            if ( document.getElementById('query').innerHTML == 'a'){
                alert('Please type in Key words');
            }
            document.getElementById('results').innerHTML = template(response);
        }
    });
    // $.ajax({
    //     url: 'https://api.spotify.com/v1/browse/categories/'+query+'/playlists',
    //     headers: { 'Authorization': 'Bearer ' + document.cookie.slice(13) },
    //
    //     success: function(response) {
    //         console.log('get category');
    //         document.getElementById('results').innerHTML = template(response);
    //     }
    // });
};

// document.getElementById('search-form').addEventListener('submit', function(e) {
//     e.preventDefault();
//     searchAlbums(document.getElementById('query').value);
// }, false);
