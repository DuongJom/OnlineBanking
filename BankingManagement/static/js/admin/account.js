import { get_admin_page_data, create_action_button } from './admin.js';

var page = 1;
var totalPage = 0;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const data = await get_admin_page_data(page, 'account');
        totalPage = data.total_pages;
        render_account_table(data.items);
    } catch (error) {
        console.error('There was a problem with loading the items:', error);
    }

    const nextbtn = document.getElementById('next-btn');
    nextbtn.addEventListener('click', next_account_page);

    const previousbtn = document.getElementById('previous-btn');
    previousbtn.addEventListener('click', previous_account_page);
});

function render_account_table(items) {
    const table = document.querySelector('table tbody');
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.remove();
    })

    items.forEach(item => {
        const new_row = document.createElement('tr');
        new_row.classList.add('h-12', 'bg-blue-gray-50', 'my-3', 'border-t', 'border-white');

        const datas = [item.Username, item.AccountNumber, item.AccountOwner.Name, item.Branch, item.Role, 
            item.TransferMethod, item.LoginMethod, item.Service]

        datas.forEach(data => {
            const cell = document.createElement('td')
            cell.innerHTML = data;
            cell.classList.add("p-2");

            new_row.appendChild(cell);
        })

        create_action_button(new_row)

        table.appendChild(new_row);
    })    

    const location = document.getElementById('location');
    location.innerHTML =  `${page}/${totalPage}`;
}


async function next_account_page(){
    if (page < totalPage) {
        page++;
        try {
            const data = await get_admin_page_data(page, 'account');
            totalPage = data.total_pages;
            render_account_table(data.items);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    }
}

async function previous_account_page(){
    if (page > 1) {
        page--;
        try {
            const data = await get_admin_page_data(page, 'account');
            totalPage = data.total_pages;
            render_account_table(data.items);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    } 
}

