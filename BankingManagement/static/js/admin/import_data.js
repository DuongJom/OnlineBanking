const dataType = document.getElementById("dataType").value;
var excelFile = null;

const getLogType = (logType, row_index, log) => {
    let icon = 'check_circle.svg';
    if(logType == "error") {
        icon = "error.svg";
    }

    const LogPattern = `
    <div class="mx-5 mb-2 border-2 border-${logType}_border bg-${logType}_bg flex items-center text-${logType}_text p-1">
        <div class="flex items-center border-r-2 border-${logType}_border pr-1">
            <div>
                <img src="${staticPath}${icon}" height="35px" width="35px"/>
            </div>
            <div>
                <p class="font-semibold">Row ${row_index}</p>
            </div>
        </div>

        <div>
            <p class="ml-1">
                ${log}
            </p>
        </div>
    </div>
    `;

    return LogPattern;
}

document.addEventListener("DOMContentLoaded", async () => {
    const excelInput = document.getElementById('excel_input');
    const fileNameDisplay = document.getElementById('file-name');
    const closeBtn = document.getElementById("closeResultPanelBtn");

    excelInput.addEventListener('change', function() {
        excelFile = this.files[0];
        const fileName = excelFile ? excelFile.name : 'Choose a file...';
        fileNameDisplay.textContent = fileName;
    })

    closeBtn.addEventListener('click', function() {
        const result_panel = document.getElementById("import_result");
        result_panel.classList.add("hidden");
    })
});

const handleImportResponse = (logs, total, success) => {

    const result_panel = document.getElementById("import_result");
    const logs_panel = document.getElementById("response_logs");
    const result_text = document.getElementById("result_text");
    const importForm = document.getElementById("importForm");

    result_panel.classList.remove('hidden');
    
    logs_panel.innerHTML = '';
    logs.forEach(log => {
        logs_panel.innerHTML += getLogType(log.status, log.row_index, log.message);
    })

    result_text.innerHTML = `${success}/${total} tuple was created!`;
    importForm.classList.remove('flex');
    importForm.classList.add('hidden');
}

window.importData = () => {
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    let url = 'import';
    const formData = new FormData();
    formData.append('file', excelFile);

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        body: formData
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
        }
        return response.json();
    })
    .then((data) => {
        handleImportResponse(data.logs, data.total, data.success_create);
        return data;
    })
    .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
    });
}