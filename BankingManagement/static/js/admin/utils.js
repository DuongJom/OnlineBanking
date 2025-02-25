window.export_data = function() {
    const exportBtn = document.getElementById("export-btn");
    const data_type = document.getElementById("dataType").value;
    const file_type = exportBtn.value;
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    fetch(`/admin/export-data/${data_type}`, {
        method: 'POST',
        headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
        filter: JSON.parse(localStorage.getItem("filterCondition")),
        file_type: file_type
        })
    })
    .then(response => {
        if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.statusText}`);
        }
        return response.blob();
    })
    .then(blob => {
        if (blob.size === 0) {
        throw new Error('The file is empty. No data to download.');
        }

        // Create the download URL for the blob
        const downloadUrl = window.URL.createObjectURL(blob);

        // Determine file extension based on file type
        let ext = '';
        if (file_type == '3') {
        ext = '.xlsx';
        } else if (file_type == '16') {
        ext = '.json';
        } else {
        ext = '.csv';
        }

        // Create the file name using the current timestamp
        const fileName = "data_" + new Date().toISOString() + ext;

        // Create a temporary <a> tag to trigger download
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // Cleanup the created Object URL
        window.URL.revokeObjectURL(downloadUrl);
    })
    .catch(error => {
        // Display the error message if something goes wrong
        console.error("An error occurred:", error);
        alert(`Failed to download the file: ${error.message}`);
    });
}

const getFilterCondition = () => {
const dynamicKey = document.getElementById("dynamicKey").value; 
const dynamicValue = document.getElementById("dynamicValue").value; 
const status_value = document.getElementById("status_input").value;

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

filterCondition["IsDeleted"] = status_value;

localStorage.setItem("filterCondition", JSON.stringify(filterCondition));
}

const renderDeleteModal = (id, object_name, data_type) => {
const delete_modal = document.getElementById("delete_modal");
const deleteConfirmMessage = document.getElementById("deleteConfirmMessage");
const deleteForm = document.getElementById("delete_form");

deleteConfirmMessage.innerHTML = `Are you sure you want to delete <b style="color:red">${object_name}</b>?`;
delete_modal.classList.remove("hidden");
delete_modal.classList.add("flex");

deleteForm.action = `/admin/${data_type}/delete/${id}`

}

const createActionButton = (row, _id, data_type, object_name) => {
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

    const createStatusCol = (row, isActive) => {
    const status_cell = document.createElement("td");
    const div = document.createElement("div");

    status_cell.classList.add("border-x", "border-black");
    div.classList.add("flex", "justify-center");

    create_toggle_button(div, isActive);
    status_cell.appendChild(div);
    row.appendChild(status_cell);
}

const createTableHeader = (col_names, table, isFixed, data_type) => {
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

    // const status_col = document.createElement("th");
    // status_col.innerHTML = "Status";
    // if(col_names.length > 3) {
    //   status_col.classList.add("admin_th");
    // }else {
    //   status_col.classList.add("less_admin_th");
    // }
    // thead.appendChild(status_col);
    
  }
  table.appendChild(thead);
}

const generateObjectSign = (cell) => {
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

const create_toggle_button = (parent, isActive) => {
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

const addStyle = (element, classes) => {
    classes.split(" ").forEach(function (cls) {
      element.classList.add(cls);
    });
  }

export {
    generateObjectSign,
    create_toggle_button,
    createActionButton,
    createTableHeader,
    addStyle,
    getFilterCondition,
    renderDeleteModal,
}