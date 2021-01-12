var map;
var markers = [];
var addNodeState = false;
var srcState = true;
var srcNode;
var dstNode;
var graph = [];
var heuristicInfo = [];
var infinite = 0;
var nLabel = 0;
var polylines = [];
var geoConst = 1;

// inisialisasi google maps
function initMap() {
  // properti maps
  var mapProp = {
    center: new google.maps.LatLng(-6.8915, 107.6107),
    zoom: 18,
    disableDoubleClickZoom: true,
  };

  // konstruktor map
  map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

  // event handler click on map untuk menambahkan marker di lokasi click
  google.maps.event.addListener(map, "click", function (event) {
    placeMarker(event.latLng);
  });
}

// place marker on google maps
function placeMarker(location) {
  // konstruktor marker
  var marker = new google.maps.Marker({
    position: location,
    animation: google.maps.Animation.DROP,
    draggable: true,
    label: nLabel.toString(),
  });

  // marker ditambahkan ke peta dan ke array markers jika sedang dalam state add node
  if (addNodeState) {
    marker.setMap(map);
    markers.push(marker);
    nLabel++;
  }

  // event handler di marker untuk menambahkan edge line
  marker.addListener("click", function () {
    addEdge(this);
  });
}

// menentukan indeks marker yang dipilih berdasarkan array markers
function getMarkerIdx(position) {
  var idx = 0,
    found = false;
  while (idx < markers.length && !found) {
    curLat = markers[idx].getPosition().lat();
    curLng = markers[idx].getPosition().lng();
    refLat = position.lat();
    refLng = position.lng();
    if (curLat == refLat && curLng == refLng) {
      found = true;
    } else {
      idx++;
    }
  }
  return idx;
}

// menambahkan edge line dari dua markers
function addEdge(id) {
  if (!addNodeState) {
    if (srcState) {
      srcNode = id;
      srcState = false;
    } else {
      dstNode = id;
      srcState = true;

      // menggambar edge line
      var edgeLine = new google.maps.Polyline({
        path: [srcNode.getPosition(), dstNode.getPosition()],
        strokeColor: "black",
        strokeOpacity: 1,
        strokeWeight: 2,
      });

      edgeLine.setMap(map);
      console.log(edgeLine.getPath().getAt(0).lat());
      polylines.push(edgeLine);

      // assign bobot graph
      graph[getMarkerIdx(srcNode.getPosition())][
        getMarkerIdx(dstNode.getPosition())
      ] = calcDistance(srcNode.getPosition(), dstNode.getPosition());
      graph[getMarkerIdx(dstNode.getPosition())][
        getMarkerIdx(srcNode.getPosition())
      ] =
        graph[getMarkerIdx(srcNode.getPosition())][
          getMarkerIdx(dstNode.getPosition())
        ];
    }
  }
}

function runAStar() {
  document.getElementById("addEdgeBtn").disabled = true;
  $.ajax({
    url: "/runAStar",
    data: {
      graph: JSON.stringify(graph),
      heuristicInfo: JSON.stringify(heuristicInfo),
    },
    type: "POST",
    success: function (response) {
      var result = JSON.stringify(response);
      result = result.slice(1, result.length - 1).split(",");
      console.log(result);

      for (var i = 0; i < result.length - 1; i++) {
        var edgeLine = new google.maps.Polyline({
          path: [
            markers[parseInt(result[i])].getPosition(),
            markers[parseInt(result[i + 1])].getPosition(),
          ],
          strokeColor: "red",
          strokeOpacity: 1,
          strokeWeight: 4,
        });

        edgeLine.setMap(map);
      }
    },

    error: function (error) {
      console.log(error);
    },
  });
}

function calcHeuristicInfo(dstNode) {
  for (var i = 0; i < markers.length; i++) {
    heuristicInfo[i] = calcDistance(
      markers[i].getPosition(),
      dstNode.getPosition()
    );
  }
}

function rad(x) {
  return (x * Math.PI) / 180;
}

function calcDistance(p1, p2) {
  var R = 6378137; // jari-jari bumi dalam meter
  var dLat = rad(p2.lat() - p1.lat());
  var dLong = rad(p2.lng() - p1.lng());
  var a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(rad(p1.lat())) *
      Math.cos(rad(p2.lat())) *
      Math.sin(dLong / 2) *
      Math.sin(dLong / 2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  var d = R * c;
  return d; // satuan meter
}

document.getElementById("addNodeBtn").onclick = addNodeStateTrue;
function addNodeStateTrue() {
  addNodeState = true;
}

document.getElementById("addEdgeBtn").onclick = addNodeStateFalse;
function addNodeStateFalse() {
  addNodeState = false;

  // konstruktor graph
  graph = new Array(markers.length);
  for (var i = 0; i < markers.length; i++) {
    graph[i] = new Array(markers.length);
  }

  // inisialisasi graph
  for (var i = 0; i < markers.length; i++) {
    for (var j = 0; j < markers.length; j++) {
      graph[i][j] = infinite;
    }
  }
  document.getElementById("addNodeBtn").disabled = true;
  document.getElementById("runAStarBtn").disabled = false;

  // konstruktor dan inisialisasi heuristicInfo
  heuristicInfo = new Array(markers.length);
  for (var i = 0; i < markers.length; i++) {
    heuristicInfo[i] = 0;
  }

  // hitung heuristicInfo
  calcHeuristicInfo(markers[markers.length - 1]);
}

document.getElementById("runAStarBtn").onclick = runAStar;
