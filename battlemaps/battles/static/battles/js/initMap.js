async function initMap() {
  // Hastings UK
  const position = { lat: 50.8552, lng: 0.5729 }

  const { Map } = await google.maps.importLibrary("maps")

  // The map, centered at Hastings
  const map = new Map(document.getElementById("map"), {
    zoom: 10,
    center: position,
  })

  map.addListener('click', e => {
    const latLngJson = e.latLng.toJSON()
    const lat = latLngJson.lat
    const lng = latLngJson.lng
    fetch(`/battles/?point=${lat},${lng}`)
      .then(res => res.json())
      .then(data => {
        console.log(data["results"][0].name)
      })
  })
}

export default initMap