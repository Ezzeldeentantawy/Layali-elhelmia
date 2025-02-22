let counts = document.querySelectorAll('.count');
const prices = document.querySelectorAll('.price');
let totalPrice = document.getElementById('totalPrice');
let count = document.querySelector('#count').innerText;

function calculateTotalPrice() {
    let total = 10;
    prices.forEach(function(price, index) {
        let count = parseInt(counts[index].innerText);
        let num = parseInt(price.innerText) * count;
        total += num;
    });
    totalPrice.innerText = total;
}

// Function to increase the count
function increase(event, button) {
    event.preventDefault();
    const valueElement = button.nextElementSibling;
    let count = parseInt(valueElement.innerHTML);
    count++;
    valueElement.innerHTML = count;
    localStorage.setItem(valueElement.id, count); // Save count in local storage
    calculateTotalPrice();
}

// Function to decrease the count
function decrease(event, button) {
    event.preventDefault();
    const valueElement = button.previousElementSibling;
    let count = parseInt(valueElement.innerHTML);
    if (count > 0) {
        count--;
        valueElement.innerHTML = count;
        localStorage.setItem(valueElement.id, count); // Save count in local storage
    }
    calculateTotalPrice();
}

// Function to handle option change
// Function to set the selected options and counts in the cart page

// Function to add delete buttons to all menuType divs
function addDeleteButtons() {
    const menuTypes = document.querySelectorAll('.menuType');
    menuTypes.forEach(menuType => {
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.style.backgroundColor = 'red';
        deleteButton.style.width = '8%';
        deleteButton.style.borderRadius = '50px';
        deleteButton.style.marginRight = '60px';
        deleteButton.style.height = '60%';
        deleteButton.addEventListener('click', del);
        menuType.appendChild(deleteButton);
    });
}

// Function to delete the specific menuType div
function del(event) {
    const button = event.target;
    const menuType = button.closest('.menuType');
    if (menuType) {
        // Set the count to 0 before removing the div
        const countElement = menuType.querySelector('.count');
        if (countElement) {
            countElement.innerText = '0';
        }
        menuType.remove();
        calculateTotalPrice();
    }
}

// Call the function to add delete buttons and set selected options and counts when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    addDeleteButtons();
    calculateTotalPrice();
});

document.querySelectorAll('.increase-button').forEach(button => {
    button.addEventListener('click', function(event) {
        increase(event, button);
    });
});

document.querySelectorAll('.decrease-button').forEach(button => {
    button.addEventListener('click', function(event) {
        decrease(event, button);
    });
});

// Save selected option in local storage
function saveOption(selectId) {
    const select = document.getElementById(selectId);
    select.addEventListener('change', function() {
        const selectedOption = select.options[select.selectedIndex].value;
        localStorage.setItem(selectId, selectedOption);
        calculateTotalPrice();
    });
}

// Call saveOption for each select element
document.querySelectorAll('select').forEach(select => {
    saveOption(select.id);
});

// Retrieve saved option from local storage and set it
function loadOption(selectId) {
    const select = document.getElementById(selectId);
    const savedOption = localStorage.getItem(selectId);
    if (savedOption) {
        select.value = savedOption;
        // Trigger change event to update the price
        const event = new Event('change');
        select.dispatchEvent(event);
    }
}

// Call loadOption for each select element
document.querySelectorAll('select').forEach(select => {
    loadOption(select.id);
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
                priceParagraph.innerText = pricesFloat[index];
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
