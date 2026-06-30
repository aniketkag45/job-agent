/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['Playfair Display', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        cream: '#F8F4F1',
        navy: {
          DEFAULT: '#14213D',
          light: '#101B43',
        },
        body: '#667085',
        border: '#E5DDD7',
        accent: {
          orange: '#E97B42',
          purple: '#A855F7',
        },
        card: {
          lavender: '#F6EEF8',
          peach: '#FFF1E8',
          blue: '#EEF5FF',
        },
      },
    },
  },
  plugins: [],
}