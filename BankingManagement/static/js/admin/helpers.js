import { tableStructure, identifier } from "./config.js";
import { createTableHeader, createActionButton } from "./utils.js";

const getAdminData = (page_no) => {
  const filterCondition = localStorage.getItem("filterCondition");
  const filter = filterCondition ? JSON.parse(filterCondition) : {};
  const queryParams = new URLSearchParams({criteria: JSON.stringify(filter)}).toString();

    return fetch(`/admin/account/${page_no}?${queryParams}`, {
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
      console.log("Received Data:", data);
      return data;
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
};


const renderTable = (items, data_type) => {
  
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
      renderTable(data.items, data_type);
    } catch (error) {
      console.error("There was a problem with loading the items:", error);
    }
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
      renderTable(data.items, data_type);
    } catch (error) {
      console.error("There was a problem with loading the items:", error);
    }
  }
}

const decide_button_type = (data_type) => {
  const addBtn = document.getElementById("add_button");

  if(addBtn != null)
  {
    addBtn.href = `/admin/${data_type}/add`;
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

const filter = async(data_type) => {
  console.log("ok");
  getFilterCondition();
  localStorage.setItem("admin_page", 1);
  try {
    const data = await getAdminData(1, data_type);
    localStorage.setItem("admin_maxPage", data.total_pages);
    renderTable(data.items, data_type);
  } catch (error) {
    console.error("There was a problem with loading the items:", error);
  }
}

const closeDeleteModal = () => {
  const delete_modal = document.getElementById("delete_modal");
  delete_modal.classList.add("hidden");
}

const adjustTableMargin = () => {
  const table1 = document.getElementById("table1");
  const table2 = document.getElementById("table2");
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
  closeDeleteModal,
  renderTable,
  goNext,
  goPrevious,
  adjustTableMargin,
  decide_button_type,
  openImportForm,
  closeImportForm,
  filter
};