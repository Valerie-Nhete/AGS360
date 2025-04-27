// List of questions
let questions = [
    "Enter your nearest city:",
    "Enter your soil pH (e.g., 6.5):",
    "Enter your microbial health (high, medium, low):",
    "Enter the nearby farmer's crop (e.g., Maize, Sorghum):",
    "Enter your total land size (in hectares):",
    "How many crops do you want to plant?:"
];

let answers = [];
let currentQuestionIndex = 0;

// Get page elements
const form = document.getElementById('question-form');
const label = document.getElementById('question-label');
const input = document.getElementById('answer');

// Detect which page we are on
const currentPage = window.location.pathname;

// Only if on data_collection.html
if (currentPage.includes("data_collection.html")) {

    if (label) {
        label.textContent = questions[currentQuestionIndex];
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        answers.push(input.value.trim());
        currentQuestionIndex++;

        if (currentQuestionIndex < questions.length) {
            label.textContent = questions[currentQuestionIndex];
            input.value = "";
        } else {
            // After last question, send data
            submitData();
        }
    });
}

// Function to send data to backend
function submitData() {
    const payload = {
        city: answers[0],
        soil_ph: answers[1],
        microbial_health: answers[2],
        crop: answers[3],
        land_size: answers[4],
        crops_count: answers[5]
    };

    // Store answers
    sessionStorage.setItem("soil_ph", payload.soil_ph);
    sessionStorage.setItem("microbial_health", payload.microbial_health);

    fetch('https://dd619286-8119-44a9-ab0b-4a0c6a5f183b-00-2eixbwk1mj7nd.kirk.replit.dev/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        sessionStorage.setItem("backendResults", JSON.stringify(data));
        window.location.href = "daily_report.html";
    })
    .catch(error => {
        console.error('Error connecting to server:', error);
        alert("Failed to connect to server. Please check if backend is running.");
    });
}

// Only if on daily_report.html, show results
if (currentPage.includes("daily_report.html")) {
    const backendData = JSON.parse(sessionStorage.getItem("backendResults"));
    if (backendData) {
        document.getElementById("soil-ph").textContent = sessionStorage.getItem("soil_ph") || "Unknown";
        document.getElementById("microbial-health").textContent = sessionStorage.getItem("microbial_health") || "Unknown";
        document.getElementById("temperature").textContent = backendData.temperature + " °C";
        document.getElementById("weather-description").textContent = backendData.weather_description;
        document.getElementById("timestamp").textContent = new Date().toLocaleString();
        document.getElementById("crop-suggestions").textContent = backendData.crop_suggestions.join(", ");
        document.getElementById("estimated-yield").textContent = backendData.estimated_yield + " tonnes";
        document.getElementById("estimated-profit").textContent = "$" + backendData.estimated_profit;
    }
}

// Export Data function (for daily report)
function exportData() {
    const backendData = JSON.parse(sessionStorage.getItem("backendResults"));
    if (!backendData) return;

    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Soil pH," + (sessionStorage.getItem("soil_ph") || "Unknown") + "\r\n";
    csvContent += "Microbial Health," + (sessionStorage.getItem("microbial_health") || "Unknown") + "\r\n";
    csvContent += "Temperature," + backendData.temperature + " °C\r\n";
    csvContent += "Weather Description," + backendData.weather_description + "\r\n";
    csvContent += "Crop Suggestions," + backendData.crop_suggestions.join(", ") + "\r\n";
    csvContent += "Estimated Yield," + backendData.estimated_yield + " tonnes\r\n";
    csvContent += "Estimated Profit," + backendData.estimated_profit + "\r\n";

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "daily_report.csv");
    document.body.appendChild(link);
    link.click();
}
