import {
  getAdminData,
  renderTable,
  goNext,
  goPrevious,
  closeDeleteModal,
} from "./helpers.js";

document.addEventListener("DOMContentLoaded", async () => {
  const data_type = document.getElementById("dataType").value;
  const next_btn = document.getElementById("next-btn");
  const previous_btn = document.getElementById("previous-btn");
  const cancel_btn = document.getElementById("cancel-btn");
  const lazyLoading = document.getElementById("lazyLoading");

  localStorage.setItem("admin_page", 1);

  try {
    const data = await getAdminData(1, data_type);

    lazyLoading.classList.add('hidden');

    localStorage.setItem("admin_maxPage", data.total_pages);
    renderTable(data.items, data_type);
  } catch (error) {
    console.error("There was a problem with loading the items:", error);
  }

  // add event handler for button in admin page
  next_btn.addEventListener("click", () => goNext(data_type));
  previous_btn.addEventListener("click", () => goPrevious(data_type));
  cancel_btn.addEventListener("click", () => closeDeleteModal());

  

});
