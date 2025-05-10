// Mock data - Replace with actual data from backend
const predictionResults = {
    algorithmResults: [
        { name: "Greedy", crop: "rice", score: 0.0017, scoreType: "cost" },
        { name: "A*", crop: "rice", score: 0.0017, scoreType: "cost" },
        { name: "Genetic", crop: "jute", score: 0.9273, scoreType: "fitness" },
        { name: "CSP", crop: "rice", score: 100, scoreType: "suitability" }
    ],
    astarExpansion: "1.", // Content from astar_path.pdf
    geneticExpansion: "1.", // Content from greedy_path.pdf
    userInput: {
        N: 90,
        P: 42,
        K: 43,
        temperature: 23,
        humidity: 82,
        ph: 6.5,
        rainfall: 202
    },
    resultingFeatures: {
        N: 90, // After interventions (simplified for mock data)
        P: 42.2,
        K: 44,
        temperature: 23,
        humidity: 82,
        ph: 6.5,
        rainfall: 202
    },
    suitabilityScores: {
        "rice": 100,
        "jute": 92.73
    },
    cropDescription: "Rice is a staple food crop that thrives in warm, humid environments with well-managed water resources.",
    resources: {
        "apply_N_fertilizer": 0,
        "apply_P_fertilizer": 0.2,
        "apply_K_fertilizer": 1.0,
        "irrigation_frequency": 3.3
    },
    estimatedCost: 50, // Example cost based on interventions
    adaptationTimeline: [
        { stage: "Initial Application", days: 0, nutrients: "P, K applied" },
        { stage: "Nutrient Uptake", days: 5, nutrients: "50% integration" },
        { stage: "Soil Stabilization", days: 10, nutrients: "80% integration" },
        { stage: "Ready for Planting", days: 15, nutrients: "100% integration" }
    ]
};

// Function to calculate best crop and confidence score
function calculateBestCrop(algorithmResults) {
    const cropCounts = {};
    algorithmResults.forEach(result => {
        const crop = result.crop;
        cropCounts[crop] = (cropCounts[crop] || 0) + 1;
    });
    let bestCrop = null;
    let maxCount = 0;
    for (const [crop, count] of Object.entries(cropCounts)) {
        if (count > maxCount) {
            bestCrop = crop;
            maxCount = count;
        }
    }
    const confidenceScore = maxCount / algorithmResults.length;
    return { bestCrop, confidenceScore };
}

const { bestCrop, confidenceScore } = calculateBestCrop(predictionResults.algorithmResults);

// Populate Best Crop Section
document.getElementById("bestCrop").innerText = bestCrop;
document.getElementById("suitabilityScore").innerText = `Suitability: ${predictionResults.suitabilityScores[bestCrop]}%`;
document.getElementById("confidenceScore").innerText = `Confidence: ${(confidenceScore * 100).toFixed(0)}% (based on algorithm agreement)`;

// Populate User Input Parameters
document.getElementById("paramN").innerText = `${predictionResults.userInput.N} units`;
document.getElementById("paramP").innerText = `${predictionResults.userInput.P} units`;
document.getElementById("paramK").innerText = `${predictionResults.userInput.K} units`;
document.getElementById("paramTemp").innerText = `${predictionResults.userInput.temperature} °C`;
document.getElementById("paramHumidity").innerText = `${predictionResults.userInput.humidity}%`;
document.getElementById("paramPh").innerText = predictionResults.userInput.ph;
document.getElementById("paramRainfall").innerText = `${predictionResults.userInput.rainfall} mm`;

// Populate Resulting Features After Change
document.getElementById("resultN").innerText = `${predictionResults.resultingFeatures.N} units`;
document.getElementById("resultP").innerText = `${predictionResults.resultingFeatures.P} units`;
document.getElementById("resultK").innerText = `${predictionResults.resultingFeatures.K} units`;
document.getElementById("resultTemp").innerText = `${predictionResults.resultingFeatures.temperature} °C`;
document.getElementById("resultHumidity").innerText = `${predictionResults.resultingFeatures.humidity}%`;
document.getElementById("resultPh").innerText = predictionResults.resultingFeatures.ph;
document.getElementById("resultRainfall").innerText = `${predictionResults.resultingFeatures.rainfall} mm`;

// Populate Crop Description
document.getElementById("cropDescription").innerText = predictionResults.cropDescription;

// Populate Resources and Costs
const resourcesList = document.getElementById("resourcesList");
let resourcesText = "";
for (const [resource, amount] of Object.entries(predictionResults.resources)) {
    let unit = "";
    if (resource.includes("fertilizer")) unit = "kg/ha";
    else if (resource === "irrigation_frequency") unit = "days between irrigation";
    resourcesText += `${resource.replace(/_/g, ' ')}: ${amount} ${unit}<br>`;
}
resourcesList.innerHTML = resourcesText || "No additional resources required.";
document.getElementById("totalCost").innerText = `Estimated Total Cost: $${predictionResults.estimatedCost.toFixed(2)}/ha`;

// Populate Algorithm Results Table
const algorithmTableBody = document.getElementById("algorithmResultsTable").querySelector("tbody");
predictionResults.algorithmResults.forEach(result => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${result.name}</td><td>${result.crop}</td><td>${result.score}</td><td>${result.scoreType}</td>`;
    algorithmTableBody.appendChild(row);
});

// Populate A* and Genetic Expansions
document.getElementById("astarContent").innerText = predictionResults.astarExpansion;
document.getElementById("geneticContent").innerText = predictionResults.geneticExpansion;

// Populate Soil Adaptation Timeline (blurred for future work)
const timelineMessage = document.getElementById("timelineMessage");
const timelineChartCanvas = document.getElementById("timelineChart").getContext("2d");
timelineMessage.innerText = "This feature will provide a detailed timeline for soil adaptation based on interventions. Stay tuned for updates!";
new Chart(timelineChartCanvas, {
    type: "line",
    data: {
        labels: predictionResults.adaptationTimeline.map(item => `${item.stage} (Day ${item.days})`),
        datasets: [{
            label: "Soil Adaptation Progress",
            data: predictionResults.adaptationTimeline.map((_, index) => (index + 1) * (100 / predictionResults.adaptationTimeline.length)),
            borderColor: "#388e3c",
            fill: false,
            tension: 0.3
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: { callbacks: { label: (context) => `${context.raw.toFixed(0)}% complete` } }
        },
        scales: {
            y: { beginAtZero: true, max: 100, title: { display: true, text: "Adaptation Progress (%)" } },
            x: { title: { display: true, text: "Timeline Stages" } }
        }
    }
});

// Populate Suitability Chart
const ctx = document.getElementById("suitabilityChart").getContext("2d");
new Chart(ctx, {
    type: "bar",
    data: {
        labels: Object.keys(predictionResults.suitabilityScores),
        datasets: [{
            label: "Suitability Score (%)",
            data: Object.values(predictionResults.suitabilityScores),
            backgroundColor: ["#388e3c", "#0288d1"]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: { callbacks: { label: (context) => `${context.raw}%` } }
        },
        scales: {
            y: { beginAtZero: true, max: 100, title: { display: true, text: "Suitability (%)" } },
            x: { title: { display: true, text: "Crops" } }
        }
    }
});

// Populate Detailed Results Table
const tableBody = document.getElementById("resultsTable").querySelector("tbody");
Object.entries(predictionResults.suitabilityScores).forEach(([crop, score]) => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${crop}</td><td>${score.toFixed(2)}%</td>`;
    tableBody.appendChild(row);
});