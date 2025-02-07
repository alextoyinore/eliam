document.addEventListener('DOMContentLoaded', function() {
    const tagInput = document.getElementById('tagInput');
    const tagDropdown = document.getElementById('tagDropdown');
    let allTags = [];

    // Load all tags initially
    fetch('/api/tags')
        .then(response => response.json())
        .then(tags => {
            allTags = tags;
        });

    // Show dropdown on focus
    tagInput.addEventListener('focus', function() {
        updateDropdown(this.value);
        tagDropdown.style.display = 'block';
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!tagInput.contains(e.target) && !tagDropdown.contains(e.target)) {
            tagDropdown.style.display = 'none';
        }
    });

    // Filter tags while typing
    tagInput.addEventListener('input', function() {
        updateDropdown(this.value);
    });

    function updateDropdown(inputValue) {
        const currentTags = inputValue.split(',').map(tag => tag.trim());
        const searchTerm = currentTags[currentTags.length - 1].toLowerCase();

        const filteredTags = allTags.filter(tag => 
            tag.toLowerCase().includes(searchTerm) && 
            !currentTags.slice(0, -1).includes(tag)
        );

        tagDropdown.innerHTML = filteredTags.map(tag => 
            `<div class="tag-item" onclick="addTag('${tag}')">${tag}</div>`
        ).join('');

        tagDropdown.style.display = filteredTags.length ? 'block' : 'none';
    }
});

function addTag(tagName) {
    const input = document.getElementById('tagInput');
    let currentTags = input.value.split(',').map(tag => tag.trim()).filter(tag => tag);
    
    // Remove the partial tag being typed
    currentTags.pop();
    
    if (!currentTags.includes(tagName)) {
        currentTags.push(tagName);
        input.value = currentTags.join(', ');
    }
    
    // Focus back on input and hide dropdown
    input.focus();
    document.getElementById('tagDropdown').style.display = 'none';
}

