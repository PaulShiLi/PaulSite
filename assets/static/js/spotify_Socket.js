var spotifyHistory;
var spotifyStatus;

$.get("/api/spotify", (data, status) => {
  spotifyHistory = data;
    songHistory(spotifyHistory);
});

var myInterval = setInterval(function () {
    // Sleep for 1 second
    $.get("/api/spotify/status", (data, status) => {
        spotifyStatus = data;
    });
    console.log(spotifyStatus);
    if (spotifyStatus["status"] != "noCurrentSong") {
        if (spotifyStatus["status"] == "currentSong") {
          currentSong(spotifyStatus);
        }
      }
      if (spotifyStatus["status"] == "noCurrentSong") {
        noCurrentSong(spotifyStatus);
    }
}, 1000);

function songHistory(spotifyStatus) {
  // Song history
  // Get song history
  // console.log(spotifyStatus)
  shortTerm = spotifyStatus["recents"];
  mediumTerm = spotifyStatus["mediumTerm"];
  longTerm = spotifyStatus["longTerm"];
  // console.log(shortTerm);
  // Process short term songs
  createHTML_term(shortTerm, "shortTerm");
  // Process medium term songs
  createHTML_term(mediumTerm, "mediumTerm");
  // Process long term songs
  createHTML_term(longTerm, "longTerm");
}

function createHTML_term(termData, term) {
  var song, html, el;
  for (var i = 0; i < termData.length; i++) {
    song = termData[i];
    // console.log(song['timeAccessed']);
    html = `<div class="img__wrap"><img src="${song["pic"]}">
            <div class="img__description">
                <h5 class="heading songTitle text-break">${song["name"]}</h3>
                <h6 class="subtitle songArtist text-break">${song["artist"]}</h5>
            </div><a class="stretched-link songLink" href=${song["link"]} target="_blank"></a>
            </div>
        `;
    el = document.createElement("li");
    el.innerHTML = html;
    songExistInList(el, `${term}-${i % 2}`, song["link"]);
  }
}

function songExistInList(song, term, link) {
  var indexed = false,
    songNames,
    songArtists,
    id;
  if (term == "shortTerm-0") {
    id = "pastMonth-1";
  }
  if (term == "shortTerm-1") {
    id = "pastMonth-2";
  }
  if (term == "mediumTerm-0") {
    id = "past6Months-1";
  }
  if (term == "mediumTerm-1") {
    id = "past6Months-2";
  }
  if (term == "longTerm-0") {
    id = "allTime-1";
  }
  if (term == "longTerm-1") {
    id = "allTime-2";
  }
  var list = document.getElementById(id);
  songLinks = list.getElementsByClassName("songLink");
  for (var i = 0; i < songLinks.length; i++) {
    // console.log(songNames[i].innerHTML);
    // console.warn("Comparing " + songNames[i].innerHTML + " with " + name + " and " + songArtists[i].innerHTML + " with " + artist);
    if (songLinks[i].href == link) {
      indexed = true;
      break;
    }
  }
  if (indexed == false) {
    list.prepend(song);
  }
}

function noCurrentSong() {
  // No song playing
  if (document.getElementById("currentCover_img").src != "/static/img/noSongs.png") {
    // Set no song title
    document.getElementById("currentCover_Song").innerHTML = "No song playing";
    // Set no song cover
    document.getElementById("currentCover_img").src = "/static/img/noSongs.png";
    // Set no song artist
    document.getElementById("currentCover_Artist").innerHTML = "";
    // Set no song link
    document.getElementById("currentCover_Link").href = "404";
  }
  // Hide music bar by adding hidden attribute
  document.getElementById("musicBar").setAttribute("hidden", "");
}

function currentSong(spotifyStatus) {
  document.getElementById("alt_musicBar").setAttribute("hidden", "");
  // Playing song
  if (document.getElementById("currentCover_Link").href != spotifyStatus["link"]) {
    // Set song cover
    document.getElementById("currentCover_img").src = spotifyStatus["pic"];
    // Set song title
    document.getElementById("currentCover_Song-1").innerHTML = spotifyStatus["name"];
    document.getElementById("currentCover_Song").innerHTML = spotifyStatus["name"];
    // Set song artist
    document.getElementById("currentCover_Artist-1").innerHTML = spotifyStatus["artist"];
    document.getElementById("currentCover_Artist").innerHTML = spotifyStatus["artist"];
    // Set song link
    document.getElementById("currentCover_Link").href = spotifyStatus["link"];
  }
  document.getElementById("musicBar").removeAttribute("hidden");
  // Check if currentDuration exists and if so show music bar
  if (spotifyStatus["currentDuration"] != null) {
      // Show music bar by removing hidden attribute
      // Get durations in milliseconds
      var currentDuration = spotifyStatus["currentDuration"];
      var totalDuration = spotifyStatus["totalDuration"];
      //    console.log("Current Duration: " + currentDuration + " milliseconds")
      //    console.log("Total Duration: " + totalDuration + " milliseconds")
      /* 
              Convert duration in seconds to hours, minutes and seconds
              */
      // Convert current duration to hours, minutes and seconds
      var current_ss = Math.floor(currentDuration / 1000);
      var current_mm = Math.floor(current_ss / 60);
      var current_hh = Math.floor(current_mm / 60);
      current_ss = current_ss % 60;
      current_mm = current_mm % 60;
      current_hh = current_hh % 60;
      // Convert total duration to hours, minutes and seconds
      var total_ss = Math.floor(totalDuration / 1000);
      var total_mm = Math.floor(total_ss / 60);
      var total_hh = Math.floor(total_mm / 60);
      total_ss = total_ss % 60;
      total_mm = total_mm % 60;
      total_hh = total_hh % 60;
      // Format current duration
      var current_hhmmssFormat = "";
      if (current_hh > 0) {
        current_hhmmssFormat = current_hh + ":";
      }
      if (current_mm < 10) {
        current_mm = "0" + current_mm;
      }
      if (current_ss < 10) {
        current_ss = "0" + current_ss;
      }
      current_hhmmssFormat = current_hhmmssFormat + current_mm + ":" + current_ss;
      // Format total duration
      var total_hhmmssFormat = "";
      if (total_hh > 0) {
        total_hhmmssFormat = total_hh + ":";
      }
      if (total_mm < 10) {
        total_mm = "0" + total_mm;
      }
      if (total_ss < 10) {
        total_ss = "0" + total_ss;
      }
      total_hhmmssFormat = total_hhmmssFormat + total_mm + ":" + total_ss;
      // Set current duration
      document.getElementById("currentDuration").innerHTML = current_hhmmssFormat;
      // Set total duration
      document.getElementById("totalDuration").innerHTML = total_hhmmssFormat;
      /*
              Setting the progress bar duration
              */
      // Set progress bar max value
      document.getElementById("musicProgressBar").max = totalDuration;
      // Set progress bar value
      document.getElementById("musicProgressBar").value = currentDuration;
  }
  else {
    // Hide music bar by adding hidden attribute
    document.getElementById("musicBar_Inner").setAttribute("hidden", "");
    
    if (spotifyStatus["end"] != null){
      document.getElementById("alt_musicBar").removeAttribute("hidden");
      // Will be a unix timestamp in the format of 1722314.638009
      // Convert to seconds
      var end = spotifyStatus["end"];
      // Get current time in seconds
      // var currentTime = Math.floor(Date.now() / 1000);
      // Get time remaining in seconds
      var timeRemaining = end - Math.floor(Date.now() / 1000);

      console.log("Time Remaining: " + timeRemaining + " seconds");
      // Convert time remaining to hours, minutes and seconds
      var timeRemaining_ss = timeRemaining;
      var timeRemaining_mm = Math.floor(timeRemaining_ss / 60);
      var timeRemaining_hh = Math.floor(timeRemaining_mm / 60);
      timeRemaining_ss = timeRemaining_ss % 60;
      timeRemaining_mm = timeRemaining_mm % 60;
      timeRemaining_hh = timeRemaining_hh % 60;

      // Round seconds to nearest whole number
      timeRemaining_ss = Math.round(timeRemaining_ss);

      console.log("Time Remaining: " + timeRemaining_hh + " hours " + timeRemaining_mm + " minutes " + timeRemaining_ss + " seconds");
      // Format time remaining
      var timeRemaining_hhmmssFormat = "";
      if (timeRemaining_hh > 0) {
        timeRemaining_hhmmssFormat = timeRemaining_hh + ":";
      }
      if (timeRemaining_mm < 10) {
        timeRemaining_mm = "0" + timeRemaining_mm;
      }
      if (timeRemaining_ss < 10) {
        timeRemaining_ss = "0" + timeRemaining_ss;
      }
      timeRemaining_hhmmssFormat = timeRemaining_hhmmssFormat + timeRemaining_mm + ":" + timeRemaining_ss
      
      // Set time remaining
      document.getElementById("remainingDuration").innerHTML = timeRemaining_hhmmssFormat;
    }
  }
}
