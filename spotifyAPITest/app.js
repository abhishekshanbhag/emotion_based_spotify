/**
 * This is an example of a basic node.js script that performs
 * the Authorization Code oAuth2 flow to authenticate against
 * the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/web-api/authorization-guide/#authorization_code_flow
 */
var AWS = require('aws-sdk');
var uuid = require('node-uuid');
var express = require('express'); // Express web server framework
var request = require('request'); // "Request" library
var querystring = require('querystring');
var cookieParser = require('cookie-parser');
var session = require('express-session');
var bodyParser = require('body-parser');
var multer = require('multer');
var PythonShell = require('python-shell');
var morgan = require('morgan');

const storage = multer.memoryStorage();
const upload = multer({storage:storage});

var client_id = '566cac34a93e413abbdfbb7e549f02df'; // Your client id
var client_secret = '830cdce64ade49de98b8296f23c18286'; // Your secret
var redirect_uri = 'http://localhost:8888/callback'; // Your redirect uri
/**
 * Generates a random string containing numbers and letters
 * @param  {number} length The length of the string
 * @return {string} The generated string
 */
var generateRandomString = function(length) {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (var i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
};

var stateKey = 'spotify_auth_state';

var app = express();
app.use(morgan('dev'));
// app.use(express.static(__dirname + '/public'))
app.use(cookieParser());
// Login
app.get('/login', function(req, res) {

  var state = generateRandomString(16);
  res.cookie(stateKey, state);

  // your application requests authorization
  var scope = 'user-read-private user-read-email';
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));
});
// Log out
app.get('/logout',function(req,res){
  res.clearCookie('access_token');
  res.redirect('http://localhost:63342/spotifyAPITest/public/index.html');
});

app.get('/callback', function(req, res) {

  // your application requests refresh and access tokens
  // after checking the state parameter

  var code = req.query.code || null;
  var state = req.query.state || null;
  var storedState = req.cookies ? req.cookies[stateKey] : null;

  if (state === null || state !== storedState) {
    res.redirect(' /#' +
      querystring.stringify({
        error: 'state_mismatch'
      }));
  } else {
    res.clearCookie(stateKey);
    var authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      form: {
        code: code,
        redirect_uri: redirect_uri,
        grant_type: 'authorization_code'
      },
      headers: {
        'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
      },
      json: true
    };

    request.post(authOptions, function(error, response, body) {
      if (!error && response.statusCode === 200) {

        var access_token = body.access_token,
            refresh_token = body.refresh_token;
        var options = {
          url: 'https://api.spotify.com/v1/me',
          headers: { 'Authorization': 'Bearer ' + access_token },
          json: true
        };

        // use the access token to access the Spotify Web API
        request.get(options, function(error, response, body) {
          console.log(body);
        });
        res.cookie('access_token', access_token, { maxAge: 900000, httpOnly: false });
        // we can also pass the token to the browser to make requests from there
        // res.redirect('/#' +
        //   querystring.stringify({
        //     access_token: access_token,
        //     refresh_token: refresh_token
        //   }));
        res.redirect('http://localhost:63342/spotifyAPITest/public/index.html');
      } else {
        res.redirect('/#' +
          querystring.stringify({
            error: 'invalid_token'
          }));
      }
    });
  }
});
// Upload
app.post('/upload',upload.single('file'),function(req,res){
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  var s3 = new AWS.S3();
  // var bucketName = 'ec601emotify';
  var bucketName = 'ec601imagebucket';

  var filename = req.body.userID;
  var params = {
    Bucket: bucketName,
    Body: new Buffer(req.file.buffer),
    ACL: 'public-read',
    ContentType: 'multipart/form-data',
    Key:filename
  };
  s3.upload(params,function(err,data){
    if (err){
      console.log('err');
    }else{
      console.log('success');
    }
  })
});
// run py
app.get('/runpy',function (req,res) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");

  var pyshell = new PythonShell('classify_image.py');
  pyshell.stdout.on('data',function(data){
    if (data == 0){
      res.send('happy');
      console.log('happy face');
      pyshell.end(function (err) {
        console.log('ignore');
      });
    }
    if(data == 1){
      res.send('sad');
      console.log('sad face');
      pyshell.end(function (err) {
        console.log('ignore');
      });
    }

  });
});
app.get('/refresh_token', function(req, res) {

  // requesting access token from refresh token
  var refresh_token = req.query.refresh_token;
  var authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    headers: { 'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64')) },
    form: {
      grant_type: 'refresh_token',
      refresh_token: refresh_token
    },
    json: true
  };

  request.post(authOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      var access_token = body.access_token;
      res.send({
        'access_token': access_token
      });
    }
  });
});

console.log('Listening on 8888');
app.listen(8888);
