document.addEventListener('scroll', function (){
    const paragraphes = document.querySelectorAll('.section-p');
    const windowHeight = window.innerHeight || document.documentElement.clientHeight;
    paragraphes.forEach(function(paragraph){
        const rect = paragraph.getBoundingClientRect();
        if (rect.top < windowHeight && rect.bottom >= 0) {
            paragraph.classList.add('visible');
        }
});
});
    
const expandableImages = document.querySelectorAll('.menuImg');
    expandableImages.forEach(image => {
        image.addEventListener('click', function(event) {
            // Prevent the document click event from firing
            event.stopPropagation();
    
            // Remove the 'expanded' class from all images
            expandableImages.forEach(img => {
                if (img !== this) {
                    img.classList.remove('expanded');
                }
            });
            // Toggle the 'expanded' class on the clicked image
            this.classList.toggle('expanded');
        });
    });
    
    // Collapse expanded images when clicking anywhere else on the screen
    document.addEventListener('click', () => {
        expandableImages.forEach(img => {
            img.classList.remove('expanded');
        });
    });

const menusContainer = document.getElementById('menus');
function showSidebar() {
    const sidebar = document.querySelector ('.sidebar')
    sidebar.style.display = 'flex'
}
function hideSidebar() {
    const sidebar = document.querySelector ('.sidebar')
    sidebar.style.display = 'none'
}


// Function to load more images