/**
 * Employee Utilities JavaScript
 * Contains common functionality for employee pages
 */

// News type mapping
const newsTypes = {
    0: { name: "New", bgColor: "bg-green-100", textColor: "text-green-800" },
    1: { name: "Policy", bgColor: "bg-red-100", textColor: "text-red-800" },
    2: { name: "Event", bgColor: "bg-blue-100", textColor: "text-blue-800" },
    3: { name: "Announcement", bgColor: "bg-orange-100", textColor: "text-orange-800" }
};

// Format date function
const formatDate = dateString => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// News page functionality
function initializeNewsPage() {
    // Search functionality
    const searchNews = document.getElementById('searchNews');
    if (searchNews) {
        searchNews.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const newsItems = document.querySelectorAll('.news-item');
            
            newsItems.forEach(item => {
                const title = item.querySelector('h3').textContent.toLowerCase();
                const content = item.querySelector('p').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || content.includes(searchTerm)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Filter by type functionality
    const filterType = document.getElementById('filterType');
    if (filterType) {
        filterType.addEventListener('change', function(e) {
            const type = e.target.value;
            const newsItems = document.querySelectorAll('.news-item');
            
            newsItems.forEach(item => {
                const itemType = item.getAttribute('data-type');
                if (type === '-1' || itemType === type) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Filter by status functionality
    const filterStatus = document.getElementById('filterStatus');
    if (filterStatus) {
        filterStatus.addEventListener('change', function(e) {
            const status = e.target.value;
            const newsItems = document.querySelectorAll('.news-item');
            
            newsItems.forEach(item => {
                const itemStatus = item.querySelector('span').textContent.toLowerCase();
                if (status === '-1' || (status === '0' && itemStatus === 'new') || (status === '1' && itemStatus !== 'new')) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
}

// Modal functionality for news
function showNewsModal(newsId) {
    // Find the news item in the DOM
    const newsItem = document.querySelector(`.news-item[data-id="${newsId}"]`);
    if (!newsItem) return;
    
    // Get news data from the DOM
    const title = newsItem.querySelector('h3').textContent;
    const content = newsItem.querySelector('p').textContent;
    const dateText = newsItem.querySelector('.mt-2 span').textContent;
    const typeSpan = newsItem.querySelector('span');
    const typeClass = typeSpan.className;
    const typeText = typeSpan.textContent;
    
    // Update modal content
    document.getElementById('modalNewsType').className = typeClass;
    document.getElementById('modalNewsType').textContent = typeText;
    document.getElementById('modalNewsTitle').textContent = title;
    document.getElementById('modalNewsContent').textContent = content;
    document.getElementById('modalNewsDate').textContent = dateText;
    
    const modal = document.getElementById('newsModal');
    modal.classList.remove('hidden');
    
    if (typeText === "New") {
        typeSpan.className = typeClass.replace('bg-green-100', 'bg-gray-100').replace('text-green-800', 'text-gray-800');
        typeSpan.textContent = "Read";
    }
}

function closeNewsModal() {
    const modal = document.getElementById('newsModal');
    modal.classList.add('hidden');
}

// Working time page functionality
function initializeWorkingTimePage() {
    // Month selector change event
    const monthSelector = document.getElementById('monthSelector');
    if (monthSelector) {
        monthSelector.addEventListener('change', function() {
            window.location.href = `/employee/working-time?month=${this.value}`;
        });
    }

    // Export button click event
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            const month = document.getElementById('monthSelector').value;
            window.location.href = `/employee/working-time/export?month=${month}`;
        });
    }

    // Confirm button click event
    const confirmBtn = document.getElementById('confirmBtn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', function() {
            document.getElementById('confirmModal').classList.remove('hidden');
        });
    }

    // Cancel confirm button click event
    const cancelConfirmBtn = document.getElementById('cancelConfirmBtn');
    if (cancelConfirmBtn) {
        cancelConfirmBtn.addEventListener('click', function() {
            document.getElementById('confirmModal').classList.add('hidden');
        });
    }

    // Confirm submit button click event
    const confirmSubmitBtn = document.getElementById('confirmSubmitBtn');
    if (confirmSubmitBtn) {
        confirmSubmitBtn.addEventListener('click', function() {
            const month = document.getElementById('monthSelector').value;
            fetch(`/employee/working-time/confirm?month=${month}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Working time confirmed successfully!');
                    window.location.reload();
                } else {
                    alert('Failed to confirm working time: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while confirming working time.');
            })
            .finally(() => {
                document.getElementById('confirmModal').classList.add('hidden');
            });
        });
    }
}

// Initialize page based on current page
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the news page
    if (document.getElementById('searchNews')) {
        initializeNewsPage();
    }
    
    // Check if we're on the working time page
    if (document.getElementById('monthSelector')) {
        initializeWorkingTimePage();
    }
});