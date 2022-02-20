let shortestPath = [];
let stations = [];
const links = document.getElementById("stns_icons");

function markShortestPath(path) {
  for (let i = 0; i < path.length; i++) {
    let station = document.getElementById(path[i]);
    station.setAttribute('r', 5);
    station.setAttribute('fill', "#00FFFF");
  }
}

function getRequest(url) {
  let request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.send()
  request.onload = function() {
    if (this.status >= 200 && this.status < 400) {
      const response = JSON.parse(this.response);
      const total_time = response.total_time;
      shortestPath = response["route"];
      markShortestPath(shortestPath)

      modal.querySelector(".modal-content").innerHTML = `
      <p> 
        <strong>Tempo total:</strong> 
        <p> ${total_time} </p>
      </p>
      `;
      modal.style.display = "block";
      window.setTimeout(function() {
          modal.style.display = "none";
      }, 3000);
    }
  }
}

links.addEventListener('click', function(event) {
  let station = event.target.id;
  if (stations.length == 0) {
    event.target.setAttribute('fill', "#FF0000");
    stations.push(station);
  }
  else if (stations.length >= 1) {
    event.target.setAttribute('fill', "#00FF00");
    stations.push(station);
    if (stations.length > 2) {
      stations = [stations[0], station];
      reset(event, false);
    }
    const [ start, end ] = stations;
    getRequest(`/api/v1/?start=${start}&end=${end}`);
  } 
  event.preventDefault();
});

function reset(event, clean = true) {
  if (clean) {
    stations = [];
    shortestPath = [];
  }
  const allStations = document.querySelectorAll("circle");
  for (let i = 0; i < allStations.length; i++) {
    let station = allStations[i];
    station.setAttribute('r', 3);
    station.setAttribute('fill', "#FFFFFF");
  }
  event.preventDefault();
}
