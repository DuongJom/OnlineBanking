import { 
    get_admin_page_data, 
    render_table, 
    next, 
    previous, 
    adjustTableMargin, 
    closeDeleteForm
} from "./helpers.js";

document.addEventListener('DOMContentLoaded', async () => {
    const data_type = document.getElementById('dataType').value;
    const next_btn = document.getElementById('next-btn');
    const previous_btn = document.getElementById('previous-btn');
    const cancel_btn = document.getElementById('cancel-btn');

    localStorage.setItem('admin_page', 1);

    try {
        const data = await get_admin_page_data(1, data_type);
        localStorage.setItem('admin_maxPage', data.total_pages)
        render_table(data.items, data_type);
    } catch (error) {
        console.error('There was a problem with loading the items:', error);
    }

    next_btn.addEventListener('click', () => next(data_type));
    previous_btn.addEventListener('click', () => previous(data_type));
    cancel_btn.addEventListener('click', () => closeDeleteForm());

    window.addEventListener('resize', adjustTableMargin);
});


