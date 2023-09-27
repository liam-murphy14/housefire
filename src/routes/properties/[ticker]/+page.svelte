<script lang="ts">
  import type { PageServerData } from './$types';
  import 'leaflet/dist/leaflet.css';
  import { onMount } from 'svelte';
  import {
    TABLE_HEADERS,
    type PropertyData,
    type PropertyTableRowData,
  } from '$lib/interfaces/PropertyData.interface';

  export let data: PageServerData;

  let L: typeof import('leaflet');
  let map: L.Map;
  let joinedPropertyData: {
    property: PropertyData;
    marker: L.Marker;
    tableRow: PropertyTableRowData;
  }[] = [];

  // FUNCTIONS FOR LEAFLET
  const addPropertyMarker = (property: PropertyData) => {
    const lat = property.latitude ?? 0;
    const lng = property.longitude ?? 0;
    const marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup(`<b>${property.name}</b><br>${property.address_1}`);
    return marker;
  };

  const focusProperty = (property: PropertyData, marker: L.Marker) => {
    const lat = property.latitude ?? 0;
    const lng = property.longitude ?? 0;
    map.flyTo([lat, lng], 13);
    marker.openPopup();
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
          property,
          marker: addPropertyMarker(property),
          tableRow: {
            Name: (property.name || property.address_1) ?? '',
            City: property.city ?? '',
            State: property.state ?? '',
            Country: property.country ?? '',
            'Available Area': property.square_footage ?? '',
          },
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
      <table class="overflow-scroll border border-hf-grey rounded-lg">
        <thead>
          {#each TABLE_HEADERS as key}
            <th class="border border-hf-grey bg-hf-grey/30 p-2 hf-body-1-x text-hf-base-dark">
              {key}
            </th>
          {/each}
        </thead>
        <tbody>
          {#each joinedPropertyData as { property, marker, tableRow }}
            <tr
              class="border border-hf-grey hover:bg-hf-blue/30 transition-colors duration-300 ease-out cursor-pointer"
              on:click={() => focusProperty(property, marker)}
            >
              {#each Object.values(tableRow) as value}
                <td class="border border-hf-grey p-2 hf-body-2 text-hf-base-dark">
                  {value}
                </td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>

<style lang="postcss">
  #map {
    @apply h-96;
  }
</style>
