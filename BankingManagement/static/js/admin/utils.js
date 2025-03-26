const ID_INDEX = 0;
const OBJECT_NAME_INDEX = 1;

const FileExtension = Object.freeze({
  EXCEL: "xlsx",
  CSV: "csv",
  JSON: "json"
});

const FileType = Object.freeze({
  EXCEL: 3,
  JSON: 16,
  CSV: 17
});

const ActionType = Object.freeze({
  VIEW: "visibility",
  EDIT: "edit",
  DELETE: "delete"
});

const formatId = (id, length) => {
  return String(id).padStart(length, "0");
};

const formatCurrency = (value) => {
  return new Intl.NumberFormat("en-US").format(value);
};

window.export_data = () => {
  const exportBtn = document.getElementById("export-btn");
  const data_type = document.getElementById("dataType").value;
  const file_type = exportBtn.value;
  const csrfToken = document.querySelector('input[name="csrf_token"]').value;

  fetch(`/admin/${data_type}/export`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      filter: JSON.parse(localStorage.getItem("filterCondition")),
      file_type: file_type,
    }),
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error(`Failed to fetch data: ${response.statusText}`);
    }
    return response.blob();
  })
  .then((blob) => {
    if (blob.size === 0) {
      throw new Error("The file is empty. No data to download.");
    }

    const downloadUrl = window.URL.createObjectURL(blob);
    let ext = FileExtension.CSV;

    if (file_type == FileType.EXCEL) {
      ext = FileExtension.EXCEL;
    } 
    else{
      ext = FileExtension.JSON;
    }

    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    const fileName = `data_${data_type}_${year}${month}${day}_${hours}${minutes}${seconds}.${ext}`;
    const a = document.createElement("a");

    a.href = downloadUrl;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    window.URL.revokeObjectURL(downloadUrl);
  })
  .catch((error) => {
    console.error("An error occurred:", error);
    alert(`Failed to download the file: ${error.message}`);
  });
  exportBtn.selectedIndex = 0;
};

const getFilterCondition = () => {
  const dynamicKey = document.getElementById("dynamicKey").value;
  const dynamicValue = document.getElementById("dynamicValue").value;
  const status_value = document.getElementById("status_input").value;
  let filterCondition = {};

  try {
    const fixedCondition = [...document.getElementsByClassName("fixedCondition"),];

    fixedCondition.map((con) => {
      if (con.value.toString().trim().length !== 0) {
        filterCondition[con.name] = con.value;
      }
    });
  } catch (error) {
    console.log(error.message);
  }

  if (dynamicValue.toString().trim().length !== 0 && dynamicKey.toString().trim().length !== 0) {
    filterCondition[dynamicKey] = { $regex: `^${dynamicValue}`, $options: "i" };
  }

  filterCondition["IsDeleted"] = status_value;
  localStorage.setItem("filterCondition", JSON.stringify(filterCondition));
};

const renderDeleteModal = (id, object_name, data_type) => {
  const page = localStorage.getItem("admin_page");
  const delete_modal = document.getElementById("delete_modal");
  const deleteConfirmMessage = document.getElementById("deleteConfirmMessage");
  const deleteForm = document.getElementById("delete_form");
  const page_input = document.createElement("input");

  page_input.value = page;
  page_input.name = "current_page";
  page_input.classList.add("hidden");

  deleteConfirmMessage.innerHTML = `Are you sure you want to delete <b style="color:red">${object_name}</b>?`;
  delete_modal.classList.remove("hidden");
  delete_modal.classList.add("flex");
  deleteForm.action = `/admin/${data_type}/delete/${id}`;
  deleteForm.appendChild(page_input);
};

const generateActionButton = (row, _id, data_type, object_name) => {
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
      case ActionType.VIEW:
        btn.href = `/admin/${data_type}/view/${_id}`;
        break;
      case ActionType.EDIT:
        btn.href = `/admin/${data_type}/edit/${_id}`;
        break;
      case ActionType.DELETE:
        btn.addEventListener("click", () => {
          renderDeleteModal(_id, object_name, data_type);
        });
        break;
    }
    i++;
  });

  action_cell.appendChild(div);
  row.appendChild(action_cell);
};

const generateTableHeader = (table, lst_field, is_right_table) => {
  const thead = document.createElement("thead");
  const tr = document.createElement("tr");

  lst_field.forEach((field) => {
    const th = document.createElement("th");
    th.innerText = field["name"];
    th.classList.add("admin_cell");
    tr.appendChild(th);
  });

  if (is_right_table) {
    const th = document.createElement("th");
    th.innerText = "Action";
    th.classList.add("admin_cell");
    tr.appendChild(th);
  }

  thead.classList.add("admin_thead");
  thead.appendChild(tr);
  table.appendChild(thead);
};

const generateTableBody = (table, data_type, lst_field, lst_item, is_right_table) => {
  const table_body = document.createElement("tbody");
  let count = 0;
  let actual_lst_item = [];

  if (lst_field.length <= 3 && is_right_table) {
    actual_lst_item = lst_item.slice(0);
  } 
  else {
    if (is_right_table) {
      lst_item.forEach((item) => {
        actual_lst_item.push(item.slice(3));
      });
    } 
    else {
      lst_item.forEach((item) => {
        actual_lst_item.push(item.slice(0, 3));
      });
    }
  }

  actual_lst_item.forEach((item, index) => {
    const tr = document.createElement("tr");

    for (let i = 0; i < lst_field.length; i++) {
      const td = document.createElement("td");

      if (lst_field[i]["isObjectId"] && item[i] != null) {
        td.classList.add("text-center");
        td.innerText = formatId(item[i], 5);
      } 
      else if (item[i] == null) {
        td.innerHTML = "";
      } 
      else if (lst_field[i]["isNumberFormat"]) {
        td.classList.add("text-right");
        td.innerHTML = formatCurrency(item[i]);
      } 
      else {
        td.innerHTML = item[i];
      }

      td.classList.add("admin_cell");
      tr.appendChild(td);
    }

    tr.classList.add("even:bg-gray-300", "bg-white");

    tr.addEventListener("mouseenter", () => {
      const lst_left_row = document.querySelectorAll("#left_table tbody tr");
      const lst_right_row = document.querySelectorAll("#right_table tbody tr");
      lst_left_row[index].classList.remove("even:bg-gray-300", "bg-white");
      lst_right_row[index].classList.remove("even:bg-gray-300", "bg-white");
      lst_left_row[index].classList.add("bg-green-300");
      lst_right_row[index].classList.add("bg-green-300");
    });

    tr.addEventListener("mouseleave", () => {
      const lst_left_row = document.querySelectorAll("#left_table tbody tr");
      const lst_right_row = document.querySelectorAll("#right_table tbody tr");
      lst_left_row[index].classList.add("even:bg-gray-300", "bg-white");
      lst_right_row[index].classList.add("even:bg-gray-300", "bg-white");
      lst_left_row[index].classList.remove("bg-green-300");
      lst_right_row[index].classList.remove("bg-green-300");
    });

    if (is_right_table) {
      generateActionButton(tr, lst_item[count][ID_INDEX], data_type, lst_item[count][OBJECT_NAME_INDEX]);
    }

    table_body.appendChild(tr);
    count++;
  });

  table.appendChild(table_body);
};

export { 
  getFilterCondition, 
  generateTableBody, 
  generateTableHeader 
};