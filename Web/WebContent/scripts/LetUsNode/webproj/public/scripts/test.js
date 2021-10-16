function product(a,b){
	//document.write('<br>*** Function: "product" ***<br>');
	return a*b;
}

function spaces(num){
	//document.write('<br>*** Function: "spaces" ***<br>');
	var i=0;
	for (i=0; i<num; i++){
		document.write("<br>");
	}
}

function swin(){
	//document.write('<br>*** Function: "swin" ***<br>');
	var smallwin=window.open("", "Window Test", "width=600,height=300");

	smallwin.document.write('<link rel="stylesheet" href="./style_sheets/win.css">');
	smallwin.document.write('<h1>This is a test of the small window</h1><br>');
	smallwin.document.write('<h6>The name of the window is ', smallwin.name,'</h6>');
	smallwin.document.write('<h6>The location of the window is ', smallwin.location,'</h6>');
	smallwin.document.write('<p><input type="button" value="Close" onclick="self.close()"></p>');
	smallwin.document.write('<br>');
}

function navbar(){
	// creates a navigation bar
	document.write('<ul class="navbar">');
	document.write('<li><a href="test1.html">Home page</a>');
	document.write('<li><a href="test2.html">Links</a>');
	document.write('<li><a href="test3.html">Something else</a>');
	document.write('</ul>');
}