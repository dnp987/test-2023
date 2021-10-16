var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "dnp",
  password: "Npaapita5",
  database: "carsdb"
});

con.connect(function(err) {
  if (err) throw err;
  //con.query("SELECT * FROM prices where", function (err, result, fields) {
	con.query("select year, make, model, price, stock_num, Name, Location, Phone, URL from dealers, prices where dealers.ID  = prices.dealer_id and prices.price < 10000 and prices.price > 5000 order by price asc;", function (err, result, fields) {
    if (err) throw err;
    console.log(result);
  });
});