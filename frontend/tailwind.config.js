/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        doh: {
          emerald: '#056247',
          emeraldDark: '#033f2e',
          emeraldLight: '#0d8562',
          gold: '#c59b27',
          goldLight: '#e4bd4d',
          sand: '#fbf9f4',
          slate: '#1e293b',
        }
      }
    },
  },
  plugins: [],
}
