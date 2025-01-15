// Declare arrays to hold groups of markers and windows so that they can be removed when the user's query changes. userLocationMarkers is for
// the user's location marker, battleMarkers is for the battle location markers, and battleWindows is for the battle info windows.
const battleMarkers = [];
const userLocationMarkers = [];
const battleWindows = [];

function initMap() {

//  Declare firstQuery variable so that the "next ten nearest battles" button can appear if not the first query.
  let firstQuery = true;

// The request iteration variable will be used to keep track of how many times the user has requested 'ten more battles'.
  let requestIteration;

//  Instantiates the map object before any input is given - so it is zoomed out with the entire world in view.
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 25, lng: -60 },
    zoom: 4,
    gestureHandling: "greedy",
    minZoom: 2,
  });

// Instantiates the autocomplete object which is attached to the search box in the navbar on the html template.
  const input = document.getElementById("auto-complete");
  const autocomplete = new google.maps.places.Autocomplete(input, {
    fields: ["place_id", "geometry", "name", "formatted_address"],
  });
  autocomplete.bindTo("bounds", map);
  google.maps.event.addDomListener(input, 'keydown', (event) => {
    if (event.keyCode === 13) {
      event.preventDefault();
    }
  });

// Instantiates the Geocoder and InfoWindow objects
  const geocoder = new google.maps.Geocoder();
  const userLocationInfoWindow = new google.maps.InfoWindow();

// Creates button on map for user to pan to current location
  const locationButton = document.createElement("button");
  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

// Sets event listener so that when user clicks on pan to current location button, the user's coordinates will
// be retrieved and a marker will be placed at their location.
  locationButton.addEventListener("click", () => {
    requestIteration = 1;

    if (userLocationMarkers.length > 0) {
      removeMarkers(userLocationMarkers);
    }

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {

          if (document.getElementById("ten-more-button")) {
            document.getElementById("ten-more-button").remove();
          }

          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };

//          The fetch battles function is called here so that nearby battles are called and markers are placed
//          for each battle when the user wants to pan to their location. The request iteration number is also increased
//          by one so that the user can call the next ten battles by clicking on the ten more battles button.
          fetchNearbyBattles(pos.lat, pos.lng, map, requestIteration);

          requestIteration++;

          const tenMoreBattlesButton = document.createElement("button");
          tenMoreBattlesButton.textContent = "Next ten nearest battles";
          tenMoreBattlesButton.classList.add("custom-map-control-button");
          tenMoreBattlesButton.setAttribute("id", "ten-more-button")
          map.controls[google.maps.ControlPosition.TOP_CENTER].push(tenMoreBattlesButton);

          tenMoreBattlesButton.addEventListener("click", () => {
            fetchNearbyBattles(pos.lat, pos.lng, map, requestIteration);
            requestIteration++;
          });

//          map.setCenter(pos);
          const userMarker = new google.maps.Marker({
            position: { lat: pos.lat, lng: pos.lng },
            map,
          });
          userLocationMarkers.push(userMarker);
//          map.setZoom(9);
        },
        () => {
          handleLocationError(true, userLocationInfoWindow, map.getCenter(), map);
        }
      );
    } else {
      handleLocationError(false, userLocationInfoWindow, map.getCenter(), map);
    }
  });

// The autocomplete event listener listens for a new place input in the autocomplete search box. Once input, the fetch
// battles function is called so that the battles nearest the input location are shown on the map.
  autocomplete.addListener("place_changed", () => {
    requestIteration = 1;

    if (userLocationMarkers.length > 0) {
      removeMarkers(userLocationMarkers);
    }

    const place = autocomplete.getPlace();

    if (!place.place_id) {
      return;
    }

    geocoder
      .geocode({ placeId: place.place_id })
      .then(({ results }) => {

        if (document.getElementById("ten-more-button")) {
          document.getElementById("ten-more-button").remove();
        }

//        map.setZoom(9);
//        map.setCenter(results[0].geometry.location);

        const marker = new google.maps.Marker({ map: map });

        marker.setPlace({
          placeId: place.place_id,
          location: results[0].geometry.location,
        });

        userLocationMarkers.push(marker);

        const targetLatLng = results[0].geometry.location.toJSON()
        const targetLat = targetLatLng.lat;
        const targetLng = targetLatLng.lng;

        const coordinates = {
          targetLat : targetLat,
          targetLng : targetLng,
        };

//      Once the fetch battles function is called, the number of request iterations is increased by one, so that
//      ten more battles may be queried by clicking on the ten more battles button.
        fetchNearbyBattles(coordinates.targetLat, coordinates.targetLng, map, requestIteration);

        requestIteration++;

        const tenMoreBattlesButton = document.createElement("button");
        tenMoreBattlesButton.textContent = "Next ten nearest battles";
        tenMoreBattlesButton.classList.add("custom-map-control-button");
        tenMoreBattlesButton.setAttribute("id", "ten-more-button")
        map.controls[google.maps.ControlPosition.TOP_CENTER].push(tenMoreBattlesButton);

        tenMoreBattlesButton.addEventListener("click", () => {
          fetchNearbyBattles(coordinates.targetLat, coordinates.targetLng, map, requestIteration)
          requestIteration++;
        });
      });
  });
}


// Function to handle if the user attempts to pan to current location but their browser doesn't support geolocation.
function handleLocationError(browserHasGeolocation, userLocationInfoWindow, pos, map) {
  userLocationInfoWindow.setPosition(pos);
  userLocationInfoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  userLocationInfoWindow.open(map);
}


// The fetch battles function fetches the nearest battles via the get_battles view in the Django 'battles' app.
// The user's queried latitude and longitude (whether from pan to current location, or from the autocomplete search
// box) are passed in as arguments, and a JSON string of ten battles with each battle's coordinates and information
// are returned. Customized markers are then placed at each battle location, and InfoWindows are shown once the
// markers are clicked on.
function fetchNearbyBattles(queryLat, queryLng, map, iteration) {
// Length of marker array checked to see if battle markers are currently open on the map. If so, they are removed,
// and a new set of ten markers will be placed.
  if (battleMarkers.length > 0) {
    removeMarkers(battleMarkers);
  }
  fetch('getbattles/' + queryLat + '/' + queryLng + '/' + iteration, {
    headers: {
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then(response => response.json())
    .then(battleCoordinateData => {
      console.log('Success:', battleCoordinateData);

      const newBounds = findMapBounds(battleCoordinateData);
      let north = newBounds.north;
      let south = newBounds.south;
      let east = newBounds.east;
      let west = newBounds.west;

      map.fitBounds({north: north, south: south, east: east, west: west});

      for (let i = 0; i < battleCoordinateData.length; i++) {

        const latitude = battleCoordinateData[i].latitude;
        const longitude = battleCoordinateData[i].longitude;

        const latLng = new google.maps.LatLng(latitude, longitude);

        const contentString =
          '<div id="content">' +
          '<div id="siteNotice">' +
          '</div>' +
          '<h5 id="firstHeading" class="firstHeading">' + battleCoordinateData[i].name + '</h5>' +
          '<div id="bodyContent">' +
          '<p><b>Date: </b>' + battleCoordinateData[i].date + '</p>' +
          '<p><b>Coordinates: </b>' + battleCoordinateData[i].latitude + ', ' + battleCoordinateData[i].longitude + '</p>' +
          '<p><b>Wikipedia link: </b><a href="' + battleCoordinateData[i].url + '">' + battleCoordinateData[i].url + '</a></p>' +
          '</div>' +
          '</div>';
        const battleInfoWindow = new google.maps.InfoWindow({
          content: contentString,
        });

        battleWindows.push(battleInfoWindow);

//      The battle markers are given a custom sword image to fit the warlike theme.
        const iconImage = {
          url: 'static/maps/icons/swords.png',
          size: new google.maps.Size(35, 35),
          anchor: new google.maps.Point(17, 17),
        }

        const marker = new google.maps.Marker({
          position: latLng,
          map: map,
          title: battleCoordinateData[i].name,
          icon: iconImage,
        });

        battleMarkers.push(marker);

//      Once a battle marker is clicked on, any other info windows currently open will be closed.
        marker.addListener('click', () => {
          closeWindows(battleWindows);
          battleInfoWindow.open({
            anchor: marker,
            map,
            shouldFocus: false,
          });
        });
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// This function removes markers provided inside of a given array, by setting each marker to null, and setting the
// array length to zero so that all references to said markers are removed.
function removeMarkers(markerArray) {
  for (let i = 0; i < markerArray.length; i++) {
    markerArray[i].setMap(null);
  }
  markerArray.length = 0;
}

// This function closes all info windows currently open so that only one info window is open at a time.
function closeWindows(infoWindowArray) {
  for (let i = 0; i < infoWindowArray.length; i++) {
    infoWindowArray[i].close();
  }
}

// findMapBounds takes an array of objects (each with latitude and longitude attributes) and finds the furthest east,
// west, south and north so that these points can be set as the bounds of where the map should pan to once the
// ten nearest battles are displayed.
function findMapBounds(battleData) {
  let maxLat = -90;
  let minLat = 90;
  let maxLng = -180;
  let minLng = 180;

  for (let i = 0; i < battleData.length; i++) {
    const userLat = parseFloat(battleData[i].latitude);
    const userLng = parseFloat(battleData[i].longitude);

    if (userLat > maxLat) {
      maxLat = userLat;
    }

    if (userLat < minLat) {
      minLat = userLat;
    }

    if (userLng > maxLng) {
      maxLng = userLng;
    }

    if (userLng < minLng) {
      minLng = userLng;
    }

  }

//  If the min and max longitude bounds are set near the International Date Line,
//  the for loop runs again but this time seeks to set the lowest longitude value as the east bound,
//  and the highest as the west bound.

  const longitudeDifference = maxLng - minLng;

  if (longitudeDifference > 180) {

    maxLng = -180;
    minLng = 180;

    for (let i = 0; i < battleData.length; i++) {
      const userLng = parseFloat(battleData[i].longitude);
      if (userLng > maxLng && userLng < 0) {
        maxLng = userLng;
      }
      if (userLng < minLng && userLng > 0) {
        minLng = userLng;
      }
    }
  }

  const bounds = {
    north: maxLat,
    south: minLat,
    east: maxLng,
    west: minLng,
  };

  return bounds;
}


window.initMap = initMap;