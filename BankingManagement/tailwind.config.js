/** @type {import('tailwindcss').Config} */

import withMT from "@material-tailwind/html/utils/withMT";

module.exports = withMT({
  content: ["./templates/*.html", "./static/**/*.js"],
  theme: {
    extend: {
      colors:{
        'bg-color' : '#2C3244',
        'bg-color2' : "#323A4E",
        'hover-btn-bg-color' : '#D28FFF',
        'hover-profile-color' : '#C1C7C6',
      },
      height: {
        '90%' : '90%',
      },
      width:{
        '500px' : '500px',
        '90%' : '90%',
      },
      flex: {
        '2' : '2',
      },
      border: {
        '1' : '1',
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
});

