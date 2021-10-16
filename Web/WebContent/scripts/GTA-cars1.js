var express = require('express');
var mysql = require('mysql');
var bodyParser = require('body-parser');
var app     = express();

// *** Use with GTA-cars1.html only *** 

//Note that in version 4 of express, express.bodyParser() was
//deprecated in favor of a separate 'body-parser' module.

var con = mysql.createConnection({
  host: "localhost",
  user: "dnp",
  password: "Npaapita5",
  database: "carsdb"
});

app.use(bodyParser.urlencoded({ extended: true })); 

var car_data = '';
//car_data = '<!DOCTYPE html><html><head><meta charset="ISO-8859-1"><link rel="stylesheet" type ="text/css" href="../css/cars-style.css"/></head><body>';
car_data = '<!DOCTYPE html><html><head><meta charset="ISO-8859-1"></head><body>';

app.post('/action1', function(req, res) {
	var car_data = ''; // start with no data, that way there's nothing left over from the previous request
	var low_price = req.body.low;
	var high_price = req.body.high;
	//console.log(low_price, high_price);
	con.query('select year, make, model, price, stock_num, Name, Location, Phone, URL from dealers, prices where dealers.ID  = prices.dealer_id and price >' + low_price + ' and price <= ' + high_price + ' order by price asc;',(err, result) => {
  	if (err){
        res.status(404).send("Hey we couldn't find it, sorry...");
        }
    else{
    	//console.log(result.length)
		for (var i =0; i< result.length; i++){
			car_data += '<p style ="color:white;">'+ result[i].year +'  '+ result[i].make +'  '+result[i].model+'  '+result[i].price+'  '+ result[i].Name + '  ' + result[i].stock_num + '    ' + '<a href =' + result[i].URL + '  target = "_blank" style= "color:yellow;">' + result[i].make + '  '+ result[i].model + '    </a>'  + '</p>';
		}
		if (result.length == 0){
    		car_data += '<p style="color:yellow;">' + 'Sorry, no cars found selling between ' + low_price + ' and ' + high_price +'</p>'; 
    	}
		car_data += '</body></html>';
		res.send(car_data);	
  		res.end();
    	}
    });
});

app.listen(5000, function() {
  console.log('The web server is running. Please open http://localhost:5000/ in your browser.');
});