//require the express nodejs module
var mysql = require('mysql');
var express = require('express'),

  //set an instance of exress
  app = express();

var con = mysql.createConnection({
  host: "localhost",
  user: "dnp",
  password: "Npaapita5",
  database: "carsdb"
});
//tell express what to do when the / route is requested
app.get('/', function (req, res) {
	var low_price = 5000;
	var high_price = 12000;
    con.query('select year, make, model, price, stock_num, Name, Location, Phone, URL from dealers, prices where dealers.ID  = prices.dealer_id and price >' + low_price + ' and price<= ' + high_price + ' order by price asc;',(err, result) => {
        if (err){
        res.status(404).send("Hey we couldn't find it, sorry...");
        }
        else{
        	  //set the appropriate HTTP header and send the data found
  			res.setHeader('Content-Type', 'text/html');
 	 		res.setHeader("Access-Control-Allow-Origin", "*");
	  		res.send(result);
  			res.end();
        }
    });
});

//wait for a connection
app.listen(5000, function () {
  console.log('The web server is running. Please open http://localhost:5000/ in your browser.');
});