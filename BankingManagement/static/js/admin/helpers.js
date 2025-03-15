import { generateTableHeader, generateTableBody, getFilterCondition } from "./utils.js";
import { tableStructure } from "./config.js";

const getAdminData = (page_no, data_type) => {
  const filterCondition = localStorage.getItem("filterCondition");
  const filter = filterCondition ? JSON.parse(filterCondition) : {};
  const queryParams = new URLSearchParams({criteria: JSON.stringify(filter)}).toString();

    return fetch(`/admin/${data_type}/${page_no}?${queryParams}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
};

const renderTable = (data_type, lst_item) => {
  if (localStorage.getItem('admin_maxPage') != 1) {
    const location = document.getElementById("location");
    location.innerHTML = `${localStorage.getItem(
      "admin_page"
    )}/${localStorage.getItem("admin_maxPage")}`;
  }
  const tables = document.querySelectorAll("table");
  tables.forEach((table) => {
    table.remove();
  });

  document.getElementById('lazyLoading').classList.add('hidden');
  const table_wrapper = document.getElementById("table_wrapper");
  table_wrapper.classList.add('admin_table_wrapper');
  if (tableStructure[data_type].length <= 3) {
    const table = document.createElement('table');
    generateTableHeader(table, tableStructure[data_type]);
    generateTableBody(table, tableStructure[data_type, lst_item]);
    table_wrapper.appendChild(table);
    return;
  }
  const left_table = document.createElement('table');
  const right_table = document.createElement('table');
  left_table.id = "left_table";
  right_table.id = "right_table";
  const left_table_structure = tableStructure[data_type].slice(0, 3);
  const right_table_structure = tableStructure[data_type].slice(3);

  generateTableHeader(left_table, left_table_structure, false);
  generateTableBody(left_table, data_type, left_table_structure, lst_item, false);

  generateTableHeader(right_table, right_table_structure, true);
  generateTableBody(right_table, data_type, right_table_structure, lst_item, true);

  left_table.classList.add('admin_left_table');
  right_table.classList.add('admin_right_table');
  table_wrapper.appendChild(left_table);
  table_wrapper.appendChild(right_table);
  adjustTableMargin();
}

const goNext = async(data_type) => {
  var page = localStorage.getItem("admin_page");
  var max_page = localStorage.getItem("admin_maxPage");
  if (page < max_page) {
    page++;
    localStorage.setItem("admin_page", page);
    try {
      const data = await getAdminData(page, data_type);
      localStorage.setItem("admin_maxPage", data.total_pages);
      renderTable(data_type, data['items']);
    } catch (error) {
      console.error("There was a problem with loading the items:", error);
    }
  }
  if (page == max_page) {
    document.getElementById('next-btn').classList.add('hidden');
  }
  if (page == 2) {
    document.getElementById('previous-btn').classList.remove('hidden');
  }

}

const goPrevious = async(data_type, page) => {
  var page = localStorage.getItem("admin_page");
  if (page > 1) {
    page--;
    localStorage.setItem("admin_page", page);
    try {
      const data = await getAdminData(page, data_type);
      localStorage.setItem("admin_maxPage", data.total_pages);
      renderTable(data_type, data['items']);
    } catch (error) {
      console.error("There was a problem with loading the items:", error);
    }
  } 
  if (page == 1) {
    document.getElementById('previous-btn').classList.add('hidden');
  } 

  if (page == (localStorage.getItem('admin_maxPage') - 1)) {
    document.getElementById('next-btn').classList.remove('hidden');
  }
  
}

const setAddUrl = (data_type) => {
  const addBtn = document.getElementById("add_button");

  if(addBtn != null)
  {
    addBtn.href = `/admin/${data_type}/new`;
  }
}

const openImportForm = () => {
  const importForm = document.getElementById("importForm");
  
  importForm.classList.remove('hidden');
  importForm.classList.add('flex');
}

const closeImportForm = () => {
  const importForm = document.getElementById("importForm");

  importForm.classList.remove('flex');
  importForm.classList.add('hidden');
}

window.filter = async(data_type) => {
  getFilterCondition();
  localStorage.setItem("admin_page", 1);
  try {
    const data = await getAdminData(1, data_type);
    localStorage.setItem("admin_maxPage", data.total_pages);
    renderTable(data_type, data.items);
  } catch (error) {
    console.error("There was a problem with loading the items:", error);
  }
}

const adjustTableMargin = () => {
  const table1 = document.getElementById("left_table");
  const table2 = document.getElementById("right_table");
  if(table1 != null) {
    if (innerWidth >= 540) {
      table2.style.marginLeft = `${table1.offsetWidth - 2}px`;
    } else {
      table2.style.marginLeft = "0px";
    }
  }
}

export {
  getAdminData,
  renderTable,
  goNext,
  goPrevious,
  adjustTableMargin,
  setAddUrl,
  openImportForm,
  closeImportForm,
};