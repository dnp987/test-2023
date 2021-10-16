//step 1) require the modules we need
var
http = require('http'),
path = require('path'),
fs = require('fs');

//helper function handles file verification
function getFile(filePath,res,page404){
	//does the requested file exist?
	fs.exists(filePath,function(exists){
		//if it does...
		if(exists){
			//read the fiule, run the anonymous function
			fs.readFile(filePath,function(err,contents){
				if(!err){
					//if there was no error
					//send the contents with the default 200/ok header
					res.end(contents);
				} else {
					//for our own troubleshooting
					console.dir(err);
				};
			});
		} else {
			//if the requested file was not found
			//serve-up our custom 404 page
			fs.readFile(page404,function(err,contents){
				//if there was no error
				if(!err){
					//send the contents with a 404/not found header 
					res.writeHead(404, {'Content-Type': 'text/html'});
					res.end(contents);
				} else {
					//for our own troubleshooting
					console.dir(err);
				};
			});
		};
	});
};

//a helper function to handle HTTP requests
function requestHandler(req, res) {
	var 	fileName = path.basename(req.url) || 'test1.html';
	process.chdir("../public");
	localFolder = process.cwd();
	page404 = localFolder + '/' + '404.html';
	console.log("Request method: " + req.method);
	console.log(localFolder + '/' +  fileName);
	if (req.method == 'GET') {
		getFile((localFolder + '/' + fileName),res,page404);
	}
};

//step 2) create the server
http.createServer(requestHandler)

//step 3) listen for an HTTP request on port 3000
.listen(3000);
 console.log('The web server is running. Please open http://localhost:3000/ in your browser.');