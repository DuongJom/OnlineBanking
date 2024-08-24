import { tableStructure, identifier } from "./config.js";

export function getAdminData(page, dataType) {
  return fetch(`/admin?page=${page}&dataType=${dataType}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
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
}

export function closeDeleteModal() {
  const deleteModal = document.getElementById("delete_modal");
  deleteModal.classList.add("hidden");
}

function renderDeleteModal(id, name) {
  const deleteModal = document.getElementById("delete_modal");
  const objectId = document.getElementById("object_id");
  const deleteConfirmMessage = document.getElementById("deleteConfirmMessage");

  deleteConfirmMessage.innerHTML = `Are you sure you want to delete <b style="color:red">${name}</b>?`;
  deleteModal.classList.remove("hidden");
  deleteModal.classList.add("flex");
  objectId.setAttribute("value", id);
}

function createActionButton(row, id, dataType, name) {
  // UI for action button
  const cellAction = document.createElement("td");
  const btnView = document.createElement("a");
  const btnDelete = document.createElement("a");
  const btnEdit = document.createElement("a");
  const div = document.createElement("div");

  const lstButton = [btnView, btnDelete, btnEdit];
  const lstIcon = ["visibility", "delete", "edit"];
  let i = 0;

  cellAction.classList.add("border-x", "border-black");
  div.classList.add("flex", "justify-center");

  lstButton.forEach((btn) => {
    const span = document.createElement("span");

    btn.classList.add("flex", "items-center", "justify-center");
    span.classList.add(
      "material-symbols-outlined",
      "hover:bg-gray-500",
      "rounded",
      "cursor-pointer"
    );

    span.style.fontWeight = "300";
    span.innerHTML = lstIcon[i];
    btn.appendChild(span);
    div.appendChild(btn);

    switch (lstIcon[i]) {
      case "visibility":
        btn.href = `/admin/${dataType}/view/${id}`;
        break;
      case "edit":
        btn.href = `/admin/${dataType}/edit/${id}`;
        break;
      case "delete":
        btn.addEventListener("click", () => {
          renderDeleteModal(id, name);
        });
        break;
    }
    i++;
  });

  cellAction.appendChild(div);
  row.appendChild(cellAction);
}

function createStatusCol(row, isActive) {
  const cellStatus = document.createElement("td");
  const div = document.createElement("div");

  cellStatus.classList.add("border-x", "border-black");
  div.classList.add("flex", "justify-center");

  createToggleButton(div, isActive);
  cellStatus.appendChild(div);
  row.appendChild(cellStatus);
}

export function renderTable(items, dataType) {
  const tables = document.querySelectorAll("table");
  const tableWrapper = document.getElementById("table_wrapper");
  const colNames = tableStructure[dataType];
  const columnCount = colNames.length;
  const location = document.getElementById("location");
  const pagination = document.getElementById("pagination");

  tables.forEach((table) => {
    table.remove();
  });

  tableWrapper.classList.add("admin_table_wrapper");

  location.innerHTML = `${localStorage.getItem("admin_page")}/${localStorage.getItem("admin_maxPage")}`;

  // set visibility of pagination part of table
  pagination.classList.remove("hidden");
  if(localStorage.getItem("admin_maxPage") <= 1){
    pagination.classList.add("hidden");
  }

  //get dataType for the table
  if (columnCount <= 3) {
    //if table has less than 4 columns
    const table = document.createElement("table");
    const tbody = document.createElement("tbody");

    table.classList.add("admin_table");
    createTableHeader(colNames, table, false, dataType);
    table.appendChild(tbody);

    for (let i = 0; i < items.length; i++) {
      const row = document.createElement("tr");
      row.classList.add("admin_tr");
      colNames.forEach((col_name) => {
        const cell = document.createElement("td");
        cell.classList.add("admin_cell");
        cell.innerHTML = items[i][col_name.key];
        if (typeof items[i][col_name.key] == "object") {
          generateObjectSign(cell);
          cell.innerHTML = items[i][col_name.key][col_name.object_key];
        }
        row.appendChild(cell);
      });

      createActionButton(
        row,
        items[i]["_id"],
        dataType,
        items[i][identifier[dataType]]
      );

      if (dataType == "account") {
        createStatusCol(row, true, items[i]["IsDeleted"]);
      }

      tbody.appendChild(row);
    }
    tableWrapper.appendChild(table);
    return;
  }

  //if table has greater than or equal to 4 columns
  const colNames1 = colNames.slice(0, 3); //cols for left(fixed) table
  const colNames2 = colNames.slice(3, columnCount); //cols for right table
  const table1 = document.createElement("table");
  const tbody1 = document.createElement("tbody");
  const table2 = document.createElement("table");
  const tbody2 = document.createElement("tbody");

  //fixed table
  table1.id = "table1";
  createTableHeader(colNames1, table1, true, dataType);
  table1.appendChild(tbody1);

  //right table
  table2.id = "table2";
  createTableHeader(colNames2, table2, false, dataType);
  table2.appendChild(tbody2);

  //loop to render fixed table
  for (let i = 0; i < items.length; i++) {
    const row = document.createElement("tr");
    row.classList.add("admin_tr");
    colNames1.forEach((col_name) => {
      const cell = document.createElement("td");
      cell.classList.add("admin_cell");
      if(items[i][col_name.key] != undefined) {
        cell.innerHTML = items[i][col_name.key];
        if (typeof items[i][col_name.key] == "object") {
          cell.innerHTML = items[i][col_name.key][col_name.object_key];
          generateObjectSign(cell);
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
    colNames2.forEach((col_name) => {
      const cell = document.createElement("td");
      cell.classList.add("admin_cell");
      if(items[i][col_name.key] != undefined) {
        cell.innerHTML = items[i][col_name.key];
        if (typeof items[i][col_name.key] == "object") {
          cell.innerHTML = items[i][col_name.key][col_name.object_key];
          generateObjectSign(cell);
        }
      }else {
        cell.innerHTML = "undefined";
      }
      
      row.appendChild(cell);
    });
    createActionButton(
      row,
      items[i]["_id"],
      dataType,
      items[i][identifier[dataType]]
    );

    if (dataType == "account") {
      createStatusCol(row, items[i]["IsDeleted"]);
    }

    tbody2.appendChild(row);
  }

  tableWrapper.appendChild(table1);
  table1.classList.add("admin_table1");
  table2.classList.add("admin_table2");
  tableWrapper.appendChild(table2);
  adjustTableMargin();
}

function createTableHeader(colNames, table, isFixed, dataType) {
  const thead = document.createElement("thead");
  thead.classList.add("admin_thead");

  if(colNames.length > 3 || isFixed == true) {
    colNames.forEach((col_name) => {
      const th = document.createElement("th");
      th.classList.add("admin_th"); 
      th.innerHTML = col_name.name;
      console.log(col_name.name);
      thead.appendChild(th);
    });
  }else {
    colNames.forEach((col_name) => {
      const th = document.createElement("th");
      th.classList.add("less_admin_th"); 
      th.innerHTML = col_name.name;
      thead.appendChild(th);
    });
  }
  

  if (!isFixed) {
    const columnAction = document.createElement("th");

    columnAction.innerHTML = "Action";
    if(colNames.length > 3) {
      columnAction.classList.add("admin_th");
    }else {
      columnAction.classList.add("less_admin_th");
    }  
    
    thead.appendChild(columnAction);

    if (dataType == "account") {
      const columnStatus = document.createElement("th");
      columnStatus.innerHTML = "Status";
      if(colNames.length > 3) {
        columnStatus.classList.add("admin_th");
      }else {
        columnStatus.classList.add("less_admin_th");
      }
      thead.appendChild(columnStatus);
    }
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

export async function goNext(dataType) {
  var page = localStorage.getItem("admin_page");
  var maxPage = localStorage.getItem("admin_maxPage");

  if (page < maxPage) {
    page++;
    localStorage.setItem("admin_page", page);
    try {
      const data = await getAdminData(page, dataType);

      localStorage.setItem("admin_maxPage", data.total_pages);
      renderTable(data.items, dataType);
    } catch (error) {
      console.error("There was a problem with loading the items:", error);
    }
  }
}

export async function goPrevious(dataType, page) {
  var page = localStorage.getItem("admin_page");

  if (page > 1) {
    page--;
    localStorage.setItem("admin_page", page);
    try {
      const data = await getAdminData(page, dataType);
      localStorage.setItem("admin_maxPage", data.total_pages);
      renderTable(data.items, dataType);
    } catch (error) {
      console.error("There was a problem with loading the items:", error);
    }
  }
}

export function adjustTableMargin() {
  const table1 = document.getElementById("table1");
  const table2 = document.getElementById("table2");

  if (innerWidth >= 700) {
    table2.style.marginLeft = `${table1.offsetWidth - 2}px`;
  } else {
    table2.style.marginLeft = "0px";
  }
}

function addStyle(element, classes) {
  classes.split(" ").forEach(function (cls) {
    element.classList.add(cls);
  });
}

function createToggleButton(parent, isActive) {
  const wrapperStyle = "inline-flex items-center me-5";
  const inputStyle = "sr-only peer";
  const textStyle =
    "ms-3 text-sm font-medium text-gray-900 dark:text-gray-300";
  const divStyle =
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
  }
  text.innerHTML = "Inactive";

  addStyle(wrapper, wrapperStyle);
  addStyle(input, inputStyle);
  addStyle(text, textStyle);
  addStyle(div, divStyle);

  wrapper.appendChild(input);
  wrapper.appendChild(div);
  wrapper.appendChild(text);

  parent.appendChild(wrapper);
}
