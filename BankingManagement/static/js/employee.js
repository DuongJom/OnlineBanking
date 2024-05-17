'strict mode'

import {TIMEOUT_SEC} from './config.js'
const API_URL = '/get-data'

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
          <td class="tb_row">${new Date(row["CreatedDate"]).toLocaleString()}</td>
          <td class="tb_row">${new Date(row["CreatedDate"]).toLocaleString()}</td>
          <td class="tb_row">${row["Sex"]}</td>
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
  
