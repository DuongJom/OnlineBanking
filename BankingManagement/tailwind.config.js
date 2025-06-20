/** @type {import('tailwindcss').Config} */

import withMT from "@material-tailwind/html/utils/withMT";

module.exports = withMT({
  content: [
    "./templates/*.html", 
    "./templates/**/*.html",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      colors:{
        'bg-color' : '#2C3244',
        'bg-color2' : "#323A4E",
        'hover-btn-bg-color' : '#D28FFF',
        'hover-profile-color' : '#C1C7C6',
        'popup-bg' : 'rgba(204, 204, 204, 0.5)',
        'popup-bg-hover' : 'rgba(204, 204, 204, 0.3)',
        'side_bar_bg' : '#634CB3',
        'hover_side_bar': '#8271C1',
      },
      height: {
        '90%' : '90%',
        '500': '500px',
        '610' : '609.59px'
      },
      width:{
        '500px' : '500px',
        '90%' : '90%',
        '99%' : '99%',
        '1330' : '1330px',
      },
      flex: {
        '2' : '2',
      },
      zIndex: {
        '1000': 1000,
      },
      screens: {
        'custom-max': { 'max': '800px' },
      },
      boxShadow: {
        'shadowRight': '4px 0 6px rgba(0, 0, 0, 0.3)', 
      },
      maxHeight: {
        '430': '430px',
        '490': '490px'
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
});

