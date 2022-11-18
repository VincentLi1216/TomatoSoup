var pics = document.getElementById('pics');

var url = new URL(location.href);
var date = url.searchParams.get('date')
console.log(date);
searchFiles(date);


function searchFiles(fd){
	var paths = []
	fetch("http://114.32.43.46/static/"+fd+"/")
    .then(function(response) {
        return response.text()
    })
    .then(function(html) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, "text/html");

		dirs = doc.querySelectorAll('html body pre a');
		for (i=1;i<dirs.length;i++){
			var temp = String(dirs[i]).split('/');
			paths.push(temp[4]);
		}
        console.log("paths caughted");
        renderGallery(paths);
    })
	.catch(function(err) {  
        console.log('Failed to fetch page: ', err);  
    });
}

function renderGallery(paths) {
	var str = "";
    console.log(paths)
	for(var i=0;i<paths.length;i++){
		console.log(i);
        str += "<li><div class=pics_set><img src='http://114.32.43.46/static/" +  date + "/" + paths[i] + "'></div></li>";
        console.log(str);
	}
	pics.innerHTML = str;
    console.log(pics.innerHTML);
    scroll_to_buttom();
}


function scroll_to_buttom(){
    console.log('go bottom');
    window.scrollTo(0, document.body.scrollHeight);
}
