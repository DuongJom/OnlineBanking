import { styles, table_structure } from "./config.js";

export function get_admin_page_data(page, dataType) {
    return fetch(`/admin?page=${page}&dataType=${dataType}`, {
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

function create_action_button(row) {
    const action_cell = document.createElement('td');
    action_cell.classList.add('border-x', 'border-black')
    const div = document.createElement('div');
    div.classList.add('flex', 'justify-center')
    const view_btn = document.createElement('button');
    const delete_btn = document.createElement('button');
    const edit_btn = document.createElement('button');

    const btn_list = [view_btn, delete_btn, edit_btn];
    const icon_list = ['visibility', 'delete', 'edit']

    let i = 0;
    btn_list.forEach(btn => {
        btn.classList.add('flex','items-center', 'justify-center')
        const span = document.createElement('span');
        span.classList.add('material-symbols-outlined', 'hover:bg-gray-500', 'rounded');
        span.style.fontWeight = '300';
        span.innerHTML = icon_list[i];
        btn.appendChild(span);
        div.appendChild(btn);
        i++;
    })

    action_cell.appendChild(div);
    row.appendChild(action_cell);
}

export function render_table(items, data_type, page, total_pages) { 
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        table.remove();
    })

    const table_wrapper = document.getElementById('table_wrapper');
    style(table_wrapper, styles.table_wrapper);

    //get dataType for the table
    const col_names = table_structure[data_type]
    var items_length = col_names.length;

    if(items_length <= 3) { //if data has less than 4 field
        const table = document.createElement('table');
        style(table, styles.table);
        tableHeader(col_names, table, false);
        const tbody = document.createElement('tbody');
        table.appendChild(tbody);

        for(let i = 0; i < items.length; i++) {
            const row = document.createElement('tr');
            style(row, styles.tr);
            col_names.forEach(col_name => {
                const cell = document.createElement('td');
                style(cell, styles.cell);
                cell.innerHTML = items[i][col_name.key];
                if(typeof items[i][col_name.key] == 'object') {
                    objectSign(cell);
                }
                row.appendChild(cell);
            })
            create_action_button(row);
            tbody.appendChild(row);
        }

        table_wrapper.appendChild(table);
    }else {
        const col_names1 = col_names.slice(0, 3); //cols for left(fixed) table
        const col_names2 = col_names.slice(3, items_length);//cols for right table

        //fixed table
        const table1 = document.createElement('table');   
        table1.id = 'table1';
        tableHeader(col_names1, table1, true);
        const tbody1 = document.createElement('tbody');
        table1.appendChild(tbody1);

        //right table
        const table2 = document.createElement('table');
        table2.id = 'table2';
        tableHeader(col_names2, table2, false);
        const tbody2 = document.createElement('tbody');
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
                    objectSign(cell);
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
                    objectSign(cell);
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
    const location = document.getElementById('location');
    location.innerHTML =  `${localStorage.getItem('admin_page')}/${localStorage.getItem('admin_maxPage')}`;
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

function objectSign(cell) {
    const span = document.createElement('span')
    span.innerHTML = 'i';
    span.classList.add('font-bold','ml-3');
    cell.appendChild(span);
    cell.classList.add('cursor-pointer', 'hover:bg-gray-400');
}

export async function next(data_type){
    var page = localStorage.getItem('admin_page');
    var max_page = localStorage.getItem('admin_maxPage');
    if (page < max_page) {
        page++;
        localStorage.setItem('admin_page', page);
        try {
            const data = await get_admin_page_data(page, data_type);
            console.log(data.items);
            localStorage.setItem('admin_maxPage', data.total_pages);
            render_table(data.items, data_type, page, max_page);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    }
}

export async function previous(data_type, page, max_page){
    var page = localStorage.getItem('admin_page');
    var max_page = localStorage.getItem('admin_maxPage');
    if (page > 1) {
        page--;
        localStorage.setItem('admin_page', page);
        try {
            const data = await get_admin_page_data(page, data_type);
            localStorage.setItem('admin_maxPage', data.total_pages);
            render_table(data.items, data_type, page, max_page);
        } catch (error) {
            console.error('There was a problem with loading the items:', error);
        }
    } 
}

export function adjustTableMargin() {
    const table1 = document.getElementById('table1');
    const table2 = document.getElementById('table2');
    console.log(window.innerWidth)
;    if (window.innerWidth >= 700) {
        table2.style.marginLeft = `${table1.offsetWidth - 2}px`;
    } else {
        table2.style.marginLeft = '0px';
    }
}