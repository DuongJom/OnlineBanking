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

