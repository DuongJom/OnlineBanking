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

// Search functionality
document.getElementById('searchNews').addEventListener('input', function(e) {
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

// Filter by type functionality
document.getElementById('filterType').addEventListener('change', function(e) {
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

// Filter by status functionality
document.getElementById('filterStatus').addEventListener('change', function(e) {
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

// Modal functionality
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