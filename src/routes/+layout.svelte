<script>
	import '../app.postcss';
</script>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css?family=Poppins:100,200,300,400,500,600,700,800,900"
	/>
</svelte:head>

<div class="min-h-screen w-full -z-50 bg-hf-base-light">
	<h1
		class="sticky top-0 p-2 w-full border-b border-hf-grey text-hf-base-dark hf-body-2-x bg-hf-base-light"
	>
		Housefire
	</h1>
	<slot />
</div>
