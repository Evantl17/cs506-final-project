let inputGroupCounter = 1; // Counter to keep track of the input group numbers

let tickers = []; // Global array to store tickers fetched from the backend

// Fetch tickers from the Flask backend
async function fetchTickers() {
    try {
        const response = await fetch('http://127.0.0.1:3000/get-tickers'); // Flask URL
        tickers = await response.json();
    } catch (error) {
        console.error('Error fetching tickers:', error);
    }
}

// Call fetchTickers when the page loads
window.onload = fetchTickers;


// Function to initialize the first input group
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

// Function to add a new input group
function addInputFields(ticker = '', price = '') {
    const inputContainer = document.querySelector('.input-container');
    const newInputGroup = document.createElement('div');
    newInputGroup.className = 'input-group';

    // Create the number label
    const numberLabel = document.createElement('span');
    numberLabel.className = 'input-number';

    // Create the stock ticker input
    const stockLabel = document.createElement('label');
    stockLabel.innerText = 'Stock Ticker:';
    const stockInput = document.createElement('input');
    stockInput.type = 'text';
    stockInput.name = 'tickers';
    stockInput.required = true;
    stockInput.value = ticker; // Pre-fill with passed value if provided
    stockInput.className = 'stock-input'; // Add class for targeting
    const suggestionBox = document.createElement('div');
    suggestionBox.className = 'autocomplete-suggestions';

    // Add event listener for autocomplete
    stockInput.addEventListener('input', function () {
        const query = stockInput.value.toLowerCase();
        suggestionBox.innerHTML = ''; // Clear existing suggestions

        if (query.length === 0) return; // Don't show suggestions for empty input

        // Filter tickers based on user input
        const matches = tickers.filter(ticker =>
            ticker.toLowerCase().startsWith(query)
        );

        // Generate suggestion elements
        matches.forEach(match => {
            const suggestion = document.createElement('div');
            suggestion.textContent = match;

            // On click, fill the input with the selected value
            suggestion.addEventListener('click', function () {
                stockInput.value = match;
                suggestionBox.innerHTML = ''; // Clear suggestions
            });

            suggestionBox.appendChild(suggestion);
        });
    });

    // Create the price input
    const priceLabel = document.createElement('label');
    priceLabel.innerText = 'Price per Stock (dollar amount):';
    const priceInput = document.createElement('input');
    priceInput.type = 'text';
    priceInput.name = 'prices';
    priceInput.value = price; // Pre-fill with passed value if provided

    // Create the delete button
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.innerText = 'Delete';
    deleteButton.onclick = function () {
        inputContainer.removeChild(newInputGroup);
        updateInputGroupNumbers(); // Update numbering after removing
    };

    // Append the elements to the new input group
    newInputGroup.appendChild(numberLabel);
    newInputGroup.appendChild(stockLabel);
    newInputGroup.appendChild(stockInput);
    newInputGroup.appendChild(suggestionBox); // Add suggestion box here
    newInputGroup.appendChild(document.createElement('br'));
    newInputGroup.appendChild(priceLabel);
    newInputGroup.appendChild(priceInput);
    newInputGroup.appendChild(document.createElement('br'));
    newInputGroup.appendChild(deleteButton);

    inputContainer.appendChild(newInputGroup);
    updateInputGroupNumbers(); // Update numbering after adding
}

// Function to update input group numbers
function updateInputGroupNumbers() {
    const inputGroups = document.querySelectorAll('.input-group');
    inputGroupCounter = 1; // Reset counter
    inputGroups.forEach((group) => {
        const numberLabel = group.querySelector('.input-number');
        if (numberLabel) {
            numberLabel.innerText = `${inputGroupCounter}. `; // Update the number
        }
        inputGroupCounter++; // Increment counter
    });
}

// Ensure the loading screen is hidden when the page loads or is restored from the cache
function hideLoadingScreen() {
    document.getElementById('loading-screen').style.display = 'none';
}

// Listen for the `pageshow` event to hide the loading screen on navigation
window.addEventListener('pageshow', hideLoadingScreen);

// Initialize input groups with retained data
function initializeInputGroups(tickerData = [], priceData = []) {
    const inputContainer = document.querySelector('.input-container');

    // Clear existing input groups
    inputContainer.innerHTML = '';

    // Populate the input groups with existing data
    for (let i = 0; i < tickerData.length; i++) {
        const ticker = tickerData[i];
        const price = priceData[i] || '';
        addInputFields(ticker, price);
    }

    // If no data, initialize the first empty input group
    if (tickerData.length === 0) {
        addInputFields();
    }
}

// Add event listener for hiding the loading screen on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    hideLoadingScreen();

    // Retrieve retained tickers and prices (if available)
    const retainedTickers = JSON.parse(
        document.getElementById('retained-tickers')?.value || '[]'
    );
    const retainedPrices = JSON.parse(
        document.getElementById('retained-prices')?.value || '[]'
    );

    // Initialize input groups with retained values
    initializeInputGroups(retainedTickers, retainedPrices);
});

// Show the loading screen on form submission
document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Show the loading screen
    document.getElementById('loading-screen').style.display = 'flex';

    // Simulate form submission delay (for demonstration purposes)
    setTimeout(() => {
        event.target.submit(); // Programmatically submit the form
    }, 1000); // Adjust delay if needed
});
