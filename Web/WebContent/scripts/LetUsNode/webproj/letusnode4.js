const express = require ( 'express' );
const app = express();
const router = express.Router();

router.get( '/home' , (req,res) => {
	var test = 5678;
	console.log(test||1234);
	res.send( 'Hello World, This is home router' );
});

router.get( '/profile' , (req,res) => {
	res.send( 'Hello World, This is profile router');
});

router.get( '/login' , (req,res) => {
	res.send( 'Hello World, This is login router');
});

router.get( '/logout' , (req,res) => {
	res.send( 'Hello World, This is logout router');
});

app.use( '/' , router);

app.listen(process.env.port || 3000 );

console .log( 'Web Server is listening at port ' + (process.env.port
|| 3000 ));