export const TIMEOUT_SEC = 10;
export const RES_PER_PAGE = 10;
export const KEY = 'abc';
export const MODAL_CLOSE_SEC = 2.5;
export const icons = '../../static/img/icons.svg';

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
