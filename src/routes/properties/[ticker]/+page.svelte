<script lang="ts">
  import type { PageServerData } from './$types';
  import 'leaflet/dist/leaflet.css';
  import 'leaflet/dist/images/layers.png';
  import 'leaflet/dist/images/layers-2x.png';
  import 'leaflet/dist/images/marker-icon.png';
  import 'leaflet/dist/images/marker-icon-2x.png';
  import 'leaflet/dist/images/marker-shadow.png';
  import { onMount } from 'svelte';
  import type { PropertyData } from '$lib/interfaces/PropertyData.interface';
  import SortableTable from '$lib/components/SortableTable.svelte';

  type PropertyWithMarker = {
    marker: L.Marker;
  } & PropertyData;
  export let data: PageServerData;

  let L: typeof import('leaflet');
  let map: L.Map;
  let joinedPropertyData: PropertyWithMarker[] = [];

  // FUNCTIONS FOR LEAFLET
  const addPropertyMarker = (property: PropertyData) => {
    const lat = property.latitude ?? 0;
    const lng = property.longitude ?? 0;
    const marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup(`<b>${property.name}</b><br>${property.address_1}`);
    return marker;
  };

  const focusProperty = (tableRowData: PropertyWithMarker) => {
    const lat = tableRowData.latitude ?? 0;
    const lng = tableRowData.longitude ?? 0;
    map.flyTo([lat, lng], 13);
    tableRowData.marker.openPopup();
  };

  onMount(async () => {
    try {
      // import leaflet
      const l = await import('leaflet');
      L = l.default;

      // initialize map
      map = L.map('map').setView([39, -98], 3);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);

      // add markers for now just first 10
      joinedPropertyData = data.properties.map((property) => {
        return {
          ...(property ?? {}),
          marker: addPropertyMarker(property),
        };
      });
    } catch (e) {
      console.error(e);
    }
  });
</script>

<div class="p-6 overflow-auto h-full">
  <div class="flex w-full h-full overflow-auto gap-4">
    <div class="w-1/2 h-full flex flex-col">
      <h1 class="text-hf-base-dark hf-heading-3">
        {data.ticker} Properties
      </h1>
      <div class="flex-grow w-full flex items-center">
        <div class="flex-grow w-full">
          <div id="map" />
        </div>
      </div>
    </div>
    <div class="w-1/2 h-full overflow-auto">
      <!-- TODO: add better sort function for square feet -->
      <SortableTable
        idKey={'id'}
        tableHeaders={{
          name: 'Name',
          address_1: 'Address',
          city: 'City',
          state: 'State',
          square_footage: 'Available Area',
        }}
        tableData={joinedPropertyData}
        rowOnClick={focusProperty}
      />
    </div>
  </div>
</div>

<style lang="postcss">
  #map {
    @apply h-96;
  }
</style>
