import { AJAX, generatePaginationButton, getSearchResultsPage, state, icons } from './config.js';

const API_URL = '/get-working-time-data';
const timetableBody = document.getElementById('timetable-body');
const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const shifts = ["Morning", "Afternoon", "Evening", "Night"]; 
const paginationButton = document.querySelector('.pagination');

//create function to get data from 'employee' document
const getData = async function(uploadData) {
    try {
      const data = await AJAX(API_URL, uploadData);
      state.data = data;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
};

function render(markup) {
    timetableBody.innerHTML += markup;
}

const today = new Date();
const currentDate = today.getDate();
const currentMonth = today.getMonth();
const currentYear = today.getFullYear();
let markup = '';

//get data and fill them into the table
getData({month: currentMonth, year: currentYear});
state.data.forEach( (doc) => {
    const row = `
        <tr>
            <td class="employee_working_tr">${doc['Check_in_time']}</td>
            <td class="employee_working_tr">${doc['Check_in time']}</td>
            <td class="employee_working_tr">${doc['Check_out time']}</td>
            <td class="employee_working_tr">${doc['Status']}</td>
        </tr>
    `;
    markup += row;
});

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

//add event when document is loaded
document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('#confirm_working_time');
    const confirmationModal = document.getElementById('confirmationModal');
    const confirmBtn = document.getElementById('confirmBtn');
    const cancelBtn = document.getElementsByClassName('cancelBtn');

    function hideModals() {
        confirmationModal.classList.add('hidden');
    }

    function showConfirmationModal(message) {
        document.getElementById('modalMessage').textContent = message;
        confirmationModal.classList.remove('hidden');
    }

    button.addEventListener('click', () => {
        showConfirmationModal('Are you sure?');
    });

    // Add event listeners to close the modal when clicking outside of it
    confirmationModal.addEventListener('click', (event) => {
    if (event.target === confirmationModal) {
        hideModals();
    }
    });

    confirmBtn.addEventListener('click', () => {
        hideModals();
    });

    // Convert HTMLCollection to an array
    Array.from(cancelBtn).forEach(btn => {
        btn.addEventListener('click', () => {
            hideModals();
        });
    });
})
