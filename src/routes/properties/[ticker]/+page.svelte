<script lang="ts">
  import type { PageServerData } from './$types';
  import { page } from '$app/stores';
  import PropertiesMap from '$lib/components/PropertiesMap.svelte';
  export let data: PageServerData;
  const tableRows = data.properties.map((property) => {
    return {
      Name: property.name || property.address_1,
      City: property.city,
      State: property.state,
      Country: property.country,
      'Square Feet': property.square_footage,
    };
  });
</script>

<div class="p-6">
  <h1 class="text-hf-base-dark hf-heading-3">
    {$page.params.ticker} Properties
  </h1>
  <PropertiesMap />
  <table class="mt-4 border border-hf-grey rounded-lg">
    <thead>
      {#each Object.keys(tableRows[0]) as key}
        <th class="border border-hf-grey bg-hf-grey/30 p-2 hf-body-1-x text-hf-base-dark">
          {key}
        </th>
      {/each}
    </thead>
    <tbody>
      {#each tableRows as row}
        <tr class="border border-hf-grey">
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
