const dateButtonsContainer = document.getElementById('dateButtonsContainer');
const submitButton = document.getElementById('submitButton');
const resultDiv = document.getElementById('result');
const resultTitle = document.getElementById('summaryTitle');
let selectedDate = '';
submitButton.disabled = true;

// Generates the buttons for the past 10 days by fetching dates from the backend
async function generatePastTenButtons(){
    try {
        const response = await fetch('https://polibite.vercel.app/api/get_dates/');
        const data = await response.json();
        const dateList = data.date_list;

        for(let i = 0; i < 10; i++){
            let dateString = dateList[i];
            let dateStringReadable = dateString.substring(5,7) + "/" + dateString.substring(8);

            // Create 10 buttons corresponding to past 10 days
            const button = document.createElement('button');
            button.textContent = dateStringReadable;
            button.value = dateString;
            button.classList.add('date-button');

            // When clicked, select the value.
            button.addEventListener('click', function() {
                selectDate(this.value);
            });

            dateButtonsContainer.appendChild(button);
        }
    } catch (error) {
        console.error('Error fetching dates:', error);
    }
}

// Fetch the summary for a specific date from the backend
async function fetchSummary(date){
    resultDiv.innerHTML = 'Loading...';
    resultTitle.innerHTML = 'Loading...';

    try {
        const response = await fetch(`https://polibite.vercel.app/api/get_summary/${date}`);
        const data = await response.json();
        const summary = data.summary;

        resultDiv.innerHTML = summary;
        resultTitle.innerHTML = `Overview of ${date}`;
    } catch (error) {
        console.error('Error fetching summary:', error);
        resultDiv.innerHTML = 'Error fetching summary. Please try again later.';
    }
}

// Function to handle date selection
function selectDate(date){
    selectedDate = date;

    const buttons = document.querySelectorAll('.date-button');
    buttons.forEach(button => {
        button.classList.toggle('selected', button.value === date);
    });

    submitButton.disabled = false;
}

// Fetch and display the summary when the submit button is clicked
submitButton.addEventListener('click', async function(){
    if (selectedDate) {
        await fetchSummary(selectedDate);
    } else {
        resultDiv.innerHTML = 'Please select a date.';
    }
});

// Generate the buttons when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', async function() {
    await generatePastTenButtons();
});
