var express = require('express');
var bodyParser = require('body-parser');
var app = express();

//Note that in version 4 of express, express.bodyParser() was
//deprecated in favor of a separate 'body-parser' module.
app.use(bodyParser.urlencoded({ extended: true })); 

app.post('/action1', function(req, res) {
	console.log(req.body);
  	res.send('Low Price: ' + req.body.low + ' High Price: ' + req.body.high);
});

app.listen(5000, function() {
  console.log('The web server is running. Please open http://localhost:5000/ in your browser.');
});