/** @type {import('tailwindcss').Config} */

import withMT from "@material-tailwind/html/utils/withMT";

module.exports = withMT({
  content: ["./templates/*.html", "./static/**/*.js"],
  theme: {
    extend: {
      colors:{
        'bg-color' : '#2C3244',
        'bg-color2' : "#323A4E",
        'hover-btn-bg-color' : '#D28FFF'
      },
      width:{
        '500px' : '500px',
        '90%' : '90%',
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
});

