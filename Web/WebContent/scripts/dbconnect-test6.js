//require the express nodejs module
var express = require('express'),
  //set an instance of exress
  app = express();

//tell express what to do when the / route is requested
app.get('/', function (req, res) {
  var i = 1,
    max = 7;
    resp = "";

  //set the appropriate HTTP header
  res.setHeader('Content-Type', 'text/html');
  res.setHeader("Access-Control-Allow-Origin", "*");
  
  //send multiple responses to the client
  for (; i <= max; i++) {
   // res.write('<p>This is the response #: ' + i + '</p>');
   resp += '<p>This is response #: ' + i + '</p>';
  }
 res.send(resp);
 res.end();
 //res.send(resp);
});

//wait for a connection
app.listen(5000, function () {
  console.log('The web server is running. Please open http://localhost:5000/ in your browser.');
});