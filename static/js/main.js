document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebar = document.getElementById('sidebar');

    // Toggle sidebar
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.add('active');
        });
    }

    // Close sidebar
    if (sidebarClose) {
        sidebarClose.addEventListener('click', function() {
            sidebar.classList.remove('active');
        });
    }

    // Close sidebar when clicking outside
    if (sidebar) {
        document.addEventListener('click', function(event) {
            if (!sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) {
                sidebar.classList.remove('active');
            }
        });
    }
    
    // Course filtering functionality
    initializeCourseFiltering();
});

function initializeCourseFiltering() {
    console.log('Initializing course filtering');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const courseCards = document.querySelectorAll('.course-card');
    
    if (filterButtons.length === 0 || courseCards.length === 0) {
        console.log('No filter buttons or course cards found');
        return; // Exit if elements don't exist
    }
    
    console.log('Found filter buttons:', filterButtons.length);
    console.log('Found course cards:', courseCards.length);
    
    // Debug: Log all filter buttons and their categories
    filterButtons.forEach(btn => {
        console.log('Filter button:', btn.textContent, 'Category:', btn.getAttribute('data-category'));
    });
    
    // Debug: Log all course cards and their categories
    courseCards.forEach(card => {
        console.log('Course card:', card.querySelector('.course-name')?.textContent, 'Category:', card.getAttribute('data-category'));
    });
    
    // Set initial state - show all courses
    const allButton = document.querySelector('.filter-btn[data-category="all"]');
    if (allButton) {
        allButton.classList.add('active');
    } else {
        // If no "all" button, activate the first button
        filterButtons[0]?.classList.add('active');
    }
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const category = button.getAttribute('data-category')?.toLowerCase();
            console.log('Filter clicked:', category);
            
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            // Filter courses
            let visibleCount = 0;
            courseCards.forEach(card => {
                const cardCategory = card.getAttribute('data-category')?.toLowerCase();
                console.log('Card category:', cardCategory, 'Selected category:', category);
                
                if (category === 'all' || cardCategory === category) {
                    card.style.display = '';
                    visibleCount++;
                    console.log('Showing card:', card.querySelector('.course-name')?.textContent);
                } else {
                    card.style.display = 'none';
                    console.log('Hiding card:', card.querySelector('.course-name')?.textContent);
                }
            });
            
            console.log('Visible cards after filtering:', visibleCount);
        });
    });
}