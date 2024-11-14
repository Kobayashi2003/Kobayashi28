// Utility function for polling task status
async function pollTaskStatus(taskId, statusUrl, resultsDiv) {
    while (true) {
        try {
            const response = await fetch(`${statusUrl}${taskId}`);
            const data = await response.json();
            if (data.state === 'SUCCESS') {
                resultsDiv.textContent = JSON.stringify(data.result, null, 2);
                break;
            } else if (data.state === 'FAILURE') {
                resultsDiv.textContent = `Error: ${data.status || data.error}`;
                break;
            } else {
                resultsDiv.textContent = data.status;
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        } catch (error) {
            resultsDiv.textContent = `Error: ${error.message}`;
            break;
        }
    }
}

// Define status URLs for each operation
const statusUrls = {
    data: '/test/data/status/',
    crud: '/test/crud/status/',
    delete: '/test/delete/status/',
    cleanup: '/test/cleanup/status/',
    search: '/test/search/status/',
    update: '/test/update/status/',
    backup: '/test/backup/status/',
    restore: '/test/restore/status/'
};

// Utility function for form submission
async function handleFormSubmit(e, url, processData, operationType) {
    e.preventDefault();
    const resultsDiv = document.getElementById('results');
    resultsDiv.textContent = 'Processing...';
    const formData = new FormData(e.target);
    try {
        const data = processData ? processData(formData) : formData;
        const options = {
            method: 'POST',
            body: data instanceof FormData ? data : JSON.stringify(data),
            headers: data instanceof FormData ? {} : { 'Content-Type': 'application/json' },
        };
        const response = await fetch(url, options);
        const result = await response.json();
        if (result.task_id) {
            await pollTaskStatus(result.task_id, statusUrls[operationType], resultsDiv);
        } else {
            resultsDiv.textContent = JSON.stringify(result, null, 2);
        }
    } catch (error) {
        resultsDiv.textContent = `Error: ${error.message}`;
    }
}

// CRUD specific functions
function updateDataFields() {
    const operation = document.getElementById('operation').value;
    const dataFieldsDiv = document.getElementById('dataFields');
    dataFieldsDiv.innerHTML = '';

    if (operation === 'create' || operation === 'update') {
        dataFieldsDiv.appendChild(createFormGroup('id', 'ID:', true));
        dataFieldsDiv.appendChild(createFormGroup('data', 'Data (JSON):', true));
    } else {
        dataFieldsDiv.appendChild(createFormGroup('id', 'ID:', true));
    }
}

function createFormGroup(id, labelText, required = false) {
    const formGroup = document.createElement('div');
    formGroup.className = 'form-group';

    const label = document.createElement('label');
    label.htmlFor = id;
    label.textContent = labelText;

    const input = document.createElement('input');
    input.type = 'text';
    input.id = id;
    input.name = id;
    if (required) {
        input.required = true;
    }

    formGroup.appendChild(label);
    formGroup.appendChild(input);
    return formGroup;
}

// Search specific functions
function updateVisibleFields() {
    const searchTypeSelect = document.getElementById('searchType');
    const selectedType = searchTypeSelect.value;
    const searchFields = document.querySelectorAll('.search-fields');
    searchFields.forEach(field => {
        field.style.display = field.id === `${selectedType}Fields` ? 'block' : 'none';
    });
    document.getElementById('results').textContent = '';
}

function clearInputFields() {
    const inputs = document.querySelectorAll('input[type="text"], select');
    inputs.forEach(input => {
        if (input.id !== 'searchType' && input.id !== 'responseSize') {
            input.value = '';
        }
    });
}

// Main event listener
document.addEventListener('DOMContentLoaded', function() {
    // Data form
    const dataForm = document.getElementById('dataForm');
    if (dataForm) {
        dataForm.addEventListener('submit', e => handleFormSubmit(e, '/test/data', null, 'data'));
    }

    // CRUD form
    const crudForm = document.getElementById('crudForm');
    const operationSelect = document.getElementById('operation');
    const modelTypeSelect = document.getElementById('modelType');
    if (crudForm) {
        if (operationSelect && modelTypeSelect) {
            operationSelect.addEventListener('change', updateDataFields);
            modelTypeSelect.addEventListener('change', updateDataFields);
            updateDataFields();
        }
        crudForm.addEventListener('submit', e => handleFormSubmit(e, '/test/crud', formData => {
            const data = {
                operation: formData.get('operation'),
                modelType: formData.get('modelType'),
                id: formData.get('id')
            };
            if (data.operation === 'create' || data.operation === 'update') {
                try {
                    data.data = JSON.parse(formData.get('data'));
                } catch (error) {
                    throw new Error('Invalid JSON in data field');
                }
            }
            return data;
        }, 'crud'));
    }

    // Delete form
    const deleteForm = document.getElementById('deleteForm');
    if (deleteForm) {
        deleteForm.addEventListener('submit', e => handleFormSubmit(e, '/test/delete', null, 'delete'));
    }

    // Cleanup form
    const cleanupForm = document.getElementById('cleanupForm');
    if (cleanupForm) {
        cleanupForm.addEventListener('submit', e => handleFormSubmit(e, '/test/cleanup', formData => ({
            type: formData.get('type')
        }), 'cleanup'));
    }

    // Search form
    const searchForm = document.getElementById('searchForm');
    const searchTypeSelect = document.getElementById('searchType');
    if (searchForm) {
        if (searchTypeSelect) {
            searchTypeSelect.addEventListener('change', () => {
                updateVisibleFields();
                clearInputFields();
            });
        }
        searchForm.addEventListener('submit', e => {
            const searchFrom = document.body.dataset.searchType; // 'local' or 'remote'
            handleFormSubmit(e, `/test/search/${searchFrom}`, null, 'search');
        });
        // Initialize visible fields on page load
        updateVisibleFields();
    }

    // Update form
    const updateForm = document.getElementById('updateForm');
    if (updateForm) {
        updateForm.addEventListener('submit', e => handleFormSubmit(e, '/test/update', null, 'update'));
    }

    // Backup form
    const backupForm = document.getElementById('backupForm');
    if (backupForm) {
        backupForm.addEventListener('submit', e => handleFormSubmit(e, '/test/backup', formData => ({
            filename: formData.get('filename')
        }), 'backup'));
    }

    // Restore form
    const restoreForm = document.getElementById('restoreForm');
    if (restoreForm) {
        restoreForm.addEventListener('submit', e => handleFormSubmit(e, '/test/restore', formData => ({
            filename: formData.get('filename')
        }), 'restore'));
    }
});