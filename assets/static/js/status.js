var myInterval = setInterval(function () {
  $.getJSON("/static/api/api.json", function (response) {
      discordStatus = response.discord.status;
  });
  changeStatus(discordStatus['discordStatus']);
    if (discordStatus['customStatus'] != null){
      if (document.getElementById('discordStatusText').innerText != discordStatus['customStatus']) {
        document.getElementById('discordStatusText').innerText = discordStatus['customStatus'];
      }
    }
    else {
        if (document.getElementById('discordStatusText').innerText != '') {
          document.getElementById('discordStatusText').innerText = '';
        }
    }
}, 1000);

function changeStatus(status){
    var statusEl = document.getElementById('status');
      if (status == "online"){
        statusEl.innerHTML = '<circle cx="25" cy="25" r="12" fill="#3ba55d" />'
      }
      else if (status == "dnd"){
        statusEl.innerHTML = '<defs> <mask id="dndMask"> <circle cx="25" cy="25" r="12" fill="white" /> <rect x="20" y="24" width="10" height="4" fill="#black"></rect> </mask> </defs> <rect fill="#ed4245" width="100%" height="100%" mask="url(#dndMask)" />'
      }
      else if (status == "idle"){
        statusEl.innerHTML = '<defs> <mask id="idleMask"> <circle cx="25" cy="25" r="12" stroke="#faa61a" stroke-width="2" fill="white" /> <circle cx="19" cy="20" r="8"  fill="black" /> </mask> </defs> <rect fill="#faa61a" width="100%" height="100%" mask="url(#idleMask)" />'
      }
      else{
        statusEl.innerHTML = '<circle cx="25" cy="25" r="12" fill="#747f8d" /> <circle cx="25" cy="25" r="6" fill="#3f434a" />'
      }
  }
  