const http = require('http');
const hostname = 'localhost';
const port = 3000;
const server = http.createServer((req, res) => {
	res.statusCode = 200;
	//res.setHeader('Content-type', 'text/plain');
	//res.setHeader('Content-type', 'application/json');
	res.setHeader('Content-type', 'text/html');
	//res.end('hello world');
	//res.end('{"message":"Hello World"}');
	res.end(
		"<h1>Hello World</h1><p>This is HTML response</p><ol><li>One</li><li>Two</li><li>Three</li></ol>"
		);
	});
	
server.listen(port, hostname, () => {
	console.log(`Server running at http://${hostname}:${port}/`);
});
