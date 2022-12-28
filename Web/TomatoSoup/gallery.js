let pics = document.getElementById('pics');

let url = new URL(location.href);
let date = url.searchParams.get('date')
console.log(date);
searchFiles(date);


function searchFiles(fd) {
	let paths = [];
	fetch("http://114.32.43.46/static/"+fd+"/")
    .then(response => { return response.text() })
    .then(html => {
        // Creat a DOMParser object to parse the html-type text
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        // Select all the line that contains urls needed
		dirs = doc.querySelectorAll('html body pre a');
        // Get the directories for pictures
		for (dir of dirs){
            // Split the whole string and get the urls part
			let temp = String(dir).split('/');
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
	let str = "";
    // Generate html elements and render on the gallery page
	for(path of paths)
        str += "<li><div class=pics_set><img src='http://114.32.43.46/static/" +  date + "/" + path + "'></div></li>";
	pics.innerHTML = str;
    scroll_to_buttom();
}


function scroll_to_buttom(){
    console.log('go bottom');
    window.scrollTo(0, document.body.scrollHeight);
}
