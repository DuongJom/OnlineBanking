import { AJAX, generatePaginationButton, getSearchResultsPage, state, icons } from './config.js';


const timetableBody = document.getElementById('timetable-body');
const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const shifts = ["Morning", "Afternoon", "Evening", "Night"]; 
const paginationButton = document.querySelector('.pagination');

function render(markup) {
    timetableBody.innerHTML += markup;
}
const currentDate = new Date();
const currentMonth = currentDate.getMonth();
const currentYear = currentDate.getFullYear();
let markup = '';
const data = [];
// Get the number of days in the current month
const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(currentYear, currentMonth, day);
    const dayOfWeek = daysOfWeek[date.getDay()];

    // Example shift assignment, can be customized
    const shift = shifts[Math.floor(Math.random() * shifts.length)];

    const row = `
        <tr>
            <td class="tb_row">${day}</td>
            <td class="tb_row">${dayOfWeek}</td>
            <td class="tb_row">${shift}</td>
        </tr>
    `;
    data.push(row);
    markup += row;
}
state.data = data;
getSearchResultsPage().forEach( e => render(e));
controlPagination();

function controlPagination(page) {
    timetableBody.innerHTML='';
    getSearchResultsPage(page).forEach( e => render(e));
    const markup = generatePaginationButton(icons);
    paginationButton.innerHTML='';
    paginationButton.insertAdjacentHTML('afterbegin', markup);
  } 

paginationButton.addEventListener('click', function (e) {
    const btn = e.target.closest('.btn--inline');
    if (!btn) return;
  
    const goToPage = +btn.dataset.goto;
    controlPagination(goToPage);
  });


