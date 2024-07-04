const table_structure = {
    account: [
        {key: 'Username', name: 'Username'}, 
        {key: 'AccountNumber', name: 'Account Number'}, 
        {key: 'Branch', name: 'Branch'}, 
        {key: "AccountOwner", name: 'Owner'}, 
        {key: 'Role', name: 'Role'}, 
        {key: 'TransferMethod', name: 'Transfer Method'}, 
        {key: 'LoginMethod', name: 'Login Method'}, 
        {key: 'Service', name: 'Service'}],
}

const styles = {
    cell: 'whitespace-nowrap p-2 relative border-x border-black',
    table: 'border border-black',
    table1: 'w-96 border border-black fixed z-10',
    table2: 'flex-1 ml-96 border border-black',
    th: 'text-left p-2 border border-black whitespace-nowrap',
    tr: 'h-8 bg-blue-gray-50 my-3 border-t border-white',
    table_wrapper: 'w-99% flex absolute top-32 overflow-x-auto',
    thead: 'bg-blue-gray-300',
}

document.addEventListener('DOMContentLoaded', async () => {
    const data_type = document.getElementById('dataType').value;

    try {
        const data = await get_admin_page_data(page, data_type);
        render_table(data.items, data_type);
    } catch (error) {
        console.error('There was a problem with loading the items:', error);
    }
});

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

export function create_action_button(row) {
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

var page = 1;

function render_table(items, data_type) { 

    const table_wrapper = document.getElementById('table_wrapper');
    style(table_wrapper, styles.table_wrapper);

    //get dataType for the table
    const col_names = table_structure[data_type]
    var items_length = col_names.length;

    if(items_length <= 3) { //if data has less than 4 field
        const table = document.createElement('table');
        style(table, styles.table);
        tableHeader(col_names, table);
        const tbody = document.createElement('tbody');
        table.appendChild(tbody);

        for(let i = 0; i < items_length; i++) {
            const row = document.createElement('tr');
            style(row, styles.tr);
            col_names.forEach(col_name => {
                const cell = document.createElement('td');
                style(cell, styles.cell);
                cell.innerHTML = items[i][col_name.key];
                row.appendChild(cell);
            })
            create_action_button(row);
            tbody.appendChild(row);
        }

        table_wrapper.appendChild(table1);
    }else {
        const col_names1 = col_names.slice(0, 3); //cols for left(fixed) table
        const col_names2 = col_names.slice(3, items_length);//cols for right table

        //fixed table
        const table1 = document.createElement('table');
        style(table1, styles.table1);
        tableHeader(col_names1, table1);
        const tbody1 = document.createElement('tbody');
        table1.appendChild(tbody1);

        //right table
        const table2 = document.createElement('table');
        style(table2, styles.table2);
        tableHeader(col_names2, table2);
        const tbody2 = document.createElement('tbody');
        table1.appendChild(tbody2);

        //loop to render fixed table
        for(let i = 0; i < items_length; i++) {
            const row = document.createElement('tr');
            style(row, styles.tr);
            col_names1.forEach(col_name => {
                const cell = document.createElement('td');
                style(cell, styles.cell);
                cell.innerHTML = items[i][col_name.key];
                row.appendChild(cell);
            })
            table1.appendChild(row);
        }

        //loop to render right table
        for(let i = 0; i < items_length; i++) {
            const row = document.createElement('tr');
            style(row, styles.tr);
            col_names2.forEach(col_name => {
                const cell = document.createElement('td');
                style(cell, styles.cell);
                cell.innerHTML = items[i][col_name.key];
                row.appendChild(cell);
            })
            create_action_button(row);
            table2.appendChild(row);
        }

        table_wrapper.appendChild(table1);
        table_wrapper.appendChild(table2);
    }
}

function tableHeader(col_names, table){
    const thead = document.createElement('thead');
    style(thead, styles.thead);
    col_names.forEach(col_name => {
        const th = document.createElement('th');
        style(th, styles.th);
        th.innerHTML = col_name.name;
        thead.appendChild(th);
    })
    const actionCol = document.createElement('th');
    actionCol.innerHTML = 'Action';

    table.appendChild(thead);
}

function style(element, classes) {
    classes.split(' ').forEach(function(cls) {
        element.classList.add(cls);
    });
}