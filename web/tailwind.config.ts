import type { Config } from 'tailwindcss'

const config: Config = {
	content: [
		'./app.vue',
		'./components/**/*.{vue,js,ts}',
		'./layouts/**/*.vue',
		'./layout/**/*.vue',
		'./pages/**/*.vue',
		'./plugins/**/*.{js,ts}',
		'./nuxt.config.{js,ts}',
		'./**/*.{vue,js,ts,html}'
	],
	theme: {
		extend: {
			colors: {
			},
		},
	},
	plugins: [],
}

export default config


