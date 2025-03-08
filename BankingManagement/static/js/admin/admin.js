import {
  getAdminData,
  renderTable,
  goNext,
  goPrevious,
  adjustTableMargin,
  decide_button_type,
  openImportForm,
  closeImportForm,
} from "./helpers.js";

document.addEventListener("DOMContentLoaded", async () => {
  const dataType = document.getElementById("dataType").value;
  const dynamicValue = document.getElementById("dynamicValue");
  const openImportFormBtn = document.getElementById("openImportFormButton");
  const closeImportFormBtn = document.getElementById("closeImportFormButton");
  let timeout = null;
  window.addEventListener("resize", adjustTableMargin);
  localStorage.setItem("admin_page", 1);
  decide_button_type(dataType);
  try {
    localStorage.setItem("filterCondition", JSON.stringify({IsDeleted: 0}));
    const data = await getAdminData(1, dataType);
    renderTable(dataType, data['items']);
  } catch (error) {
    console.error("There was a problem with loading the items:", error);
  }

  document.getElementById('cancel-btn').addEventListener('click', () => {
    document.getElementById('delete_modal').classList.add('hidden');
  })

  dynamicValue.addEventListener('keyup', function () {
    clearTimeout(timeout);

    timeout = setTimeout(function () {
      filter(dataType);
    }, 1000);
  });

  openImportFormBtn.addEventListener("click", () => openImportForm());
  closeImportFormBtn.addEventListener("click", () => closeImportForm());

});
 