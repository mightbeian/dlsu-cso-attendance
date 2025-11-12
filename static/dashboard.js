// Dashboard JavaScript
// Main attendance and user management functionality

// DOM Elements
const idNumberInput = document.getElementById('idNumber');
const messageArea = document.getElementById('messageArea');
const messageText = document.getElementById('messageText');
const userPhotoContainer = document.getElementById('userPhotoContainer');
const userPhoto = document.getElementById('userPhoto');
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const adminBtn = document.getElementById('adminBtn');
const adminModal = document.getElementById('adminModal');
const modalClose = document.querySelector('.close');

// Statistics
const activeCount = document.getElementById('activeCount');
const totalUsers = document.getElementById('totalUsers');
const loggedInToday = document.getElementById('loggedInToday');
const currentTime = document.getElementById('currentTime');

// Tab management
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Forms
const addUserForm = document.getElementById('addUserForm');
const exportBtn = document.getElementById('exportBtn');
const manageSearchInput = document.getElementById('manageSearchInput');
const usersList = document.getElementById('usersList');

// ============ UTILITY FUNCTIONS ============

function showMessage(message, type = 'success') {
    messageArea.className = 'message-area ' + type;
    messageText.textContent = message;
    messageArea.classList.remove('hidden');
    
    setTimeout(() => {
        messageArea.classList.add('hidden');
    }, 5000);
}

function clearInput() {
    idNumberInput.value = '';
    idNumberInput.focus();
}

async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            return data;
        }
        
        if (!response.ok) {
            throw new Error('Request failed');
        }
        
        return response;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ============ ATTENDANCE FUNCTIONALITY ============

async function handleAttendance() {
    const id_number = idNumberInput.value.trim();
    
    if (!id_number) {
        showMessage('Please enter your ID Number', 'error');
        return;
    }
    
    try {
        const result = await apiCall('/api/attendance', {
            method: 'POST',
            body: JSON.stringify({ id_number })
        });
        
        if (result.success) {
            const messageType = result.is_birthday ? 'birthday' : 'success';
            showMessage(result.message, messageType);
            
            // Show user photo if available
            if (result.user.photo_filename) {
                userPhoto.src = `/static/photos/${result.user.photo_filename}`;
                userPhotoContainer.classList.remove('hidden');
                userPhoto.style.display = 'block';
                userPhoto.nextElementSibling.style.display = 'none';
            } else {
                userPhotoContainer.classList.remove('hidden');
                userPhoto.style.display = 'none';
                userPhoto.nextElementSibling.style.display = 'flex';
            }
            
            // Hide photo after 5 seconds
            setTimeout(() => {
                userPhotoContainer.classList.add('hidden');
            }, 5000);
            
            clearInput();
            refreshActiveUsers();
            updateStats();
        }
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Enter key handler
idNumberInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleAttendance();
    }
});"
  }, {"path": "static/dashboard.js", "content": "// Dashboard JavaScript - Part 2\n\n// ============ ACTIVE USERS SIDEBAR ============\n\nasync function refreshActiveUsers() {\n    try {\n        const data = await apiCall('/api/active-users');\n        let totalActive = 0;\n        \n        Object.keys(data).forEach(committee => {\n            const users = data[committee];\n            const committeeId = committee.replace(/ /g, '-').toLowerCase();\n            const container = document.getElementById(`committee-${committeeId}`);\n            const countBadge = document.querySelector(`[data-committee=\"${committee}\"]`);\n            \n            if (users.length === 0) {\n                container.innerHTML = '<p class=\"no-users\">No active users</p>';\n                countBadge.textContent = '0';\n            } else {\n                container.innerHTML = users.map(user => `\n                    <div class=\"user-item\">\n                        ${user.photo_filename ? \n                            `<img src=\"/static/photos/${user.photo_filename}\" class=\"user-item-photo\" alt=\"${user.full_name}\">` :\n                            `<div class=\"user-item-placeholder\"><i class=\"fas fa-user\"></i></div>`\n                        }\n                        <div class=\"user-item-info\">\n                            <div class=\"user-item-name\">${user.full_name}</div>\n                            <div class=\"user-item-time\">Since ${user.time_in}</div>\n                        </div>\n                    </div>\n                `).join('');\n                \n                countBadge.textContent = users.length;\n                totalActive += users.length;\n            }\n        });\n        \n        activeCount.textContent = totalActive;\n    } catch (error) {\n        console.error('Error refreshing active users:', error);\n    }\n}\n\n// ============ SEARCH FUNCTIONALITY ============\n\nlet searchTimeout;\nsearchInput.addEventListener('input', () => {\n    clearTimeout(searchTimeout);\n    const query = searchInput.value.trim();\n    \n    if (query.length < 2) {\n        searchResults.classList.add('hidden');\n        return;\n    }\n    \n    searchTimeout = setTimeout(async () => {\n        try {\n            const users = await apiCall(`/api/users/search?q=${encodeURIComponent(query)}`);\n            \n            if (users.length === 0) {\n                searchResults.innerHTML = '<div class=\"search-result-item\">No users found</div>';\n            } else {\n                searchResults.innerHTML = users.map(user => `\n                    <div class=\"search-result-item\" data-id=\"${user.id_number}\">\n                        <div class=\"search-result-name\">${user.full_name}</div>\n                        <div class=\"search-result-details\">\n                            ID: ${user.id_number} | ${user.committee}\n                        </div>\n                    </div>\n                `).join('');\n                \n                // Add click handlers\n                document.querySelectorAll('.search-result-item').forEach(item => {\n                    item.addEventListener('click', () => {\n                        idNumberInput.value = item.dataset.id;\n                        searchResults.classList.add('hidden');\n                        searchInput.value = '';\n                        idNumberInput.focus();\n                    });\n                });\n            }\n            \n            searchResults.classList.remove('hidden');\n        } catch (error) {\n            console.error('Search error:', error);\n        }\n    }, 300);\n});\n\n// Close search results when clicking outside\ndocument.addEventListener('click', (e) => {\n    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {\n        searchResults.classList.add('hidden');\n    }\n});\n\n// ============ ADMIN MODAL ============\n\nadminBtn.addEventListener('click', () => {\n    adminModal.classList.remove('hidden');\n    loadManageUsers();\n});\n\nmodalClose.addEventListener('click', () => {\n    adminModal.classList.add('hidden');\n});\n\nwindow.addEventListener('click', (e) => {\n    if (e.target === adminModal) {\n        adminModal.classList.add('hidden');\n    }\n});\n\n// Tab switching\ntabBtns.forEach(btn => {\n    btn.addEventListener('click', () => {\n        const tabName = btn.dataset.tab;\n        \n        tabBtns.forEach(b => b.classList.remove('active'));\n        tabContents.forEach(c => c.classList.remove('active'));\n        \n        btn.classList.add('active');\n        document.getElementById(`${tabName}-tab`).classList.add('active');\n        \n        if (tabName === 'manage-users') {\n            loadManageUsers();\n        }\n    });\n});\n\n// ============ EXPORT DTR ============\n\nexportBtn.addEventListener('click', () => {\n    window.location.href = '/api/export-dtr';\n});\n\n// ============ ADD USER FORM ============\n\naddUserForm.addEventListener('submit', async (e) => {\n    e.preventDefault();\n    \n    const formData = {\n        id_number: document.getElementById('newIdNumber').value.trim(),\n        full_name: document.getElementById('newFullName').value.trim(),\n        birthday: document.getElementById('newBirthday').value.trim(),\n        committee: document.getElementById('newCommittee').value\n    };\n    \n    try {\n        const result = await apiCall('/api/users', {\n            method: 'POST',\n            body: JSON.stringify(formData)\n        });\n        \n        alert(result.message);\n        addUserForm.reset();\n        \n        // Handle photo upload if provided\n        const photoInput = document.getElementById('newPhoto');\n        if (photoInput.files.length > 0) {\n            const photoFormData = new FormData();\n            photoFormData.append('photo', photoInput.files[0]);\n            \n            try {\n                await fetch(`/api/users/${result.user.id}/photo`, {\n                    method: 'POST',\n                    body: photoFormData\n                });\n            } catch (photoError) {\n                console.error('Photo upload error:', photoError);\n                alert('User added but photo upload failed');\n            }\n        }\n        \n        updateStats();\n        \n    } catch (error) {\n        alert('Error: ' + error.message);\n    }\n});\n\n// ============ MANAGE USERS ============\n\nasync function loadManageUsers() {\n    try {\n        const users = await apiCall('/api/users');\n        displayUsersList(users);\n    } catch (error) {\n        usersList.innerHTML = '<p class=\"error\">Error loading users</p>';\n    }\n}\n\nfunction displayUsersList(users) {\n    if (users.length === 0) {\n        usersList.innerHTML = '<p>No users found</p>';\n        return;\n    }\n    \n    usersList.innerHTML = users.map(user => `\n        <div class=\"user-list-item\">\n            <div class=\"user-list-info\">\n                <div class=\"user-list-name\">${user.full_name}</div>\n                <div class=\"user-list-details\">\n                    ID: ${user.id_number} | ${user.committee} | Birthday: ${user.birthday}\n                </div>\n            </div>\n            <button class=\"delete-btn\" data-id=\"${user.id}\" data-name=\"${user.full_name}\">\n                <i class=\"fas fa-trash\"></i> Delete\n            </button>\n        </div>\n    `).join('');\n    \n    // Add delete handlers\n    document.querySelectorAll('.delete-btn').forEach(btn => {\n        btn.addEventListener('click', () => deleteUser(btn.dataset.id, btn.dataset.name));\n    });\n}\n\nmanageSearchInput.addEventListener('input', async () => {\n    const query = manageSearchInput.value.trim();\n    \n    try {\n        if (query.length === 0) {\n            const users = await apiCall('/api/users');\n            displayUsersList(users);\n        } else {\n            const users = await apiCall(`/api/users/search?q=${encodeURIComponent(query)}`);\n            displayUsersList(users);\n        }\n    } catch (error) {\n        console.error('Search error:', error);\n    }\n});\n\nasync function deleteUser(userId, userName) {\n    if (!confirm(`Are you sure you want to delete ${userName}?\\n\\nThis will also delete all attendance records for this user.`)) {\n        return;\n    }\n    \n    try {\n        const result = await apiCall(`/api/users/${userId}`, {\n            method: 'DELETE'\n        });\n        \n        alert(result.message);\n        loadManageUsers();\n        updateStats();\n        refreshActiveUsers();\n    } catch (error) {\n        alert('Error: ' + error.message);\n    }\n}\n\n// ============ STATISTICS ============\n\nasync function updateStats() {\n    try {\n        const users = await apiCall('/api/users');\n        totalUsers.textContent = users.length;\n        \n        // Count users who logged in today\n        // This is a simplified version - you might want to add a backend endpoint for this\n        const activeData = await apiCall('/api/active-users');\n        let todayCount = 0;\n        Object.values(activeData).forEach(committee => {\n            todayCount += committee.length;\n        });\n        loggedInToday.textContent = todayCount;\n        \n    } catch (error) {\n        console.error('Error updating stats:', error);\n    }\n}\n\n// Update current time\nfunction updateTime() {\n    const now = new Date();\n    currentTime.textContent = now.toLocaleTimeString('en-US', {\n        hour: '2-digit',\n        minute: '2-digit'\n    });\n}\n\n// ============ INITIALIZATION ============\n\ndocument.addEventListener('DOMContentLoaded', () => {\n    refreshActiveUsers();\n    updateStats();\n    updateTime();\n    \n    // Refresh active users every 10 seconds\n    setInterval(refreshActiveUsers, 10000);\n    \n    // Update time every second\n    setInterval(updateTime, 1000);\n    \n    // Focus on ID input\n    idNumberInput.focus();\n});\n\n// Refocus input when page becomes visible\ndocument.addEventListener('visibilitychange', () => {\n    if (!document.hidden) {\n        idNumberInput.focus();\n    }\n});\n"}]