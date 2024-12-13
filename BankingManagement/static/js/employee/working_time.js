import { AJAX, generatePaginationButton, getSearchResultsPage, state, icons } from './config.js';

const API_URL = '/get-working-time-data';
const timetableBody = document.getElementById('timetable-body');

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
            <td class="employee_working_tr">${doc['Check_in_time']}</td>
            <td class="employee_working_tr">${doc['Check_out_time']}</td>
            <td class="employee_working_tr">${doc['Working_status']}</td>
        </tr>
    `;
    markup += row;
});

render(markup);

//add event when document is loaded
document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('#confirm_working_time');
    const confirmationModal = document.getElementById('confirmationModal');
    const confirmBtn = document.getElementById('confirmBtn');
    const cancelBtn = document.getElementsByClassName('cancelBtn');

    //hide models
    function hideModals() {
        confirmationModal.classList.add('hidden');
    }

    //load data from the server for the one who log in


    // show confirmation btn
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
