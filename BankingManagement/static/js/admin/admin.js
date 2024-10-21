import {
  getAdminData,
  renderTable,
  goNext,
  goPrevious,
  closeDeleteModal,
  adjustTableMargin,
  decide_button_type,
  openImportForm,
  closeImportForm,
  filter,
} from "./helpers.js";
document.addEventListener("DOMContentLoaded", async () => {
  window.filter = filter;
  localStorage.setItem("filterCondition", JSON.stringify({}));
  window.addEventListener("resize", adjustTableMargin);
  const dataType = document.getElementById("dataType").value;
  const btnNext = document.getElementById("next-btn");
  const btnPrevious = document.getElementById("previous-btn");
  const btnCancel = document.getElementById("cancel-btn");
  const lazyLoading = document.getElementById("lazyLoading");
  const openImportFormBtn = document.getElementById("openImportFormButton");
  const closeImportFormBtn = document.getElementById("closeImportFormButton");
  const dynamicValue = document.getElementById("dynamicValue");
  localStorage.setItem("admin_page", 1);

  try {
    const data = await getAdminData(1, dataType);

    lazyLoading.classList.add('hidden');

    localStorage.setItem("admin_maxPage", data.total_pages);
    renderTable(data.items, dataType);
  } catch (error) {
    console.error("There was a problem with loading the items:", error);
  }

  // add event handler for button in admin page
  btnNext.addEventListener("click", () => goNext(dataType));
  btnPrevious.addEventListener("click", () => goPrevious(dataType));
  btnCancel.addEventListener("click", () => closeDeleteModal());
  openImportFormBtn.addEventListener("click", () => openImportForm());
  closeImportFormBtn.addEventListener("click", () => closeImportForm());
  decide_button_type(dataType);

  dynamicValue.addEventListener("keydown", function(event) {
    if (event.key === "Enter") { 
      filter(dataType);
    }
  });
});
 