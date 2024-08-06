import { styles, table_structure } from "./config.js";

export function get_salary_page_data() {
    return fetch(`/employee/salary`, {
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
//salaries=[{},{}]
export function render_table(items, data_type = 'salary') { 
    const tables = document.querySelectorAll('table');
    const table_wrapper = document.getElementById('table_wrapper');
    const col_names = table_structure[data_type];
    const items_length = col_names.length;
    const location = document.getElementById('location');
    const col_names1 = col_names.slice(0, 3); //cols for left(fixed) table
    const col_names2 = col_names.slice(3, items_length);//cols for right table
    const table1 = document.createElement('table');
    const tbody1 = document.createElement('tbody');
    const table2 = document.createElement('table');
    const tbody2 = document.createElement('tbody');

    tables.forEach(table => {
        table.remove();
    })
    
    style(table_wrapper, styles.table_wrapper);
    
    location.innerHTML =  `${localStorage.getItem('salary_page')}/${localStorage.getItem('salary_maxPage')}`;

    //get dataType for the table
    if(items_length <= 3) { //if table has less than 4 columns
        const table = document.createElement('table');
        const tbody = document.createElement('tbody');

        style(table, styles.table);
        tableHeader(col_names, table, false);
        table.appendChild(tbody);

        for(let i = 0; i < items.length; i++) {
            const row = document.createElement('tr');
            style(row, styles.tr);
            col_names.forEach(col_name => {
                const cell = document.createElement('td');
                style(cell, styles.cell);
                cell.innerHTML = items[i][col_name.key];
                if(typeof items[i][col_name.key] == 'object') {
                    generateObjectSign(cell);
                }
                row.appendChild(cell);
            })
            create_action_button(row);
            tbody.appendChild(row);
        }

        table_wrapper.appendChild(table);
        return
    }

    //if table has greater than or equal to 4 columns
    //fixed table
    table1.id = 'table1';
    tableHeader(col_names1, table1, true);
    table1.appendChild(tbody1);

    //right table
    table2.id = 'table2';
    tableHeader(col_names2, table2, false);
    table2.appendChild(tbody2);

    //loop to render fixed table
    for(let i = 0; i < items.length; i++) {
        const row = document.createElement('tr');
        style(row, styles.tr);
        col_names1.forEach(col_name => {
            const cell = document.createElement('td');
            style(cell, styles.cell);
            cell.innerHTML = items[i][col_name.key];
            if(typeof items[i][col_name.key] == 'object') {
                generateObjectSign(cell);
            }
            row.appendChild(cell);       
        })
        tbody1.appendChild(row);
    }

    //loop to render right table
    for(let i = 0; i < items.length; i++) {
        const row = document.createElement('tr');
        style(row, styles.tr);
        col_names2.forEach(col_name => {
            const cell = document.createElement('td');
            style(cell, styles.cell);
            cell.innerHTML = items[i][col_name.key];
            if(typeof items[i][col_name.key] == 'object') {
                generateObjectSign(cell);
            }
            row.appendChild(cell);
        })
        create_action_button(row);
        tbody2.appendChild(row);
    }

    table_wrapper.appendChild(table1);
    style(table1, styles.table1);
    style(table2, styles.table2);
    table_wrapper.appendChild(table2);
    adjustTableMargin();
}

function tableHeader(col_names, table, isFixed){
    const thead = document.createElement('thead');

    style(thead, styles.thead);
    col_names.forEach(col_name => {
        const th = document.createElement('th');
        style(th, styles.th);
        th.innerHTML = col_name.name;
        thead.appendChild(th);
    })

    if(!isFixed) {
        const action_col = document.createElement('th');

        action_col.innerHTML = 'Action'
        style(action_col, styles.th);
        thead.appendChild(action_col);
    }

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

export async function next(data_type){
    var page = localStorage.getItem('salary_page');
    var max_page = localStorage.getItem('salary_maxPage');

    if (page < max_page) {
        page++;
        localStorage.setItem('salary_page', page);
        try {
            const data = await get_salary_page_data(page, data_type);

            localStorage.setItem('salary_maxPage', data.total_pages);
            render_table(data.items, data_type);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    }
}

export async function previous(data_type, page){
    var page = localStorage.getItem('salary_page');

    if (page > 1) {
        page--;
        localStorage.setItem('salary_page', page);
        try {
            const data = await get_salary_page_data(page, data_type);
            localStorage.setItem('salary_maxPage', data.total_pages);
            render_table(data.items, data_type);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    } 
}

export function adjustTableMargin() {
    const table1 = document.getElementById('table1');
    const table2 = document.getElementById('table2');
    
    if (window.innerWidth >= 700) {
        table2.style.marginLeft = `${table1.offsetWidth - 2}px`;
    } else {
        table2.style.marginLeft = '0px';
    }
}

