import { get_admin_page_data, create_action_button } from './admin.js';

var page = 1;
var totalPage = 0;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const data = await get_admin_page_data(page, 'employee');
        totalPage = data.total_pages;
        render_table(data.items);
    } catch (error) {
        console.error('There was a problem with loading the items:', error);
    }

    const nextbtn = document.getElementById('next-btn');
    nextbtn.addEventListener('click', next_page);

    const previousbtn = document.getElementById('previous-btn');
    previousbtn.addEventListener('click', previous_page);
});

function render_table(items) {
    const table = document.querySelector('table tbody');
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.remove();
    })

    items.forEach(item => {
        const new_row = document.createElement('tr');
        new_row.classList.add('h-7', 'bg-blue-gray-50', 'my-3', 'border-t', 'border-white');

        const datas = [item.Username, "position",item.Role,"gender","0101010101", "this is an email", "this is an address", "9:00", 
            "18:00", "working_status", "670000 bilion"]

        var i = 0;
        datas.forEach(data => {
            const cell = document.createElement('td')
            cell.innerHTML = data;

            if (i == 6) {
                const span = document.createElement('span')
                span.innerHTML = 'i';
                span.classList.add('absolute', 'mx-1', 'font-bold');
                cell.appendChild(span);
                cell.classList.add('cursor-pointer', 'hover:bg-gray-400');
            }

            if(i==3 || i==4 || i==5 || i==6 || i==7 || i == 8 || i == 9 || i == 10){
                cell.classList.add('hidden')
                switch(i){
                    case 3:
                        cell.classList.add('2xl:table-cell');
                        break;
                    case 4:
                        cell.classList.add('sc-1220:table-cell');
                        break;
                    case 5:
                        cell.classList.add('xl:table-cell');
                        break;
                    case 6:
                        cell.classList.add('lg:table-cell');
                        break;
                    case 7:
                        cell.classList.add('sc-960:table-cell');
                        break;
                    case 8:
                        cell.classList.add('sc-860:table-cell');
                        break;
                    case 9:
                        cell.classList.add('md:table-cell');
                        break;
                    case 10:
                        cell.classList.add('sm:table-cell');
                        break;
                }
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


async function next_page(){
    console.log("next");
    if (page < totalPage) {
        page++;
        try {
            const data = await get_admin_page_data(page, 'employee');
            totalPage = data.total_pages;
            render_table(data.items);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    }
}

async function previous_page(){
    if (page > 1) {
        page--;
        try {
            const data = await get_admin_page_data(page, 'employee');
            totalPage = data.total_pages;
            render_table(data.items);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    } 
}



