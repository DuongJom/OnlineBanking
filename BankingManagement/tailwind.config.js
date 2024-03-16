/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      height: {
        '500px': '500px',
      },
      width: {
        '500px' : '500px',
      },
      colors: {
        'btn_color' : '#A1FB8E'
      }
    },
  },
  plugins: [],
}

