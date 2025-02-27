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
  try {
    localStorage.setItem("filterCondition", JSON.stringify({IsDeleted: 0}));
    const data = await getAdminData(1);
    // renderTable(data, 'account');
  } catch (error) {
    console.error("There was a problem with loading the items:", error);
  }
});
 