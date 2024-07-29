const fullDay = {
    Mon: "Monday",
    Tue: "Tuesday",
    Wed: "Wednesday",
    Thu: "Thursday",
    Fri: "Friday",
    Sat: "Saturday",
    Sun: "Sunday"
}

const fullMonth = {
    Jan: "January",
    Feb: "February",
    Mar: "March",
    Apr: "April",
    May: "May",
    Jun: "June",
    Jul: "July",
    Aug: "August",
    Sep: "September",
    Oct: "October",
    Nov: "November",
    Dec: "December"
}

const sec = document.querySelector(".sec");
const min = document.querySelector(".min");
const hr = document.querySelector(".hr");

function getFullTime(){
    let time  = new Date();
    // Update Date + Analog time
    var dateString = time.toUTCString().replace(',', '').split(' ');
    // Names for days in week
    var dateWeek = fullDay[dateString[0]];
    // Full month name
    var month = fullMonth[dateString[2]];
    // PST/GMT or whatever the time location
    var timeLocation = new Date().toLocaleTimeString('en-us',{timeZoneName:'short'}).split(' ')[2];
    // Seconds
    var seconds = time.getSeconds().toString()
    if (seconds.length == 1){
        seconds = "0" + seconds;
    }
    var minutes = time.getMinutes().toString()
    if (minutes.length == 1){
        minutes = "0" + minutes;
    }
    // Time type of day
    var timeType = "AM";
    if (time.getHours() >= 12 && time.getHours() != 24){
        timeType = "PM";
    }
    // Hours
    var hours = time.getHours();
    if (hours > 12){
        hours = hours - 12;
    }
    // Full String
    var fullTimeString = dateWeek + ", " + month + " " + time.getDate() + " " + time.getFullYear() + "\n" + hours + ":" + minutes + ":" + seconds + " " + timeType + " " + timeLocation;
    return fullTimeString;
}

setInterval(function(){
    let time  = new Date();
    let secs = time.getSeconds() * 6;
    let mins = time.getMinutes() * 6;
    let hrs = time.getHours() * 30;
    // Update clock
    sec.style.transform = `rotateZ(${secs}deg)`;
    min.style.transform = `rotateZ(${mins}deg)`;
    hr.style.transform = `rotateZ(${hrs+(mins/12)}deg)`;
    // Update Full Time display
    var fullTime = getFullTime();
    document.getElementById("date").innerText = fullTime;
});