export const TIMEOUT_SEC = 10;
export const RES_PER_PAGE = 10;
export const KEY = 'abc';
export const MODAL_CLOSE_SEC = 2.5;
export const icons = '../../static/img/icons.svg';

export const table_structure ={ 
  employee: [
    {key: 'STT', name: 'STT'},
    {key: 'EmployeeId', name: 'Employee ID'},
    {key: 'EmployeeName', name: 'Employee Name'},
    {key: 'Role', name: 'Role'},
    {key: 'Check_in_time', name: 'Check In'},
    {key: 'Check_out_time', name: 'Check Out'},
    {key: 'Working_status', name: 'Working Status'}
  ],
  salary: [
    {key: 'WageType', name: 'Wage  Type'},
    {key: 'BasicSalary', name: 'Basic Salary'},
    {key: 'OverTime', name: 'Over Time'},
    {key: 'PublicHoliday', name: 'Public Holiday'},
    {key: 'ShiftAllowance', name: 'Shift Allowance'},
    {key: 'GroomingAllowance', name: 'Grooming Allowance'},
    {key: 'PerformanceBonus', name: 'Performance Bonus'},
    {key: 'GrossWages', name: 'Gross Wages'},
    {key: 'NetPay', name: 'Net Pay'},
  ]
}

export const styles ={ 
  cell: 'whitespace-nowrap p-2 relative border-x border-black',
  table: 'border border-black',
  table1: 'border border-black z-10 sm:fixed shadow-shadowRight',
  table2: 'flex-1 border border-black',
  th: 'text-left p-2 border border-black whitespace-nowrap',
  tr: 'h-8 bg-blue-gray-50 my-3 border-t border-white',
  table_wrapper: 'w-99% overflow-x-auto',//flex absolute top-20, add these utilities if something wrong
  thead: 'bg-blue-gray-300',
}


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
 
  //AJAX, get data from backend
export const AJAX = async function (url, uploadData = undefined) {
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
          "headers": {
            'X-CSRFToken': csrfToken
          }
        });
  
      const res = await Promise.race([fetchPro, timeout(TIMEOUT_SEC)]);
      const data = await res.json();
      data.sort((a,b) => a.STT - b.STT);
      if (!res.ok) throw new Error(`${data.message} (${res.status})`);
      return data;
    } catch (err) {
      throw err;
    }
  };
  
export const state = {
  data:[],
  page: 1,
  resultsPerPage: 10
}

//generate pagination button
export function generatePaginationButton(icons) {
    const curPage = state.page;
    const numPages = Math.ceil(
      state.data.length / state.resultsPerPage // resultPerPage
    );
    // Page 1, and there are other pages
    if (curPage === 1 && numPages > 1) {
      return `
      <button data-goto='${curPage + 1}' class="btn--inline pagination__btn--next flex items-center 
      h-[30px] font-medium justify-center bg-blue-gray-400 text-white py-1.5 px-3 rounded-md 
      hover:bg-hover-btn-bg-color">
          <span>Page ${curPage + 1}</span>
          <svg class="w-6 h-6 ml-2">
              <use href="${icons}#icon-arrow-right"></use>
          </svg>
      </button>                
      `;
    }
      

    // Last page
    if (curPage === numPages && numPages > 1) {
      return `
      <button data-goto='${curPage - 1}' class="btn--inline pagination__btn--prev flex items-center 
      h-[30px] font-medium justify-center bg-blue-gray-400 text-white py-1.5 px-3 rounded-md 
      hover:bg-hover-btn-bg-color">
          <svg class="w-6 h-6 mr-2">
              <use href="${icons}#icon-arrow-left"></use>
          </svg>
          <span>Page ${curPage - 1}</span>
      </button> 
      `;
    }

    // Other page
    if (curPage < numPages) {
      return `
      <button data-goto='${curPage - 1}' class="btn--inline pagination__btn--prev flex items-center 
      h-[30px] font-medium justify-center bg-blue-gray-400 text-white py-1.5 px-3 rounded-md 
      hover:bg-hover-btn-bg-color">
          <svg class="w-6 h-6 mr-2">
              <use href="${icons}#icon-arrow-left"></use>
          </svg>
          <span>Page ${curPage - 1}</span>
      </button> 

      <button data-goto='${curPage + 1}' class="btn--inline pagination__btn--next flex items-center 
      h-[30px] font-medium justify-center bg-blue-gray-400 text-white py-1.5 px-3 rounded-md 
      hover:bg-hover-btn-bg-color">
          <span>Page ${curPage + 1}</span>
          <svg class="w-6 h-6 ml-2">
              <use href="${icons}#icon-arrow-right"></use>
          </svg>
      </button> 
      `;
    }

    // Page 1, and there are NO other pages
    return '';
  }

export const getSearchResultsPage = function (page = state.page) {
  state.page = page;

  const start = (page - 1) * state.resultsPerPage; //state.search.resultPerPage = 10 is the result per page
  const end = page * state.resultsPerPage;
  return state.data.slice(start, end);
};
