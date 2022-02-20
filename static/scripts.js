let shortestPath = [];
let stations = [];
const links = document.getElementById("stns_icons");

// helper function to mark each stations on the shortest path with bigger Cyan circle
function markShortestPath(path) {
  for (let i = 0; i < path.length; i++) {
    let station = document.getElementById(path[i]);
    let radius = parseFloat(station.getAttribute('r')) + 2;
    station.setAttribute('r', radius);
    station.setAttribute('fill', "#00FFFF");
  }
}

// ajax get request function (works for IE10+)
function getRequest(url) {
  let request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.send()
  request.onload = function() {
    if (this.status >= 200 && this.status < 400) {
      shortestPath = JSON.parse(this.response)['route']
      markShortestPath(shortestPath)
    }
  }
}

links.addEventListener('click', function(event) {
  let station = event.target.id;
  if (stations.length == 0) {
    event.target.setAttribute('fill', "#FF0000");
    stations.push(station);
  }
  else if (stations.length == 1) {
    event.target.setAttribute('fill', "#00FF00");
    stations.push(station);
    const [ start, end ] = stations;
    getRequest(`/api/v1/?start=${start}&end=${end}`);
  }
  event.preventDefault();
});

// helper function to reset the color of each station
function reset(e) {
    for (let i = 0; i < stations.length; i++) {
      document.getElementById(stations[i]).setAttribute('fill', "#FFFFFF");
    }
    stations = [];
    if (shortestPath != []) {
      for (let i = 0; i < shortestPath.length; i++) {
        let station = document.getElementById(shortestPath[i]);
        let radius = parseFloat(station.getAttribute('r')) - 2;
        station.setAttribute('r', radius);
        station.setAttribute('fill', "#FFFFFF");
      }
      shortestPath = [];
    }
    e.preventDefault();
}

// Doubleclick to reset the station selection
let tapped = false;
document.addEventListener('dblclick', reset);
document.addEventListener('touchstart', function(e) {
    if(!tapped){
      tapped = setTimeout(function(){ tapped = false; }, 300);
    }
    else {    //tapped within 300ms of last tap. double tap
      clearTimeout(tapped);
      tapped=false;
      reset(e);
    }
});