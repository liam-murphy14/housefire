<script lang="ts">
  let L;

  const startMap = async () => {
    try {
      // @ts-ignore
      L = window.L;
      // @ts-ignore
      const map = L.map('map').setView([51.505, -0.09], 13);
      // @ts-ignore
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);
    } catch (e) {
      console.log(e);
    }
  };
</script>

<svlete:head>
  <link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""
  />
  <script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""
    on:load={startMap}
  ></script>
</svlete:head>
<div id="map" class="h-72" />
