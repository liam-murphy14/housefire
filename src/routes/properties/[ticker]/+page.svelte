<script lang="ts">
  import type { PageServerData } from './$types';
  import PropertiesMap from '$lib/components/PropertiesMap.svelte';
  export let data: PageServerData;
  const tableRows = data.properties.map((property) => {
    return {
      Name: property.name || property.address_1,
      City: property.city,
      State: property.state,
      Country: property.country,
      'Available Area': property.square_footage,
    };
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
          <PropertiesMap properties={data.properties} />
        </div>
      </div>
    </div>
    <div class="w-1/2 h-full overflow-auto">
      <table class="overflow-scroll border border-hf-grey rounded-lg">
        <thead>
          {#each Object.keys(tableRows[0]) as key}
            <th class="border border-hf-grey bg-hf-grey/30 p-2 hf-body-1-x text-hf-base-dark">
              {key}
            </th>
          {/each}
        </thead>
        <tbody>
          {#each tableRows as row}
            <tr
              class="border border-hf-grey hover:bg-hf-blue/30 transition-colors duration-300 ease-out cursor-pointer"
            >
              {#each Object.values(row) as value}
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
