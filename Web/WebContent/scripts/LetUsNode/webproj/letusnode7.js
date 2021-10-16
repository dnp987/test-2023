const express = require('express');
const app = express();
let mysql = require('mysql');
const bodyParser = require ( 'body-parser' );
const path = require('path');
app.use(bodyParser.urlencoded({ extended: true })); 
const router = express.Router();

app.use(express.static(path.join(__dirname, 'public'))); // set the root path
app.use('/css', express.static(path.join(__dirname, 'public'))) // path for css files
app.use('/scripts', express.static(path.join(__dirname, 'public'))) // path for javascript files
app.use('/images', express.static(path.join(__dirname, 'public'))) // path for image files
router.get( '/' , (req,res) => {
	//console.log(req.url);
	//res.setHeader('Content-type', 'application/json');
	//res.send('{"message":"This is the default router"}');
	//res.setHeader('Content-type', 'text/html');
	const file_name = '/public/test1.html';
	res.sendFile(__dirname + file_name);
});
/*
router.get( '/home' , (req,res) => {
	console.log(req.url);
	console.log(req.method);
	res.setHeader('Content-type', 'text/plain');
	res.send( 'Hello World, This is home router' );
});

router.get( '/profile' , (req,res) => {
	console.log(req.url);
	res.setHeader('Content-type', 'text/plain');
	res.send( 'Hello World, This is profile router');
});

router.get( '/login' , (req,res) => {
	console.log(req.url);
	res.setHeader('Content-type', 'text/html');
	res.send( "<h1>Hello World</h1><p>This is HTML response</p><ol><li>One</li><li>Two</li><li>Three</li></ol>");
});

router.get( '/logout' , (req,res) => {
	console.log(req.url);
	res.setHeader('Content-type', 'text/plain');
	res.send( 'Hello World, This is logout router');
});
*/

let con = mysql.createConnection({
  host: "localhost",
  user: "dnp",
  password: "Npaapita5",
  database: "carsdb"
});

router.post('/action1', function(req, res) {
	let car_data = '<!DOCTYPE html><html><head><meta charset="ISO-8859-1"></head><body>';
	
	let min_price = req.body.min;
	let max_price = req.body.max;
	//console.log(min_price, max_price);
	con.query('select year, make, model, price, stock_num, Name, URL from dealers, prices where dealers.ID  = prices.dealer_id and price >' + min_price + ' and price <= ' + max_price + ' order by price asc;',(err, result) => {
  	if (err){
        res.status(404).send('<p style = "color:white;">' + 'Hey we couldn' +'t find it, sorry!'+'</p>');
        }
    else{
    	 var formatter = new Intl.NumberFormat('en-US', {
    	style: 'currency',
    	currency: 'USD',
    	});
    	
    	car_data += '<p style = "color:white;">' + result.length + ' cars found between ' + formatter.format(min_price) + ' and ' + formatter.format(max_price) + '</p>';
    	car_data += '<table style = "text-align:left; color:white;"><tr><th>#</th><th>Year</th><th>Make</th><th>Model</th><th>Price</th><th>Dealer</th><th>Stock #</th><th>Go to Car</th></tr>';

		let index = 0;
		for (let i =0; i< result.length; i++){
			let price = formatter.format(result[i].price);
			index = i+1;
			//car_data += '<p style ="color:white;">' + index + ' : ' + result[i].year + '  '+ result[i].make + '  ' + result[i].model + '  ' + price + '  ' + result[i].Name + '  ' + result[i].stock_num +
			// '    ' + '<a href =' + result[i].URL + '  target = "_blank" style= "color:yellow;">' + result[i].make + '  ' + result[i].model + '    </a>'  + '</p>'; 
			 car_data += '<tr style = "text-align:left; color:white;"><td>' + index + ' : '+'</td><td>' + result[i].year + '</td><td>'+ result[i].make + '</td><td>' + result[i].model + '</td><td>' + price + '</td><td>' + result[i].Name + '</td><td>' + result[i].stock_num +
			 '</td><td><a href =' + result[i].URL + '  target = "_blank" style= "color:yellow;">' + result[i].make + ' ' + result[i].model + ' </a>'  + '</td></tr>';
		}
		car_data += '</table></body></html>';
		res.send(car_data);	
  		res.end();
    	}
    });
});

app.use( '/' , router);

app.listen(process.env.port || 3000 );

console .log( 'Web Server is listening at port ' + (process.env.port
|| 3000 ));