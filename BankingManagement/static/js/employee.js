'strict mode'

import {TIMEOUT_SEC} from './config.js'
const API_URL = '/get-data'

const checkIn = document.getElementById('check_in');
const checkOut = document.getElementById('check_out');
const wfhCheckIn = document.getElementById('wfh_check_in');
const wfhCheckOut = document.getElementById('wfh_check_out');
const dayOff = document.getElementById('day_off');
const closeModalButton = document.getElementById('closeModal');
const modal = document.getElementById('myModal');
const modalMessage = document.getElementById('modalMessage');
const confirmButton = document.querySelector('.confirm');
const buttons = document.querySelectorAll('.action-btn');
        
// Function to disable all buttons except the one that was clicked
function disableButton(button) {
            button.disabled = true;
}


// Event handler for button clicks using event delegation
document.getElementById('buttonContainer').addEventListener('click', function(event) {

  if (event.target.tagName === 'BUTTON') {
    // Set the modal message based on the button clicked
    const buttonText = event.target.textContent;
    modalMessage.textContent = `Do you confirm to ${buttonText.toLowerCase()}?`;
    if (event.target.id === 'check_in') {
      //show model
      modal.classList.toggle('hidden');

      disableButton(wfhCheckIn);
      disableButton(wfhCheckOut);
      disableButton(dayOff);
    }
    if (event.target.id === 'wfh_check_in') {
      //show model
      modal.classList.toggle('hidden');

      disableButton(checkIn);
      disableButton(checkOut);
      disableButton(dayOff);
    }
    if (event.target.id === 'check_out') {
      //show model
      modal.classList.toggle('hidden');

      //reactivate buttons
      buttons.forEach(button => {
        button.disabled = false;
      });
    }
    if (event.target.id === 'wfh_check_out') {
      //show model
      modal.classList.toggle('hidden');

      //reactivate buttons
      buttons.forEach(button => {
        button.disabled = false;
      });
    }
    if (event.target.id === 'day_off') {
      //show model
      modal.classList.toggle('hidden');
      const text = `Would you like to take half-day off or 1 day off?`
      modalMessage.textContent = text;
      confirmButton.textContent = '1 day';
      closeModalButton.textContent = 'Half-day'
      //reactivate buttons
      buttons.forEach(button => {
        button.disabled = false;
      });
    }



      console.log('Button clicked:', event.target);
  }
});

// Event listener for closing the modal
closeModalButton.addEventListener('click', () => {
    modal.classList.toggle('hidden');

    if (closeModalButton.textContent === '1 day') {
      closeModalButton.textContent = 'Close';
      
      buttons.forEach(button => {
        button.disabled = true;
      });
      
      setTimeout(() => {
        buttons.forEach(button => {
          button.disabled = false; // Re-enable buttons after 1 day
        });
      }, 86400*500); 
    }
    
    // Re-enable all buttons when the modal is closed
    buttons.forEach(button => {
        button.disabled = true;
    });
});

confirmButton.addEventListener('click', (e) => {
    modal.classList.toggle('hidden');
    if (confirmButton.textContent === '1 day') {
      confirmButton.textContent = 'Confirm';

      buttons.forEach(button => {
        button.disabled = true;
      });
    
      setTimeout(() => {
        buttons.forEach(button => {
          button.disabled = false; // Re-enable buttons after 1 day
        });
      }, 86400*1000); 
    }
    console.log(e.target)
});

// Close modal when clicking outside the modal content
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.classList.toggle('hidden');
        // Re-enable all buttons when the modal is closed
        buttons.forEach(button => {
            button.disabled = false;
        });
    }
});







const timeout = function (s) {
  return new Promise(function (_, reject) {
    setTimeout(function () {
      reject(new Error(`Request took too long! Timeout after ${s} second`));
    }, s * 1000);
  });
};
// get the csrf token
const getCSRFToken = () => {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
};

const AJAX = async function (url, uploadData = undefined) {
  try {
    const csrfToken = getCSRFToken();
    // include the csrf token in the headers for fetch()
    const fetchPro = uploadData
      ? fetch(url, {
        "method": "POST",
        "headers": {"Content-Type": "application/json", "X-CSRFToken": csrfToken},
        "body": JSON.stringify(uploadData),
        })
      : fetch(url,{
        headers: {
          'X-CSRFToken': csrfToken
        }
      });

    const res = await Promise.race([fetchPro, timeout(TIMEOUT_SEC)]);
    const data = await res.json();
    if (!res.ok) throw new Error(`${data.message} (${res.status})`);
    return data;
  } catch (err) {
    throw err;
  }
};

const month = document.getElementById('month');
const year = document.getElementById('year');

const render = function(data){
  // Clear existing rows
  const tbody = document.querySelector('#employee-table');
  tbody.innerHTML = '';

  // Populate table with fetched data
  data.forEach((row, index) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
          <td class="tb_row">${index + 1}</td>
          <td class="tb_row">${row["_id"]}</td>
          <td class="tb_row">${row["Name"]}</td>
          <td class="tb_row">${row["Email"]}</td>
          <td class="hidden lg:table-cell tb_row">${new Date(row["CreatedDate"]).toLocaleString()}</td>
          <td class="hidden lg:table-cell tb_row">${new Date(row["CreatedDate"]).toLocaleString()}</td>
          <td class="hidden xl:table-cell tb_row">${row["Sex"]}</td>
      `;
      tbody.appendChild(tr);
  })
};

const get_Data = async function(uploadData){
  const data = await AJAX(API_URL, uploadData);
  render(data);
};

month.addEventListener('change', function(e){
  e.preventDefault();
  const uploadData = {"month": month.value, "year": year.value};
  get_Data(uploadData);
})

year.addEventListener('change', function(e){
  e.preventDefault();
  const uploadData = {"month": month.value, "year": year.value};
  get_Data(uploadData);
});

// const getResultsPage = function (page = state.search.page) {
//     state.search.page = page;
  
//     const start = (page - 1) * state.search.resultsPerPage; // 0
//     const end = page * state.search.resultsPerPage; // 9
  
//     return state.search.results.slice(start, end);
//   };
  
