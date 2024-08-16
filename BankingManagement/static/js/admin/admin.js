import {
  get_admin_page_data,
  render_table,
  next,
  previous,
  adjustTableMargin,
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
    const data = await get_admin_page_data(1, data_type);

    lazyLoading.classList.add('hidden');

    localStorage.setItem("admin_maxPage", data.total_pages);
    render_table(data.items, data_type);
  } catch (error) {
    console.error("There was a problem with loading the items:", error);
  }

  next_btn.addEventListener("click", () => next(data_type));
  previous_btn.addEventListener("click", () => previous(data_type));
  cancel_btn.addEventListener("click", () => closeDeleteModal());

  addEventListener("resize", adjustTableMargin);
});
