'strict mode'
import { AJAX, icons, generatePaginationButton, state, getSearchResultsPage} from './config.js';
const API_URL = '/get-data';

const paginationButton = document.querySelector('.pagination');

//add event when document is loaded
document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('#buttonContainer .action-btn');
  const confirmationModal = document.getElementById('confirmationModal');
  const confirmBtn = document.getElementById('confirmBtn');
  const cancelBtn = document.getElementsByClassName('cancelBtn');
  const dayOffModal = document.getElementById('dayOffModal');
  const halfDayBtn = document.getElementById('halfDayBtn');
  const wholeDayBtn = document.getElementById('wholeDayBtn');

  let activeButton = null;

  function showConfirmationModal(message) {
      document.getElementById('modalMessage').textContent = message;
      confirmationModal.classList.remove('hidden');
  }

  function hideModals() {
      confirmationModal.classList.add('hidden');
      dayOffModal.classList.add('hidden');
  }

  function disableOtherButtons(...exceptIds) {
    // Iterate over each button
    buttons.forEach(button => {
        // If the button's ID is not in the exceptIds array, disable it
        if (!exceptIds.includes(button.id)) {
            button.disabled = true;
        } else {
            // Ensure the button with exceptId is not disabled
            button.disabled = false;
        }
    });
  }


  function enableAllButtons() {
      buttons.forEach(button => {
          button.disabled = false;
      });
  }

  buttons.forEach(button => {
      button.addEventListener('click', () => {
          activeButton = button;
          if (button.id === 'day_off') {
              dayOffModal.classList.remove('hidden');
          } else {
              showConfirmationModal(`Confirm ${button.textContent}?`);
          }
      });
  });

  confirmBtn.addEventListener('click', () => {
      if (activeButton.id === 'check_in') {
        disableOtherButtons(activeButton.id, 'check_out');
      } 
      else if (activeButton.id === 'wfh_check_in'){
        disableOtherButtons(activeButton.id, 'wfh_check_out');
      }
      else if (activeButton.id === 'check_out' || activeButton.id === 'wfh_check_out') {
        enableAllButtons();
      }
      hideModals();
  });

  // Convert HTMLCollection to an array
  Array.from(cancelBtn).forEach(btn => {
    btn.addEventListener('click', () => {
        hideModals();
    });
  });

  halfDayBtn.addEventListener('click', () => {
      disableOtherButtons('day_off');
      hideModals();
  });

  wholeDayBtn.addEventListener('click', () => {
      disableOtherButtons('day_off');
      hideModals();
  });
   // Add event listeners to close the modal when clicking outside of it
   confirmationModal.addEventListener('click', (event) => {
    if (event.target === confirmationModal) {
        hideModals();
    }
  });

  dayOffModal.addEventListener('click', (event) => {
      if (event.target === dayOffModal) {
          hideModals();
      }
  });
});


const month = document.getElementById('month');
const year = document.getElementById('year');

//render table
const render = function(data){
  // Clear existing rows
  const tbody = document.querySelector('#employee-table');
  tbody.innerHTML = '';

  // Populate table with fetched data
  data.forEach((row) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
      <td class="text-center employee_tr">${row["STT"]}</td>
      <td class="employee_tr">${row["_id"]}</td>
      <td class="employee_tr">${row["Employee Name"]}</td>
      <td class="employee_tr">${row["Role"]}</td>
      <td class="employee_tr">${row["Gender"]}</td>
      <td class="employee_tr">${row["Employee Position"]}</td>
      <td class="employee_tr">${row["Employee Phone"]}</td>
      <td class="employee_tr">${row["Employee Email"]}</td>
      <td class="employee_tr">${row["Employee Address"]}</td>
      <td class="hidden lg:table-cell text-center employee_tr">${row["Check-in time"]}</td>
      <td class="hidden lg:table-cell text-center employee_tr">${row["Check-out time"]}</td>
      <td class="hidden xl:table-cell employee_tr">${row["Status"]}</td>
      `;
      tbody.appendChild(tr);
  })
};

// Asynchronous data fetching function
const getData = async function(uploadData) {
  try {
    const data = await AJAX(API_URL, uploadData);
    state.data = data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

// Event listener for month change
month.addEventListener('change', async function(e) {
  e.preventDefault();
  const uploadData = { month: month.value, year: year.value };
  await getData(uploadData);
  controlPagination();
});

// Event listener for year change
year.addEventListener('change', function(e) {
  e.preventDefault();
  const uploadData = { month: month.value, year: year.value };
  getData(uploadData);
  controlPagination();
});

// Render data when the document is loaded
document.addEventListener('DOMContentLoaded', function (){
  const data = JSON.parse(document.querySelector('#flask-data').textContent)
  state.data = data.sort((a,b) => a.STT - b.STT);;
  controlPagination();
  
});

//control pagination
function controlPagination(page=1) {
  render(getSearchResultsPage(page));
  const markup = generatePaginationButton(icons);
  paginationButton.innerHTML='';
  paginationButton.insertAdjacentHTML('afterbegin', markup);
} 

//pagination
paginationButton.addEventListener('click', function (e) {
  const btn = e.target.closest('.btn--inline');
  if (!btn) return;

  const goToPage = +btn.dataset.goto;
  controlPagination(goToPage);
});




