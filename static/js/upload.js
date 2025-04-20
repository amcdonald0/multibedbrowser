document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const progressBar = document.querySelector('.progress');
    const progressBarInner = document.querySelector('.progress-bar');
    const uploadStatusTable = document.getElementById('uploadStatusTable');

    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            const files = document.getElementById('fileInput').files;
            const projectName = document.getElementById('projectName').value;
            const fileType = document.getElementById('fileType').value;
            const description = document.getElementById('fileDescription').value;
            
            // Add form data
            formData.append('projectName', projectName);
            formData.append('fileType', fileType);
            formData.append('description', description);
            
            // Add files
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }
            
            // Show progress bar
            progressBar.style.display = 'block';
            
            // Clear previous status
            uploadStatusTable.innerHTML = '';
            
            // Create status rows for each file
            for (let i = 0; i < files.length; i++) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${files[i].name}</td>
                    <td>${formatFileSize(files[i].size)}</td>
                    <td class="status-pending">Pending</td>
                    <td>0%</td>
                `;
                uploadStatusTable.appendChild(row);
            }
            
            // Send upload request
            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                updateUploadStatus(data);
            })
            .catch(error => {
                console.error('Error:', error);
                showError('An error occurred while uploading files. Please try again.');
            });
        });
    }

    function updateUploadStatus(data) {
        // Update progress bar
        progressBarInner.style.width = `${data.overallProgress}%`;
        
        // Update status for each file
        data.files.forEach((file, index) => {
            const row = uploadStatusTable.children[index];
            if (row) {
                const statusCell = row.children[2];
                const progressCell = row.children[3];
                
                statusCell.textContent = file.status;
                statusCell.className = `status-${file.status.toLowerCase()}`;
                progressCell.textContent = `${file.progress}%`;
            }
        });
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function showError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        uploadForm.insertBefore(alertDiv, uploadForm.firstChild);
    }
}); 