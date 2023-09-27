<script>
  import '../app.postcss';
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css?family=Poppins:100,200,300,400,500,600,700,800,900"
  />
</svelte:head>

<div class="h-screen w-screen -z-50 bg-hf-base-light overflow-auto flex flex-col">
  <h1
    class="sticky top-0 p-2 w-full border-b border-hf-grey text-hf-base-dark hf-body-2-x bg-hf-base-light flex-shrink-0"
  >
    Housefire
  </h1>
  <div class="overflow-auto">
    <slot />
  </div>
</div>
