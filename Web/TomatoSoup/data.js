var datas = document.getElementById('datas');
var d = "";

// var reader = new FileReader();
// var ds = reader.readAsText("../data.txt", 'utf-8')

// Read from data.txt
var rawFile = new XMLHttpRequest();
rawFile.open("GET", "../data.txt", false);
rawFile.onreadystatechange = function (){
    // When web is on connection / If web page is ready or sending initialization
    if(rawFile.readyState === 4 && (rawFile.status === 200 || rawFile.status == 0)){
        var allText = rawFile.responseText;
        ds = allText.split("/")
        d += "<div class='dv'>" + "Visits : " + ds[0] + "</div>";
        d += "<div class='dv'>" + "Downloads : " + ds[1] + "</div>";
        datas.innerHTML = d;
    }
}
rawFile.send(null);


// fetch("../data.json").then(response => {
//     return response.json();
// }).then(data => {
//     data = JSON.stringify(data);
    
//     d += "<div class='dv'>" + "Visits : " + JSON.parse(data).visits + "</div>";
//     d += "<div class='dv'>" + "Downloads : " + JSON.parse(data).downloads + "</div>";
//     datas.innerHTML = d;

//     console.log(data);
// });
