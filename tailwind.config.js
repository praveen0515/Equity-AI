/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0e17',
        surface: '#111827',
        primary: '#3b82f6',
        accent: '#06b6d4',
      },
    },
  },
  plugins: [],
}
