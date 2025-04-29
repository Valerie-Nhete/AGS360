let currentQuestionIndex = 0;
const questions = [
  "Enter your nearest city name:",
  "Enter your soil pH value (e.g., 6.5):",
  "Enter your soil microbial health (high, medium, low):",
  "Enter a brief note on what nearby farmers are growing:",
  "How many crops do you want to plant?",
  "Enter your total land size (in hectares):"
];
const answers = [];

document.addEventListener("DOMContentLoaded", function () {
  const questionLabel = document.getElementById("question-label");
  const answerInput = document.getElementById("answer");
  const form = document.getElementById("question-form");

  if (questionLabel && answerInput && form) {
    questionLabel.textContent = questions[currentQuestionIndex];

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const answer = answerInput.value.trim();
      if (answer !== "") {
        answers.push(answer);
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
          questionLabel.textContent = questions[currentQuestionIndex];
          answerInput.value = "";
        } else {
          submitAnswers();
        }
      } else {
        alert("Please enter an answer before submitting.");
      }
    });
  }

  // Populate Daily Report Page
  if (window.location.pathname.includes("daily_report.html")) {
    const reportData = JSON.parse(localStorage.getItem("dailyReport"));
    if (reportData) {
      document.getElementById("city").textContent = reportData.city;
      document.getElementById("temperature").textContent = reportData.temperature + "°C";
      document.getElementById("soil_moisture").textContent = reportData.soil_moisture + "%";
      document.getElementById("weather").textContent = reportData.weather;
      document.getElementById("soil_ph").textContent = reportData.soil_ph;
      document.getElementById("microbial_health").textContent = reportData.microbial_health;
      document.getElementById("nearby_crops").textContent = reportData.nearby_crops;
      document.getElementById("suggested_crops").textContent = reportData.suggested_crops.join(", ");
      document.getElementById("estimated_yield").textContent = reportData.estimated_yield + " tons";
      document.getElementById("estimated_profit").textContent = "$" + reportData.estimated_profit;
      document.getElementById("timestamp").textContent = reportData.timestamp;
    }
  }
});

function submitAnswers() {
  const collectedData = {
    city: answers[0],
    soil_ph: answers[1],
    microbial_health: answers[2],
    nearby_crops: answers[3],
    num_crops: answers[4],
    land_size: answers[5],
  };

  fetch("/process", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(collectedData),
  })
    .then((response) => response.json())
    .then((data) => {
      localStorage.setItem("dailyReport", JSON.stringify(data.result));
      window.location.href = "daily_report.html";
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Failed to connect to server.");
    });
}

// Export Daily Report to CSV
function exportCSV() {
  const reportData = JSON.parse(localStorage.getItem("dailyReport"));
  if (!reportData) {
    alert("No report data available to export.");
    return;
  }

  const csvRows = [
    ["Field", "Value"],
    ["City", reportData.city],
    ["Temperature", reportData.temperature + "°C"],
    ["Soil Moisture", reportData.soil_moisture + "%"],
    ["Weather", reportData.weather],
    ["Soil pH", reportData.soil_ph],
    ["Microbial Health", reportData.microbial_health],
    ["Nearby Crops", reportData.nearby_crops],
    ["Suggested Crops", reportData.suggested_crops.join(", ")],
    ["Estimated Yield", reportData.estimated_yield + " tons"],
    ["Estimated Profit", "$" + reportData.estimated_profit],
    ["Timestamp", reportData.timestamp]
  ];

  const csvContent = csvRows.map(row => row.join(",")).join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "daily_report.csv";
  link.click();
}