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
        '350px' : '300px',
        '150px' : '150px'
      },
      colors: {
        'btn_color' : '#45942E'
      }
    },
  },
  plugins: [],
}

