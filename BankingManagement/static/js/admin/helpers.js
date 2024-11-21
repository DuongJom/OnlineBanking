import { tableStructure, identifier } from "./config.js";

export function getAdminData(page, dataType) {
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

export function closeDeleteModal() {
  const delete_modal = document.getElementById("delete_modal");
  delete_modal.classList.add("hidden");
}

function renderDeleteModal(id, object_name, data_type) {
  const delete_modal = document.getElementById("delete_modal");
  const deleteConfirmMessage = document.getElementById("deleteConfirmMessage");
  const deleteForm = document.getElementById("delete_form");

  deleteConfirmMessage.innerHTML = `Are you sure you want to delete <b style="color:red">${object_name}</b>?`;
  delete_modal.classList.remove("hidden");
  delete_modal.classList.add("flex");

  deleteForm.action = `/admin/${data_type}/delete/${id}`
  
}

function createActionButton(row, _id, data_type, object_name) {
  // UI for action button
  const action_cell = document.createElement("td");
  const view_btn = document.createElement("a");
  const delete_btn = document.createElement("a");
  const edit_btn = document.createElement("a");
  const div = document.createElement("div");

  const btn_list = [view_btn, delete_btn, edit_btn];
  const icon_list = ["visibility", "delete", "edit"];
  let i = 0;

  action_cell.classList.add("border-x", "border-black");
  div.classList.add("flex", "justify-center");

  btn_list.forEach((btn) => {
    const span = document.createElement("span");

    btn.classList.add("flex", "items-center", "justify-center");
    span.classList.add(
      "material-symbols-outlined",
      "hover:bg-gray-500",
      "rounded",
      "cursor-pointer"
    );

    span.style.fontWeight = "300";
    span.innerHTML = icon_list[i];
    btn.appendChild(span);
    div.appendChild(btn);

    switch (icon_list[i]) {
      case "visibility":
        btn.href = `/admin/${data_type}/view/${_id}`;
        break;
      case "edit":
        btn.href = `/admin/${data_type}/edit/${_id}`;
        break;
      case "delete":
        btn.addEventListener("click", () => {
          renderDeleteModal(_id, object_name, data_type);
        });
        break;
    }
    i++;
  });

  action_cell.appendChild(div);
  row.appendChild(action_cell);
}

function createStatusCol(row, isActive) {
  const status_cell = document.createElement("td");
  const div = document.createElement("div");

  status_cell.classList.add("border-x", "border-black");
  div.classList.add("flex", "justify-center");

  create_toggle_button(div, isActive);
  status_cell.appendChild(div);
  row.appendChild(status_cell);
}

export function renderTable(items, data_type) {
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
      createStatusCol(row, true, items[i]["IsDeleted"]);
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
    createStatusCol(row, items[i]["IsDeleted"]);
    tbody2.appendChild(row);
  }

  table_wrapper.appendChild(table1);
  table1.classList.add("admin_table1");
  table2.classList.add("admin_table2");
  table_wrapper.appendChild(table2);
  adjustTableMargin();
}

function createTableHeader(col_names, table, isFixed, data_type) {
  const thead = document.createElement("thead");
  thead.classList.add("admin_thead");
  if(col_names.length > 3 || isFixed == true) {
    col_names.forEach((col_name) => {
      var th = document.createElement("th");
      th.classList.add("admin_th"); 
      th.innerHTML = col_name.name;
      thead.appendChild(th); 
    });
  }else {
    col_names.forEach((col_name) => {
      const th = document.createElement("th");
      th.classList.add("less_admin_th"); 
      th.innerHTML = col_name.name;
      thead.appendChild(th); 
    });
  }

  if (!isFixed) {
    const action_col = document.createElement("th");

    action_col.innerHTML = "Action";
    if(col_names.length > 3) {
      action_col.classList.add("admin_th");
    }else {
      action_col.classList.add("less_admin_th");
    }  
    
    thead.appendChild(action_col);

    const status_col = document.createElement("th");
    status_col.innerHTML = "Status";
    if(col_names.length > 3) {
      status_col.classList.add("admin_th");
    }else {
      status_col.classList.add("less_admin_th");
    }
    thead.appendChild(status_col);
    
  }
  table.appendChild(thead);
}

function generateObjectSign(cell) {
  const icon = document.createElement("div");

  icon.innerHTML = "i";
  icon.classList.add("font-bold");
  icon.classList.add(
    "w-5",
    "h-5",
    "bg-popup-bg",
    "inline-block",
    "rounded-full",
    "text-center",
    "leading-5",
    "mr-3"
  );
  cell.insertBefore(icon, cell.firstChild);
  cell.classList.add("cursor-pointer", "hover:bg-gray-400");
}

export async function goNext(data_type) {
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

export async function goPrevious(data_type, page) {
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

export function adjustTableMargin() {
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

function addStyle(element, classes) {
  classes.split(" ").forEach(function (cls) {
    element.classList.add(cls);
  });
}

function create_toggle_button(parent, isActive) {
  const wrapper_style = "inline-flex items-center me-5";
  const input_style = "sr-only peer";
  const text_style =
    "ms-3 text-sm font-medium text-gray-900 dark:text-gray-500";
  const div_style =
    "relative w-8 h-4 bg-gray-500 rounded-full peer dark:bg-gray-700 peer-focus:ring-4" +
    "peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 peer-checked:after:translate-x-full " +
    "rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] " + 
    "after:absolute after:top-0 after:start-0 after:bg-white after:border-gray-300 after:border " +
    "after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600";

  const wrapper = document.createElement("label");
  const input = document.createElement("input");
  const div = document.createElement("div");
  const text = document.createElement("span");

  input.type = "checkbox";
  input.disabled = true;

  if (isActive == 0) {
    input.checked = true;
    text.innerHTML = "Active";
  }else {
    text.innerHTML = "Inactive";
  }

  addStyle(wrapper, wrapper_style);
  addStyle(input, input_style);
  addStyle(text, text_style);
  addStyle(div, div_style);

  wrapper.appendChild(input);
  wrapper.appendChild(div);
  wrapper.appendChild(text);

  parent.appendChild(wrapper);
}

export function decide_button_type(data_type) {
  const addBtn = document.getElementById("add_button");

  if(addBtn != null)
  {
    addBtn.href = `/admin/${data_type}/add`;
  }
}

export function openImportForm() {
  const importForm = document.getElementById("importForm");
  
  importForm.classList.remove('hidden');
  importForm.classList.add('flex');
}

export function closeImportForm() {
  const importForm = document.getElementById("importForm");
  
  importForm.classList.remove('flex');
  importForm.classList.add('hidden');
}

function getFilterCondition() {
  const dynamicKey = document.getElementById("dynamicKey").value; 
  const dynamicValue = document.getElementById("dynamicValue").value; 

  let filterCondition = {};

  try {
    const fixedCondition = [...document.getElementsByClassName("fixedCondition")];
    fixedCondition.map(con => {
      if(con.value !== "") {
        filterCondition[con.name] = con.value;
      }
    })

  }
  catch(error) {
    console.log(error.message);
  }

  if (dynamicValue !== "" && dynamicKey !== "") {
    filterCondition[dynamicKey] = {$regex: `^${dynamicValue}`, $options: 'i'};
  }
  console.log(filterCondition);
  localStorage.setItem("filterCondition", JSON.stringify(filterCondition));
}

export async function filter(data_type) {
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
