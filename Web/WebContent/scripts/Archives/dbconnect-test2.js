var mysql = require('mysql');
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({ extended: false });

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.use('/', express.static(__dirname + '/', {
    index: false, 
    immutable: true, 
    cacheControl: true,
    maxAge: "30d"
}));

app.set('view engine', 'html');

var connection = mysql.createConnection({
  host: "localhost",
  user: "dnp",
  password: "Npaapita5",
  database: "carsdb"
});

app.get('/',(req, res) => {
	var car_list = [ ];
	var p_tag_start = "<p>";
	var p_tag_end = "<\/p>";
	var temp = "";

	var doc_heading = "<!DOCTYPE HTML><html><head><title>Test<\/title>" + '<link type ="text/css" rel="stylesheet" href="./css/test-style.css">' + "<\/head>";
	var doc_middle = "<body><h1>GTA Used Car Data <\/h1>";
	var doc_end = "<\/body><\/html>";
	
    connection.connect(function(err) {
    if(err) throw err;
        else {
            connection.query("select year, make, model, price, stock_num, Name, Location, Phone, URL from dealers, prices where dealers.ID  = prices.dealer_id and prices.price < 10000 and prices.price > 5000 order by price asc;",(err, result) => {
                if(err) {
                    console.log(err); 
                    res.json({"error":true});
                }
                else { 
                    console.log(result.length + " records found");
                    temp = doc_heading + doc_middle;
                    for (i = 0; i < result.length; i++){
        				temp +=  p_tag_start + "Name: " + result[i].Name + " Year: " + result[i].year + " Make: " + result[i].make + " Model: " + result[i].model + " Price: " + result[i].price + " URL: " + result[i].URL + p_tag_end;
        			}
        			temp += doc_end;
        			res.send(temp);
	            }
            });
        }
    });
});

app.listen(3000, function () {
    console.log('Connected to port 3000');
});