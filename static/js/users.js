document.addEventListener('DOMContentLoaded', function() {
    loadUserData();
    const userSearch = document.getElementById('userSearch');
    const usersTable = document.getElementById('usersTable');
    
    if (userSearch) {
        userSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = usersTable.getElementsByTagName('tr');
            
            for (let row of rows) {
                const username = row.cells[0].textContent.toLowerCase();
                const email = row.cells[1].textContent.toLowerCase();
                
                if (username.includes(searchTerm) || email.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            }
        });
    }
});

function loadUserData() {
    fetch('/api/users')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(users => {
        const tableBody = document.getElementById('usersTable');
        tableBody.innerHTML = '';

        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>
                    <span class="badge ${user.role === 'admin' ? 'bg-danger' : 'bg-primary'}">
                        ${user.role}
                    </span>
                </td>
                <td>
                    <span class="badge ${user.is_active ? 'bg-success' : 'bg-secondary'}">
                        ${user.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>${user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}</td>
                ${current_user.is_admin ? `
                <td>
                    <button class="btn btn-sm btn-info" onclick="editUser('${user.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteUser('${user.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
                ` : ''}
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error loading user data:', error);
        showError('Error loading user data. Please try again later.');
    });
}

function submitNewUser() {
    const form = document.getElementById('addUserForm');
    const formData = new FormData(form);
    
    fetch('/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password'),
            role: formData.get('role')
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Close modal and refresh page
            const modal = bootstrap.Modal.getInstance(document.getElementById('addUserModal'));
            modal.hide();
            location.reload();
        } else {
            showError(data.message || 'Failed to add user');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('An error occurred while adding the user');
    });
}

function editUser(userId) {
    // Fetch user data
    fetch(`/api/users/${userId}`)
    .then(response => response.json())
    .then(user => {
        // Populate edit form
        document.getElementById('editUsername').value = user.username;
        document.getElementById('editEmail').value = user.email;
        document.getElementById('editRole').value = user.role;
        
        // Show edit modal
        const editModal = new bootstrap.Modal(document.getElementById('editUserModal'));
        editModal.show();
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Failed to load user data');
    });
}

function updateUser(userId) {
    const form = document.getElementById('editUserForm');
    const formData = new FormData(form);
    
    fetch(`/api/users/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: formData.get('username'),
            email: formData.get('email'),
            role: formData.get('role')
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Close modal and refresh page
            const modal = bootstrap.Modal.getInstance(document.getElementById('editUserModal'));
            modal.hide();
            location.reload();
        } else {
            showError(data.message || 'Failed to update user');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('An error occurred while updating the user');
    });
}

function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        fetch(`/api/users/${userId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                showError(data.message || 'Failed to delete user');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('An error occurred while deleting the user');
        });
    }
}

function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.querySelector('.users-container').insertBefore(alertDiv, document.querySelector('.user-actions'));
} 