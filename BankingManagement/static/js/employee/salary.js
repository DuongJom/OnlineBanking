import { styles, table_structure } from "./config.js";
const currentYear = document.getElementById('year');
function get_salary_page_data(page, dataType, year = currentYear) {
    return fetch(`/employee?page=${page}&dataType=${dataType}&year=${year}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        return data;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

/* 
    columns will be months
    rows will be table_structure[data_type]
*/
function render_table(items, data_type = 'salary') { 
    const tables = document.querySelectorAll('table');
    const table_wrapper = document.getElementById('table_wrapper');
    const col_names = items.map(item => item.month);
    col_names.unshift(table_structure[data_type][0]['name'])
    const row_names = table_structure[data_type].slice(1);
    const location = document.getElementById('location');
    tables.forEach(table => {
        table.remove();
    })
    
    style(table_wrapper, styles.table_wrapper);
    
    location.innerHTML =  `${localStorage.getItem('salary_page')}/${localStorage.getItem('salary_maxPage')}`;

    const table = document.createElement('table');
    const tbody = document.createElement('tbody');

    style(table, styles.table);
    tableHeader(col_names, table);
    table.appendChild(tbody);
/*
    loop through items.elements, get properties of the table_structure and put it in the row data
    fill in the first column
    get the data of each month and insert to each row that we want 
*/
    for(let i = 0; i < row_names.length; i++) {
        const row = document.createElement('tr');
        style(row, styles.tr);
        const cell1 = document.createElement('td');
        cell1.innerHTML = row_names[i].name;
        row.appendChild(cell1);

        //fill data in the table sequently 
        items.forEach(item => {
            const cell = document.createElement('td');
            style(cell, styles.cell);
            cell.innerHTML = item[row_names[i].key];
            row.appendChild(cell);
        })
        tbody.appendChild(row);
    }

    table_wrapper.appendChild(table);
    return

}

function tableHeader(col_names, table){
    const thead = document.createElement('thead');

    style(thead, styles.thead);
    col_names.forEach(col_name => {
        const th = document.createElement('th');
        style(th, styles.th);
        th.innerHTML = col_name;
        thead.appendChild(th);
    })

    table.appendChild(thead);
}

function style(element, classes) {
    classes.split(' ').forEach(function(cls) {
        element.classList.add(cls);
    });
}

function generateObjectSign(cell) {
    const icon = document.createElement('div')

    icon.innerHTML = 'i';
    icon.classList.add('font-bold');
    icon.classList.add('w-5', 'h-5', 'bg-popup-bg', 'inline-block', 'rounded-full', 'text-center', 'leading-5', 'ml-4');
    cell.appendChild(icon);
    cell.classList.add('cursor-pointer', 'hover:bg-gray-400');
}

async function next(data_type, year) {
    // Retrieve and convert 'page' and 'max_page' to numbers
    let page = parseInt(localStorage.getItem('salary_page'), 10);
    const max_page = parseInt(localStorage.getItem('salary_maxPage'), 10);

    // Compare page with max_page as numbers
    if (page < max_page) {
        page++;  // Increment the page number
        localStorage.setItem('salary_page', page);

        try {
            // Fetch the data for the next page
            const data = await get_salary_page_data(page, data_type, year);

            // Update max_page in localStorage if necessary
            localStorage.setItem('salary_maxPage', data.total_pages);

            // Re-render the table with the new data
            render_table(data.items, data_type);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    }
}


async function previous(data_type, year) {
    // Retrieve and convert 'page' to a number
    let page = parseInt(localStorage.getItem('salary_page'), 10);

    // Check if the page number is greater than 1
    if (page > 1) {
        page--;  // Decrement the page number
        localStorage.setItem('salary_page', page);

        try {
            // Fetch the data for the previous page
            const data = await get_salary_page_data(page, data_type, year);

            // Update max_page in localStorage if necessary
            localStorage.setItem('salary_maxPage', data.total_pages);

            // Re-render the table with the new data
            render_table(data.items, data_type);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    } 
}

document.addEventListener('DOMContentLoaded', async () => {
    const data_type = document.getElementById('dataType').value;
    const next_btn = document.getElementById('next-btn');
    const previous_btn = document.getElementById('previous-btn');
    const yearEl = document.getElementById('year');
    const year = yearEl.value;

    localStorage.setItem('salary_page', 1);

    try {
        let data = await get_salary_page_data(1, data_type, year);
        console.log(data);

        yearEl.addEventListener('change', async (e) => {
            e.preventDefault();
            data = await get_salary_page_data(1, data_type, year);
            render_table(data.items, data_type);
            next_btn.addEventListener('click', () => next(data_type, year));
            previous_btn.addEventListener('click', () => previous(data_type, year));
        })
        
        localStorage.setItem('salary_maxPage', 1)
        render_table(data.items, data_type);
    } catch (error) {
        console.error('There was a problem with loading the items:', error);
    }

    next_btn.addEventListener('click', () => next(data_type, year));
    previous_btn.addEventListener('click', () => previous(data_type, year));
    //can add the adjustTableMargin() to the code later 
});
