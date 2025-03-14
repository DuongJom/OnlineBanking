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
  const btnNext = document.getElementById("next-btn");
  const btnPrevious = document.getElementById("previous-btn");
  let timeout = null;
  window.addEventListener("resize", adjustTableMargin);
  localStorage.setItem("admin_page", 1);
  decide_button_type(dataType);
  try {
    localStorage.setItem("filterCondition", JSON.stringify({IsDeleted: 0}));
    const data = await getAdminData(1, dataType);
    localStorage.setItem("admin_maxPage", data['total_pages']);
    renderTable(dataType, data['items']);
  } catch (error) {
    console.error("There was a problem with loading the items:", error);
  }

  if(localStorage.getItem('admin_maxPage') == 1) {
    btnNext.classList.add('hidden');
  } 
  btnPrevious.classList.add('hidden');

  document.getElementById('cancel-btn').addEventListener('click', () => {
    document.getElementById('delete_modal').classList.add('hidden');
  })

  dynamicValue.addEventListener('keyup', function () {
    clearTimeout(timeout);
    timeout = setTimeout(function () {
      filter(dataType);
    }, 1000);
  });

  btnNext.addEventListener("click", () => goNext(dataType));
  btnPrevious.addEventListener("click", () => goPrevious(dataType));
  openImportFormBtn.addEventListener("click", () => openImportForm());
  closeImportFormBtn.addEventListener("click", () => closeImportForm());
});
 