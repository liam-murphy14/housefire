/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				'hf-base-light': '#FAF9F6',
				'hf-base-dark': '#121212',
				'hf-orange': '#FFC299',
				'hf-blue': '#C6DEFF',
				'hf-grey': '#E6E6E6',
				'hf-navy': '#346392'
			}
		}
	},
	plugins: []
};
