import { tableStructure, identifier } from "./config.js";
import { createTableHeader, createActionButton } from "./utils.js";

const getAdminData = (page, dataType) => {
  const csrfToken = document.querySelector('input[name="csrf_token"]').value;
  return fetch(`/admin`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      page: page,
      dataType: dataType,
      filter: JSON.parse(localStorage.getItem("filterCondition"))
    }),
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
}

const renderTable = (items, data_type) => {
  const tables = document.querySelectorAll("table");
  const table_wrapper = document.getElementById("table_wrapper");
  const col_names = tableStructure[data_type];
  const number_col = col_names.length;
  const location = document.getElementById("location");

  tables.forEach((table) => {
    table.remove();
  });

  table_wrapper.classList.add("admin_table_wrapper");

  location.innerHTML = `${localStorage.getItem(
    "admin_page"
  )}/${localStorage.getItem("admin_maxPage")}`;

  //get dataType for the table
  if (number_col <= 3) {
    //if table has less than 4 columns
    const table = document.createElement("table");
    const tbody = document.createElement("tbody");

    table.classList.add("admin_table");
    createTableHeader(col_names, table, false, data_type);
    table.appendChild(tbody);

    for (let i = 0; i < items.length; i++) {
      const row = document.createElement("tr");
      row.classList.add("admin_tr");
      col_names.forEach((col_name) => {
        const cell = document.createElement("td");
        cell.classList.add("admin_cell");
        cell.innerHTML = items[i][col_name.key];
        if (typeof items[i][col_name.key] == "object") {
          if(Array.isArray(items[i][col_name.key])) {
            if(items[i][col_name.key].length != 0 && items[i][col_name.key][0] != null) {
              cell.innerHTML = items[i][col_name.key].map(item => item.MethodName).join(', ');
            }else {
              cell.innerHTML = ""
            }
          }else if(col_name.isObject == true){
            cell.innerHTML = items[i][col_name.key][col_name.object_key];
            generateObjectSign(cell);
          }else {
            cell.innerHTML = items[i][col_name.key][col_name.object_key];
          }
        }
        row.appendChild(cell);
      });

      createActionButton(
        row,
        items[i]["_id"],
        data_type,
        items[i][identifier[data_type]]
      );
      // createStatusCol(row, true, items[i]["IsDeleted"]);
      tbody.appendChild(row);
    }
    table_wrapper.appendChild(table);
    return;
  }

  //if table has greater than or equal to 4 columns
  const col_names1 = col_names.slice(0, 3); //cols for left(fixed) table
  const col_names2 = col_names.slice(3, number_col); //cols for right table
  const table1 = document.createElement("table");
  const tbody1 = document.createElement("tbody");
  const table2 = document.createElement("table");
  const tbody2 = document.createElement("tbody");

  //fixed table
  table1.id = "table1";
  createTableHeader(col_names1, table1, true, data_type);
  table1.appendChild(tbody1);

  //right table
  table2.id = "table2";
  createTableHeader(col_names2, table2, false, data_type);
  table2.appendChild(tbody2);

  //loop to render fixed table
  for (let i = 0; i < items.length; i++) {
    const row = document.createElement("tr");
    row.classList.add("admin_tr");
    col_names1.forEach((col_name) => {
      const cell = document.createElement("td");
      cell.classList.add("admin_cell");
      if(items[i][col_name.key] != undefined) {
        cell.innerHTML = items[i][col_name.key];
        if (typeof items[i][col_name.key] == "object") {
          if(Array.isArray(items[i][col_name.key])) {
            if(items[i][col_name.key].length != 0 && items[i][col_name.key][0] != null) {
              cell.innerHTML = items[i][col_name.key].map(item => item.MethodName).join(', ');
            }else {
              cell.innerHTML = ""
            }
          }else if(col_name.isObject == true){
            cell.innerHTML = items[i][col_name.key][col_name.object_key];
            generateObjectSign(cell);
          }else {
            cell.innerHTML = items[i][col_name.key][col_name.object_key];
          }
        }
      }else {
        cell.innerHTML = "undefined";
      }
      row.appendChild(cell);
    });
    tbody1.appendChild(row);
  }

  //loop to render right table
  for (let i = 0; i < items.length; i++) {
    const row = document.createElement("tr");
    row.classList.add("admin_tr");
    col_names2.forEach((col_name) => {
      const cell = document.createElement("td");
      cell.classList.add("admin_cell");
      if(items[i][col_name.key] != undefined) {
        cell.innerHTML = items[i][col_name.key];
        if (typeof items[i][col_name.key] == "object") {
          if(Array.isArray(items[i][col_name.key])) {
            if(items[i][col_name.key].length != 0 && items[i][col_name.key][0] != null) {
              cell.innerHTML = items[i][col_name.key].map(item => item.MethodName).join(', ');
            }else {
              cell.innerHTML = ""
            }
          }else if(col_name.isObject == true){
            cell.innerHTML = items[i][col_name.key][col_name.object_key];
            generateObjectSign(cell);
          }else {
            cell.innerHTML = items[i][col_name.key][col_name.object_key];
          }
        }
      }else {
        cell.innerHTML = "undefined";
      }
      
      row.appendChild(cell);
    });
    createActionButton(
      row,
      items[i]["_id"],
      data_type,
      items[i][identifier[data_type]]
    );
    // createStatusCol(row, items[i]["IsDeleted"]);
    tbody2.appendChild(row);
  }

  table_wrapper.appendChild(table1);
  table1.classList.add("admin_table1");
  table2.classList.add("admin_table2");
  table_wrapper.appendChild(table2);
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