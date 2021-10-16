var mysql = require('mysql');
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({ extended: false });

const fs = require('fs');
const path = require('path');

app.use(bodyParser.urlencoded({extended: false}));
app.use('/', express.static(__dirname + '/'));
app.set('view engine', 'html');

var con = mysql.createConnection({
  host: "localhost",
  user: "dnp",
  password: "Npaapita5",
  database: "carsdb"
});

app.get('/', function(request, response){
	var car_list = "";
	var reo = '<!DOCTYPE html><html><head><meta charset="ISO-8859-1"><title>GTA Car Data Test</title></head><body><h1>GTA Car Data Test</h1>table</body></html>';
	console.log('GET request received at /');
    con.query("select year, make, model, price, stock_num, Name, Location, Phone, URL from dealers, prices where dealers.ID  = prices.dealer_id and + prices.price >10000 and prices.price <20000 order by price asc;",(err, result) => {
        //if (err) throw err;
        if (err){
        response.status(404).send("Hey we couldn't fine it, sorry...");
        }
        else{
        	for (i = 0; i < result.length; i++){
        	//car_list[i] = "Name: " + result[i].Name + " Year: " + result[i].year + " Make: " + result[i].make + " Model: " + result[i].model + " Price: " + result[i].price + " URL: " + result[i].URL;
        	car_list += '<tr><td>'+ result[i].Name +'</td><td>'+ result[i].year +'</td><td>'+ result[i].make +'</td><td>'+result[i].model+'</td>+<td>'+result[i].price+'</td><td>'+result[i].URL+'</td></tr>';
        	}
        	car_list = '<table border = 2><thead><tr><th>Dealer</th><th>Year</th><th>Make</th><th>Model</th><th>Price</th><th>URL</th></tr></thead>' + car_list + '</table>';
        	reo = reo.replace('table', car_list);
        	response.send(reo);
            /*response.send(result); */
			console.log(result.length, " records found");
			response.end();
						
			/* console.log(__dirname);
			console.log(process.cwd());
			process.chdir('../');
			response.sendFile(path.join(__dirname, '../', 'test1.html')); */
			
        }

    });
});
/* From a browser: http://localhost:3000/ , 192.168.2.12:3000 , http:/home-pc:3000. Use ipconfig, hostname to get system info */ 
app.listen(3000, function () {
    console.log('Connected to port 3000');
});