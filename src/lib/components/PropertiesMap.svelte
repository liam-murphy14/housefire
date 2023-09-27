<script lang="ts">
  import type { PropertyData } from '$lib/interfaces/PropertyData.interface';
  import 'leaflet/dist/leaflet.css';
  import { onMount } from 'svelte';

  export let properties: PropertyData[] = [];

  onMount(async () => {
    try {
      // import leaflet
      const l = await import('leaflet');
      const L = l.default;

      // initialize map
      const map = L.map('map').setView([39, -98], 3);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);

      // FUNCTIONS FOR LEAFLET
      const addPropertyMarker = (property: PropertyData) => {
        const lat = property.latitude ?? 0;
        const lng = property.longitude ?? 0;
        const marker = L.marker([lat, lng]).addTo(map);
        marker.bindPopup(`<b>${property.name}</b><br>${property.address_1}`);
      };

      // add markers for now just first 10
      properties.forEach((property) => {
        addPropertyMarker(property);
      });
    } catch (e) {
      console.log(e);
    }
  });
</script>

<div id="map" />

<style lang="postcss">
  #map {
    @apply h-96;
  }
</style>
