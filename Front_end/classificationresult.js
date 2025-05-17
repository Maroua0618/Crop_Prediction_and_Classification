// Mock data - Replace with actual data from backend
const predictionResults = {
    initialEnvironment: {
        N: 70.0,
        P: 50.0,
        K: 100.0,
        temperature: 30.0,
        humidity: 40.0,
        ph: 7.0,
        rainfall: 150.0
    },
    resourceAdjustments: {
        greedy: [
            { crop: "pigeonpeas", modifications: "add_organic_matter: 25 units, apply_K_fertilizer: 300 units" },
            { crop: "jute", modifications: "add_organic_matter: 30 units, apply_K_fertilizer: 400 units" },
            { crop: "coffee", modifications: "add_organic_matter: 15 units, apply_K_fertilizer: 100 units, apply_N_fertilizer: 50 units" },
            { crop: "grapes", modifications: "add_organic_matter: 30 units, apply_K_fertilizer: 300 units, apply_P_fertilizer: 50 units" },
            { crop: "papaya", modifications: "apply_P_fertilizer: 450 units" }
        ],
        astar: [
            { crop: "papaya", modifications: "" },
            { crop: "mothbeans", modifications: "apply_N_fertilizer: 50 units" },
            { crop: "pigeonpeas", modifications: "apply_P_fertilizer: 50 units, apply_N_fertilizer: 50 units" },
            { crop: "coffee", modifications: "apply_N_fertilizer: 100 units, add_organic_matter: 5 units" },
            { crop: "jute", modifications: "add_organic_matter: 10 units" }
        ]
    },
    algorithmResults: [
        { name: "Greedy", crop: "pigeonpeas", score: 0.0084, scoreType: "cost" },
        { name: "A*", crop: "papaya", score: 0.0432, scoreType: "cost" },
        { name: "Genetic", crop: "papaya", score: 0.8629, scoreType: "fitness" },
        { name: "CSP", crop: "None", score: -Infinity, scoreType: "suitability" }
    ],
    greedyExpansion: `# Greedy Algorithm Expansion

No exact solution found. Returning top 5 crops with lowest total costs after expanding 2567 nodes.

## Top 5 Crops by Cost:
1. pigeonpeas: cost 0.0084
   - Recommended Modifications:
     - add_organic_matter: 25 units
     - apply_K_fertilizer: 300 units
2. jute: cost 0.0132
   - Recommended Modifications:
     - add_organic_matter: 30 units
     - apply_K_fertilizer: 400 units
3. coffee: cost 0.0146
   - Recommended Modifications:
     - add_organic_matter: 15 units
     - apply_K_fertilizer: 100 units
     - apply_N_fertilizer: 50 units
4. grapes: cost 0.0152
   - Recommended Modifications:
     - add_organic_matter: 30 units
     - apply_K_fertilizer: 300 units
     - apply_P_fertilizer: 50 units
5. papaya: cost 0.0171
   - Recommended Modifications:
     - apply_P_fertilizer: 450 units

## Performance Metrics:
- Nodes expanded: 2567
- Execution time: 26.559096s
- Memory usage: 6.295676 MB

![Greedy Search Path](greedy_path.pdf)`,

    astarExpansion: `# A* Algorithm Expansion

No exact solution found. Returning top 5 crops with lowest total costs after expanding 2874 nodes.

## Top 5 Crops by Cost:
1. papaya: cost 0.0432
   - Recommended Modifications: None
2. mothbeans: cost 5.1566
   - Recommended Modifications:
     - apply_N_fertilizer: 50 units
3. pigeonpeas: cost 10.6909
   - Recommended Modifications:
     - apply_P_fertilizer: 50 units
     - apply_N_fertilizer: 50 units
4. coffee: cost 112.6357
   - Recommended Modifications:
     - apply_N_fertilizer: 100 units
     - add_organic_matter: 5 units
5. jute: cost 143.8933
   - Recommended Modifications:
     - add_organic_matter: 10 units

## Performance Metrics:
- Nodes expanded: 2874
- Execution time: 28.594419s
- Memory usage: 3.973558 MB

![A* Search Path](astar_path (2).pdf)`,

    geneticExpansion: `# Genetic Algorithm Expansion

The genetic algorithm evolves solutions through natural selection principles.

## Evolution Process:
- Generation 0: Fitness = 0.7873, Crop = papaya
- Generation 10: Fitness = 0.8319, Crop = papaya
- Generation 20: Fitness = 0.8554, Crop = papaya
- Generation 30: Fitness = 0.8620, Crop = papaya
- Generation 40: Fitness = 0.8628, Crop = papaya

## Best Solution:
- Fitness = 0.8629
- Interventions:
  - add_organic_matter: 0 units
  - irrigation_frequency: 1 day
  - apply_N_fertilizer: 0 units
  - apply_P_fertilizer: 0 units
  - apply_K_fertilizer: 0 units
- Crop: papaya

## Top 5 Crops by Suitability:
1. papaya: 81.27%
2. jute: 81.11%
3. coffee: 79.75%
4. chickpea: 79.18%
5. banana: 77.82%

## Performance Metrics:
- Generations: 40
- Execution time: 27.524738s
- Memory usage: 1.069918 MB`,

    cspExpansion: `# CSP Algorithm Expansion

The Constraint Satisfaction Problem (CSP) algorithm models crop selection as a set of variables with constraints.

## Initial Environment:
- N: 70.0
- P: 50.0
- K: 100.0
- temperature: 30.0
- humidity: 40.0
- ph: 7.0
- rainfall: 150.0

## Final Environment:
- N: 70.0
- P: 50.0
- K: 100.0
- temperature: 30.0
- humidity: 40.0
- ph: 7.0
- rainfall: 150.0

## Constraints:
- Crop (Hard): Satisfied
- Crop,Irrigation (Hard): Satisfied
- Fertilizer_N,Fertilizer_P,Fertilizer_K (Soft): Satisfied, Penalty: 0
- Irrigation (Soft): Satisfied, Penalty: 0
- Organic_Matter (Soft): Satisfied, Penalty: 0

## Objective Score:
- Score: -inf
- Selected Crop: None

## Top 5 Crops by Suitability:
1. papaya: 71.43%
   - N: 70.0 ✓ (Range: 31-70)
   - P: 50.0 ✓ (Range: 46-70)
   - K: 100.0 ✗ (Range: 45-55)
   - temperature: 30.0 ✓ (Range: 23.0-43.7)
   - humidity: 40.0 ✗ (Range: 90.0-94.9)
   - ph: 7.0 ✓ (Range: 6.5-7.0)
   - rainfall: 150.0 ✓ (Range: 40.4-248.9)
2. mothbeans: 57.14%
   - N: 70.0 ✗ (Range: 0-40)
   - P: 50.0 ✓ (Range: 35-60)
   - K: 100.0 ✗ (Range: 15-25)
   - temperature: 30.0 ✓ (Range: 24.0-32.0)
   - humidity: 40.0 ✓ (Range: 40.0-65.0)
   - ph: 7.0 ✓ (Range: 3.5-9.9)
   - rainfall: 150.0 ✗ (Range: 30.9-74.4)
3. pigeonpeas: 57.14%
   - N: 70.0 ✗ (Range: 0-40)
   - P: 50.0 ✗ (Range: 55-80)
   - K: 100.0 ✗ (Range: 15-25)
   - temperature: 30.0 ✓ (Range: 18.3-37.0)
   - humidity: 40.0 ✓ (Range: 30.4-69.7)
   - ph: 7.0 ✓ (Range: 4.5-7.4)
   - rainfall: 150.0 ✓ (Range: 90.1-198.8)
4. jute: 42.86%
   - N: 70.0 ✓ (Range: 60-100)
   - P: 50.0 ✓ (Range: 35-60)
   - K: 100.0 ✗ (Range: 35-45)
   - temperature: 30.0 ✗ (Range: 23.1-27.0)
   - humidity: 40.0 ✗ (Range: 70.9-89.9)
   - ph: 7.0 ✓ (Range: 6.0-7.5)
   - rainfall: 150.0 ✗ (Range: 150.2-199.8)
5. maize: 42.86%
   - N: 70.0 ✓ (Range: 60-100)
   - P: 50.0 ✓ (Range: 35-60)
   - K: 100.0 ✗ (Range: 15-25)
   - temperature: 30.0 ✗ (Range: 18.0-26.5)
   - humidity: 40.0 ✗ (Range: 55.3-74.8)
   - ph: 7.0 ✓ (Range: 5.5-7.0)
   - rainfall: 150.0 ✗ (Range: 60.7-109.8)

## Performance Metrics:
- Constraints checked: 25
- Backtracks: 3
- Execution time: 1.149737s
- Memory usage: 0.937282 MB`,

    algorithmComparison: {
        greedy: { time: 26.559096, memory: 6.295676 },
        astar: { time: 28.594419, memory: 3.973558 },
        genetic: { time: 27.524738, memory: 1.069918 },
        csp: { time: 1.149737, memory: 0.937282 }
    },
    suitabilityScores: {
        "papaya": 81.27, // Using Genetic's higher score as default
        "jute": 81.11,
        "coffee": 79.75,
        "chickpea": 79.18,
        "banana": 77.82,
        "mothbeans": 57.14, // From CSP
        "pigeonpeas": 57.14,
        "maize": 42.86
    },
    cropDetails: {
        "papaya": {
            N: { value: 70.0, range: "31-70", match: true },
            P: { value: 50.0, range: "46-70", match: true },
            K: { value: 100.0, range: "45-55", match: false },
            temperature: { value: 30.0, range: "23.0-43.7", match: true },
            humidity: { value: 40.0, range: "90.0-94.9", match: false },
            ph: { value: 7.0, range: "6.5-7.0", match: true },
            rainfall: { value: 150.0, range: "40.4-248.9", match: true }
        },
        "mothbeans": {
            N: { value: 70.0, range: "0-40", match: false },
            P: { value: 50.0, range: "35-60", match: true },
            K: { value: 100.0, range: "15-25", match: false },
            temperature: { value: 30.0, range: "24.0-32.0", match: true },
            humidity: { value: 40.0, range: "40.0-65.0", match: true },
            ph: { value: 7.0, range: "3.5-9.8", match: true },
            rainfall: { value: 150.0, range: "30.9-74.4", match: false }
        },
        "pigeonpeas": {
            N: { value: 70.0, range: "0-40", match: false },
            P: { value: 50.0, range: "55-80", match: false },
            K: { value: 100.0, range: "15-25", match: false },
            temperature: { value: 30.0, range: "18.3-37.0", match: true },
            humidity: { value: 40.0, range: "30.4-69.7", match: true },
            ph: { value: 7.0, range: "4.5-7.4", match: true },
            rainfall: { value: 150.0, range: "90.1-198.8", match: true }
        },
        "jute": {
            N: { value: 70.0, range: "60-100", match: true },
            P: { value: 50.0, range: "35-60", match: true },
            K: { value: 100.0, range: "35-45", match: false },
            temperature: { value: 30.0, range: "23.1-27.0", match: false },
            humidity: { value: 40.0, range: "70.9-89.9", match: false },
            ph: { value: 7.0, range: "6.0-7.5", match: true },
            rainfall: { value: 150.0, range: "150.2-199.8", match: false }
        },
        "maize": {
            N: { value: 70.0, range: "60-100", match: true },
            P: { value: 50.0, range: "35-60", match: true },
            K: { value: 100.0, range: "15-25", match: false },
            temperature: { value: 30.0, range: "18.0-26.5", match: false },
            humidity: { value: 40.0, range: "55.3-74.8", match: false },
            ph: { value: 7.0, range: "5.5-7.0", match: true },
            rainfall: { value: 150.0, range: "60.7-109.8", match: false }
        }
    }
};

// Convert markdown to HTML
function markdownToHtml(markdown) {
    if (!markdown) return '';
    
    markdown = markdown.replace(/^# (.*$)/gm, '<h2>$1</h2>');
    markdown = markdown.replace(/^## (.*$)/gm, '<h3>$1</h3>');
    markdown = markdown.replace(/^### (.*$)/gm, '<h4>$1</h4>');
    
    markdown = markdown.replace(/^\s*- (.*$)/gm, '<li>$1</li>');
    
    const listItems = markdown.match(/<li>.*?<\/li>/gs);
    if (listItems) {
        listItems.forEach(item => {
            if (!item.includes('</ul>')) {
                markdown = markdown.replace(item, `<ul>${item}</ul>`);
            }
        });
    }
    
    markdown = markdown.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    markdown = markdown.replace(/\*(.*?)\*/g, '<em>$1</em>');
    markdown = markdown.replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" style="max-width: 100%; margin: 20px 0;">');
    
    const paragraphs = markdown.split('\n\n');
    markdown = paragraphs.map(p => {
        if (!p.startsWith('<h') && !p.startsWith('<ul') && !p.startsWith('<img') && p.trim() !== '') {
            return `<p>${p}</p>`;
        }
        return p;
    }).join('');
    
    return markdown;
}

// Render search tree using vis.js
function renderSearchTree(containerId, treeData) {
    const container = document.getElementById(containerId);
    const data = {
        nodes: new vis.DataSet(treeData.nodes),
        edges: new vis.DataSet(treeData.edges)
    };
    const options = {
        layout: { hierarchical: { direction: "UD", sortMethod: "directed" } },
        nodes: { shape: "box", font: { size: 12 } },
        edges: { arrows: "to", font: { size: 10 } }
    };
    new vis.Network(container, data, options);
}

// Populate Initial Environment
document.getElementById("initialN").innerText = `${predictionResults.initialEnvironment.N} units`;
document.getElementById("initialP").innerText = `${predictionResults.initialEnvironment.P} units`;
document.getElementById("initialK").innerText = `${predictionResults.initialEnvironment.K} units`;
document.getElementById("initialTemp").innerText = `${predictionResults.initialEnvironment.temperature} °C`;
document.getElementById("initialHumidity").innerText = `${predictionResults.initialEnvironment.humidity}%`;
document.getElementById("initialPh").innerText = predictionResults.initialEnvironment.ph;
document.getElementById("initialRainfall").innerText = `${predictionResults.initialEnvironment.rainfall} mm`;

// Populate Resource Adjustments
const resourceAdjustmentsDiv = document.getElementById("resourceAdjustments");
let adjustmentsText = "<strong>Recommended Modifications by Algorithm:</strong><br>";
Object.entries(predictionResults.resourceAdjustments).forEach(([algo, mods]) => {
    adjustmentsText += `<strong>${algo.charAt(0).toUpperCase() + algo.slice(1)}:</strong><br>`;
    mods.forEach(mod => {
        adjustmentsText += `${mod.crop}: ${mod.modifications}<br>`;
    });
    adjustmentsText += "<br>";
});
resourceAdjustmentsDiv.innerHTML = adjustmentsText || "No adjustments required.";

// Populate Algorithm Results Table
const algorithmTableBody = document.getElementById("algorithmResultsTable").querySelector("tbody");
algorithmTableBody.innerHTML = '';
predictionResults.algorithmResults.forEach(result => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${result.name}</td><td>${result.crop}</td><td>${result.score}</td><td>${result.scoreType}</td>`;
    algorithmTableBody.appendChild(row);
});

// Populate Expansions
document.getElementById("greedyDetails").innerHTML = markdownToHtml(predictionResults.greedyExpansion);
document.getElementById("astarDetails").innerHTML = markdownToHtml(predictionResults.astarExpansion);
document.getElementById("geneticDetails").innerHTML = markdownToHtml(predictionResults.geneticExpansion);
document.getElementById("cspDetails").innerHTML = markdownToHtml(predictionResults.cspExpansion);

// Render Search Trees
const greedyTreeImage = document.getElementById("greedyTreeImage");
const astarTreeImage = document.getElementById("astarTreeImage");

if (greedyTreeImage.complete && greedyTreeImage.naturalHeight !== 0) {
    greedyTreeImage.style.display = "block";
} else {
    renderSearchTree("greedyTreeVis", { nodes: [], edges: [] }); // Placeholder
}

if (astarTreeImage.complete && astarTreeImage.naturalHeight !== 0) {
    astarTreeImage.style.display = "block";
} else {
    renderSearchTree("astarTreeVis", { nodes: [], edges: [] }); // Placeholder
}

// Populate Algorithm Comparison Table
const comparisonTableBody = document.getElementById("comparisonTable").querySelector("tbody");
comparisonTableBody.innerHTML = '';
Object.entries(predictionResults.algorithmComparison).forEach(([algo, metrics]) => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${algo}</td><td>${metrics.time.toFixed(6)}</td><td>${metrics.memory.toFixed(6)}</td>`;
    comparisonTableBody.appendChild(row);
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
            backgroundColor: ["#388e3c", "#0288d1", "#ffa000", "#d32f2f", "#7b1fa2", "#0288d1", "#ffa000", "#d32f2f"]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: { callbacks: { label: (context) => `${context.raw.toFixed(2)}%` } }
        },
        scales: {
            y: { beginAtZero: true, max: 100, title: { display: true, text: "Suitability (%)" } },
            x: { title: { display: true, text: "Crops" } }
        }
    }
});

// Populate Detailed Results Table
const tableBody = document.getElementById("resultsTable").querySelector("tbody");
tableBody.innerHTML = '';
Object.entries(predictionResults.suitabilityScores).forEach(([crop, score]) => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${crop}</td><td>${score.toFixed(2)}%</td>`;
    tableBody.appendChild(row);
});

// Add tabs functionality for algorithm expansions
function openExpansionTab(evt, tabName) {
    const expansionContent = document.getElementsByClassName("expansion-content");
    for (let i = 0; i < expansionContent.length; i++) {
        expansionContent[i].style.display = "none";
    }

    const tabLinks = document.getElementsByClassName("expansion-tab");
    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].className = tabLinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

window.openExpansionTab = openExpansionTab;

// Default to showing the first tab
document.addEventListener('DOMContentLoaded', function() {
    const firstTab = document.querySelector('.expansion-tab');
    if (firstTab) {
        firstTab.click();
    }
});