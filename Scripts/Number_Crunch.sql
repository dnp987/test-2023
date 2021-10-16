select year, make, model, avg(price) from prices where price > 0 group by year, make, model order by year;
select year, make, model, avg(price) from prices where price > 0 group by year, make, model order by make, model, year;
select  year, make, model, min(price) from prices group by year, make, model order by year;
select  year, make, model, max(price) from prices group by year, make, model order by year;
select year, make, model, count(price) from prices where price > 0 group by year, make, model order by year;

select * from prices order by model;
select * from prices where make = "Mazda" and model = "Mazda3 GX";
select * from prices where dealer_id like "%CHRYSLER%";
select * from prices where dealer_id not like "%FORD%" and model = "Focus";
select * from prices where model = "Focus";
select * from prices where URL = "N/A";
select year, make, model, price, stock_num, Name, Location, Phone, URL from dealers, prices where dealers.ID  = prices.dealer_id and prices.price > 0 and prices.price <=1000 order by price asc;
select year, make, model, price, stock_num, Name, Location, Phone, URL from dealers, prices where dealers.ID  = prices.dealer_id and prices.price > 10000 and prices.price < 20000 order by price asc;
select year, make, model, price, stock_num, Name, Location, Phone, URL from dealers, prices where dealers.ID  = prices.dealer_id and prices.price > 50000 and prices.price < 75000 order by price asc;
select year, make, model, price, stock_num, Name, Location, Phone, URL from dealers, prices where dealers.ID  = prices.dealer_id and prices.price > 75000 order by price asc;

select count(*) from prices; # total number of cars for sale
select count(*) from prices where price = 0; # total number of cars with no price