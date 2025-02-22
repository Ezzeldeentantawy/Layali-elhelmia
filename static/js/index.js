let count = document.querySelector('#count').innerHTML;
const category = document.querySelectorAll('.category');
category.forEach((category, index) => {
    if (index % 2 !== 0) {
        category.style.flexDirection = 'row-reverse';
    } else {
        category.style.flexDirection = 'row';
    }
});
const menuImg = document.querySelectorAll('.menuImg');
const mediaquery = window.matchMedia('(max-width: 768px)');
const mediaqueryL = window.matchMedia('(max-width: 1024px)');
menuImg.forEach((menuImg, index) => {
    if (index % 2 !== 0) {
        menuImg.style.marginRight = '5%';
        menuImg.style.marginLeft = '0%';
    } else {
        menuImg.style.marginRight = '0%';
    }
});
const menusContainer = document.querySelectorAll('.menus-container');
menusContainer.forEach((menusContainer, index) => {
    if (index % 2 !== 0) {
        menusContainer.style.marginRight = '0%';
        menusContainer.style.marginLeft = '5%';
        
    } else {
        menusContainer.style.marginRight = '5%';
    }
    if (mediaquery.matches) {
        menusContainer.style.marginLeft = '0';
        menusContainer.style.marginRight = '0';
    } else if (mediaqueryL.matches) {
        menusContainer.style.marginLeft = '0';
        menusContainer.style.marginRight = '0';
    }
});
function increase(event, button) {
    event.preventDefault();
    const valueElement = button.nextElementSibling;
    let count = parseInt(valueElement.innerHTML);
    count++;
    valueElement.innerHTML = count;
}
function decrease(event, button) {
    event.preventDefault();
    const valueElement = button.previousElementSibling;
    let count = parseInt(valueElement.innerHTML);
    if (count > 0) {
        count--;
        valueElement.innerHTML = count;
    }
}

// Save selected option in local storage
function saveOption(selectId) {
    const select = document.getElementById(selectId);
    select.addEventListener('change', function() {
        const selectedOption = select.options[select.selectedIndex].value;
        localStorage.setItem(selectId, selectedOption);
    });
}

// Call saveOption for each select element
document.querySelectorAll('select').forEach(select => {
    saveOption(select.id);
});

// Function to handle option change
function updatePrice(selectId, prices, priceId) {
    if (prices !== undefined) {
        // Parse the prices into an array
        const pricesList = prices.split(' | ');
        const pricesFloat = pricesList.map(price => parseFloat(price));
        // Get the specific select element and price element
        const select = document.getElementById(selectId);
        const priceParagraph = document.getElementById(priceId);
        // Ensure both elements exist
        if (priceParagraph) {
            // Get the selected value (e.g., "M" or "L")
            const selectedOption = select.options[select.selectedIndex].value.trim();
            const selected = select.options[select.selectedIndex].innerText;
            for (let index = 0 ; index<select.options.length ; index++){
            if (parseInt(selectedOption) === index) {
                if (pricesFloat[index] !== undefined){ 
                priceParagraph.innerText = pricesFloat[index];
                }
                else {
                    priceParagraph.innerText = 'Not available';

                }
            }
            }
            
            // Update the price based on the selected option

    }
}
}
function changeprice() {
    calculateTotalPrice();
}

calculateTotalPrice();

function searchData(value) {
    const menus = document.querySelectorAll('.menuType');
    menus.forEach(menu => {
        const menuText = menu.textContent.toLowerCase();
        const searchText = value.toLowerCase();
        if (menuText.includes(searchText)) {
            menu.style.display = '';
        } else {
            menu.style.display = 'none';
        }
    });
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        const searchValue = event.target.value.toLowerCase();
        const menus = document.querySelectorAll('.category');
        for (let menu of menus) {
            const menuText = menu.textContent.toLowerCase();
            if (menuText.includes(searchValue)) {
                menu.scrollIntoView({ behavior: 'smooth' });
                break;
            }
        }
    }
}
function submitCartForm() {
    const mealDivs = document.querySelectorAll('.menuType');
    let totalMealCount = 0;
    let hasUnavailableItem = false;
    let selectedItems = '';

    mealDivs.forEach(meal => {
        const countElement = meal.querySelector('.count');
        const priceElement = meal.querySelector('.price');

        if (!countElement || !priceElement) {
            console.error("Missing elements in:", meal);
            return;
        }

        const count = Number(countElement.textContent.replace(/\D/g, '')) || 0;
        const price = priceElement.textContent.trim().toLowerCase();
        const isAvailable = price !== "not available";

        totalMealCount += count;
        
        if (!isAvailable) {
            hasUnavailableItem = true;
        } else if (count > 0) {
            // Get the ID of the menuType div and add it to the string
            selectedItems += `<div class="menuType" id="${meal.id}">\n${meal.innerHTML}\n</div> `;  // Format: "id:content;"
        }
    });

    if (hasUnavailableItem) {
        alert('⚠️ Unavailable items detected!');
        return;
    }

    if (totalMealCount === 0) {
        alert('🍴 Please select meals first!');
        return;
    }
    console.log(selectedItems)
    document.getElementById('menuMealsContent').value = selectedItems;
    document.getElementById('cartForm').submit();
}