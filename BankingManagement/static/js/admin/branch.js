import { get_admin_page_data, create_action_button } from './admin.js';

var page = 1;
var totalPage = 0;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const data = await get_admin_page_data(page, 'account');
        totalPage = data.total_pages;
        render_branch_table(data.items);
    } catch (error) {
        console.error('There was a problem with loading the items:', error);
    }

    const nextbtn = document.getElementById('next-btn');
    nextbtn.addEventListener('click', next_branch_page);

    const previousbtn = document.getElementById('previous-btn');
    previousbtn.addEventListener('click', previous_branch_page);
});

function render_branch_table(items) {
    const table = document.querySelector('table tbody');
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.remove();
    })

    items.forEach(item => {
        const new_row = document.createElement('tr');
        new_row.classList.add('h-7', 'bg-blue-gray-50', 'my-3', 'border-t', 'border-white');

        const datas = ["branch name", "This is address"];

        var i = 0;
        datas.forEach(data => {
            console.log(data);
            const cell = document.createElement('td')
            cell.innerHTML = data;

            if (i == 1) {
                const span = document.createElement('span')
                span.innerHTML = 'i';
                span.classList.add('absolute', 'mx-1', 'font-bold');
                cell.appendChild(span);
                cell.classList.add('cursor-pointer', 'hover:bg-gray-400');
            }

            cell.classList.add('p-2', 'relative', 'border-x', 'border-black','text-nowrap');
            new_row.appendChild(cell);
            i++;
        })

        create_action_button(new_row)

        table.appendChild(new_row);
    })    

    const location = document.getElementById('location');
    location.innerHTML =  `${page}/${totalPage}`;
}


async function next_branch_page(){
    if (page < totalPage) {
        page++;
        try {
            const data = await get_admin_page_data(page, 'branch');
            totalPage = data.total_pages;
            render_branch_table(data.items);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    }
}

async function previous_branch_page(){
    if (page > 1) {
        page--;
        try {
            const data = await get_admin_page_data(page, 'branch');
            totalPage = data.total_pages;
            render_branch_table(data.items);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    } 
}

