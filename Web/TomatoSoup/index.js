// Create months' for
var month_olympic = [31,29,31,30,31,30,31,31,30,31,30,31];
var month_normal = [31,28,31,30,31,30,31,31,30,31,30,31];
var month_name = ["January","Febrary","March","April","May","June","July","Auguest","September","October","November","December"];

var holder = document.getElementById("days");
var prev = document.getElementById("prev");
var next = document.getElementById("next");
var ctitle = document.getElementById("calendar-title");
var cyear = document.getElementById("calendar-year");
var showpic = document.getElementById("showpic");
var selected_date = new Date();
var selected_year = selected_date.getFullYear();
var selected_month = selected_date.getMonth();
var selected_day = selected_date.getDate();

// Function to show the first day of the month
function day_Start_intheMonth(month, year) {
	var tmpDate = new Date(year, month, 1);
	return (tmpDate.getDay());
}

// Funcion to decide it's Olympic month or Normal month 
function days_in_Month(month, year) {
	if (year % 4 === 0 && year % 100 !== 0 || year % 400 === 0) {
		return (month_olympic[month]);
	} else {
		return (month_normal[month]);
	}
}

// Render the Airboard Gallery page
function refreshDate(){
	var str = "";
	var totalDay = days_in_Month(selected_month, selected_year); 
	var firstDay = day_Start_intheMonth(selected_month, selected_year); 
	var myclass;
	for(var i = 1; i < firstDay; i++){ 
		str += "<li></li>";
	}
	for(var i = 1; i <= totalDay; i++){
		if((i < selected_day && selected_year == selected_date.getFullYear() && selected_month == selected_date.getMonth()) || selected_year < selected_date.getFullYear() || ( selected_year == selected_date.getFullYear() && selected_month < selected_date.getMonth())){ 
			myclass = " class='darkgrey days'"; 
		}else if (i == selected_day && selected_year == selected_date.getFullYear() && selected_month == selected_date.getMonth()){
			myclass = " class='days'";
		}else{
			myclass = " class='lightgrey days'";
		}
		/*str += "<a href='" + t + "'><li"+myclass+">"+i+"</li></a>";*/
		str += "<li"+myclass+">"+i+"</li>";
	}
	holder.innerHTML = str; 
	ctitle.innerHTML = month_name[selected_month]; 
	cyear.innerHTML = selected_year;
}
refreshDate();

// Function to move to previous or next month
prev.onclick = function(e){
	e.preventDefault();
	selected_month--;
	if(selected_month < 0){
		selected_year--;
		selected_month = 11;
	}
	refreshDate();
}
next.onclick = function(e){
	e.preventDefault();
	selected_month++;
	if(selected_month > 11){
		selected_year++;
		selected_month = 0;
	}
	refreshDate();
}

// Click days elements -> 
document.getElementById("days").addEventListener("click", function(e) {
    if (e.target && e.target.matches("li")&&(e.target.innerText != 0)) { 
		
		var rawFile = new XMLHttpRequest();	
		var fFile = new XMLHttpRequest();
		rawFile.open("GET", "../data.txt", false);
		fFile.open("POST", "../data.txt", true);
		res = ""
		rawFile.onreadystatechange = function (){
			// When web is on connection / If web page is ready or sending initialization
			if(rawFile.readyState === 4 && (rawFile.status === 200 || rawFile.status == 0)){
				var allText = rawFile.responseText;
				ds = allText.split("/")
				tmp = parseInt(ds[0])+1;
				res = String(tmp)+"/"+ds[1];
				console.log(res);
			}
		}
		rawFile.send(null);
		fFile.send(res)

		if (e.target.innerText < 10){
			window.location.href = "gallery.html?date="+(selected_month+1)+"-0"+e.target.innerText+"-"+selected_year;
		}else{
			window.location.href = "gallery.html?date="+(selected_month+1)+"-"+e.target.innerText+"-"+selected_year;
		}
    }
});


