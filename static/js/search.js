document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const resultsTable = document.getElementById('resultsTable');
    const noResults = document.getElementById('noResults');

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const formData = {
                query: document.getElementById('searchQuery').value,
                fileType: document.getElementById('fileType').value,
                dateFrom: document.getElementById('dateFrom').value,
                dateTo: document.getElementById('dateTo').value,
                sortBy: document.getElementById('sortBy').value,
                sortOrder: document.getElementById('sortOrder').value
            };

            // Send search request
            fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                showError('An error occurred while searching. Please try again.');
            });
        });
    }

    function displayResults(results) {
        resultsTable.innerHTML = '';
        
        if (results.length === 0) {
            noResults.style.display = 'block';
            return;
        }
        
        noResults.style.display = 'none';
        
        results.forEach(result => {
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${result.name}</td>
                <td>${result.type}</td>
                <td>${formatFileSize(result.size)}</td>
                <td>${formatDate(result.date)}</td>
                <td>
                    <button class="btn btn-sm btn-primary btn-action" onclick="viewFile('${result.id}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-success btn-action" onclick="downloadFile('${result.id}')">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="btn btn-sm btn-danger btn-action" onclick="deleteFile('${result.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            
            resultsTable.appendChild(row);
        });
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }

    function showError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        searchForm.insertBefore(alertDiv, searchForm.firstChild);
    }
});

// File action functions
function viewFile(fileId) {
    window.location.href = `/view/${fileId}`;
}

function downloadFile(fileId) {
    window.location.href = `/download/${fileId}`;
}

function deleteFile(fileId) {
    if (confirm('Are you sure you want to delete this file?')) {
        fetch(`/api/files/${fileId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Refresh the search results
                document.getElementById('searchForm').dispatchEvent(new Event('submit'));
            } else {
                throw new Error('Failed to delete file');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete file. Please try again.');
        });
    }
} 