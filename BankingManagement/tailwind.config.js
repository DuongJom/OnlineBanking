/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      colors:{
        'bg-color' : '#2C3244',
        'bg-color2' : "#323A4E",
        'hover-btn-bg-color' : '#D28FFF'
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
}

