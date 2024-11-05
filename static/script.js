let inputGroupCounter = 1; // Counter to keep track of the input group numbers

// Function to initialize the first input group with a number
function initializeFirstInputGroup() {
    const inputContainer = document.querySelector('.input-container');
    const firstInputGroup = inputContainer.querySelector('.input-group');

    // Create the number label for the first input group
    const numberLabel = document.createElement('span');
    numberLabel.className = 'input-number';
    numberLabel.innerText = `${inputGroupCounter}. `; // Display the number
    firstInputGroup.insertBefore(numberLabel, firstInputGroup.firstChild); // Insert at the beginning

    inputGroupCounter++; // Increment the counter for the next input group
}

// Function to add more input boxes for stock and price
function addInputFields() {
    const inputContainer = document.querySelector('.input-container');
    const newInputGroup = document.createElement('div');
    newInputGroup.className = 'input-group';

    // Create the number label
    const numberLabel = document.createElement('span');
    numberLabel.className = 'input-number';
    numberLabel.innerText = `${inputGroupCounter}. `;

    // Create the stock ticker input
    const stockLabel = document.createElement('label');
    stockLabel.innerText = 'Stock Ticker:';
    const stockInput = document.createElement('input');
    stockInput.type = 'text';
    stockInput.name = 'tickers';
    stockInput.required = true;

    // Create the price input
    const priceLabel = document.createElement('label');
    priceLabel.innerText = 'Price per Stock (dollar amount):';
    const priceInput = document.createElement('input');
    priceInput.type = 'text';
    priceInput.name = 'prices';

    // Create the delete button
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.innerText = 'Delete';
    deleteButton.onclick = function() {
        inputContainer.removeChild(newInputGroup);
        updateInputGroupNumbers();
    };

    // Append the elements to the new input group
    newInputGroup.appendChild(numberLabel);
    newInputGroup.appendChild(stockLabel);
    newInputGroup.appendChild(stockInput);
    newInputGroup.appendChild(document.createElement('br'));
    newInputGroup.appendChild(priceLabel);
    newInputGroup.appendChild(priceInput);
    newInputGroup.appendChild(document.createElement('br'));
    newInputGroup.appendChild(deleteButton);

    inputContainer.appendChild(newInputGroup);
    inputGroupCounter++;
}

// Function to update input group numbers
function updateInputGroupNumbers() {
    const inputGroups = document.querySelectorAll('.input-group');
    inputGroupCounter = 1;
    inputGroups.forEach(group => {
        const numberLabel = group.querySelector('.input-number');
        numberLabel.innerText = `${inputGroupCounter}. `;
        inputGroupCounter++;
    });
}

document.addEventListener('DOMContentLoaded', initializeFirstInputGroup);
