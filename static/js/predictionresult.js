// Mock data - Replace with actual data from backend
const predictionResults = {
    algorithmResults: [
        { name: "Greedy", crop: "rice", score: 0.0017, scoreType: "cost" },
        { name: "A*", crop: "rice", score: 0.0017, scoreType: "cost" },
        { name: "Genetic", crop: "jute", score: 0.9273, scoreType: "fitness" },
        { name: "CSP", crop: "rice", score: 100, scoreType: "suitability" }
    ],
    astarExpansion: `# A* Algorithm Expansion

The A* search algorithm explores the search space efficiently by combining:
- The cost to reach the current node (g-score)
- The estimated cost to reach the goal (heuristic or h-score)

![A* Search Tree](astar_search_tree.png)

## Execution Trace:
1. Starting with initial soil parameters: N=90, P=42, K=43
2. Calculated heuristic values for possible soil adjustments
3. Expanded nodes in order of f-score (g + h):
   - Add 0.2 P fertilizer (f=0.0012)
   - Add 1.0 K fertilizer (f=0.0015)
   - No N fertilizer needed (optimal level)
4. Selected Path: Apply 0.2 P + 1.0 K fertilizer
5. Termination: Goal state reached when suitability for rice = 100%

## Performance Metrics:
- Nodes explored: 12
- Path cost: 0.0017 (resource cost)
- Execution time: 42ms`,

    geneticExpansion: `# Genetic Algorithm Expansion

The genetic algorithm evolves solutions through natural selection principles.

## Execution Details:
1. Initial population size: 50 individuals
2. Chromosome encoding: [N_fertilizer, P_fertilizer, K_fertilizer, irrigation]
3. Fitness function: soil_suitability(crop) - resource_cost

## Evolution Process:
- Generation 1: Best fitness = 0.7821 (crop: jute)
- Generation 5: Best fitness = 0.8534 (crop: jute)
- Generation 10: Best fitness = 0.9112 (crop: jute)
- Generation 15: Best fitness = 0.9273 (crop: jute)

## Selection and Mutation:
- Tournament selection (size 3)
- Mutation rate: 0.05
- Crossover rate: 0.85

## Termination: 
- Convergence achieved after 15 generations
- Final solution: Optimized for jute with 92.73% suitability`,

    cspExpansion: `# CSP Algorithm Expansion

The Constraint Satisfaction Problem (CSP) algorithm models crop selection as a set of variables with constraints.

## Execution Details:
1. Variables: N, P, K, temperature, humidity, pH, rainfall
2. Constraints: Optimal ranges for rice (e.g., N: 80-100, pH: 6.0-7.0)
3. Backtracking search to assign values satisfying all constraints

## Execution Trace:
1. Assigned N=90 (within rice constraint)
2. Assigned P=42.2 after adding 0.2 units
3. Assigned K=44 after adding 1.0 units
4. Verified environmental constraints (temperature, humidity, etc.)
5. Solution found: All constraints satisfied for rice

## Performance Metrics:
- Constraints checked: 25
- Backtracks: 3
- Execution time: 35ms`,

    greedyExpansion: `# Greedy Algorithm Expansion

The Greedy algorithm makes locally optimal choices at each step to minimize resource cost.

![Greedy Search Tree](greedy_search_tree.png)

## Execution Trace:
1. Starting with initial soil parameters: N=90, P=42, K=43
2. Selected cheapest intervention: Add 0.2 P fertilizer (cost=0.0008)
3. Selected next cheapest: Add 1.0 K fertilizer (cost=0.0009)
4. No further interventions needed (N optimal)
5. Termination: Reached suitability for rice = 100%

## Performance Metrics:
- Steps taken: 2
- Total cost: 0.0017
- Execution time: 20ms`,

    astarTreeData: {
        nodes: [
            { id: 1, label: "Initial: N=90, P=42, K=43" },
            { id: 2, label: "Add 0.2 P: N=90, P=42.2, K=43" },
            { id: 3, label: "Add 1.0 K: N=90, P=42.2, K=44" }
        ],
        edges: [
            { from: 1, to: 2, label: "Add 0.2 P (f=0.0012)" },
            { from: 2, to: 3, label: "Add 1.0 K (f=0.0015)" }
        ]
    },

    greedyTreeData: {
        nodes: [
            { id: 1, label: "Initial: N=90, P=42, K=43" },
            { id: 2, label: "Add 0.2 P: N=90, P=42.2, K=43" },
            { id: 3, label: "Add 1.0 K: N=90, P=42.2, K=44" }
        ],
        edges: [
            { from: 1, to: 2, label: "Add 0.2 P (cost=0.0008)" },
            { from: 2, to: 3, label: "Add 1.0 K (cost=0.0009)" }
        ]
    },

    algorithmComparison: {
        astar: {
            strengths: [
                "Guaranteed to find optimal solution",
                "Efficient path finding",
                "Reliable for standard cases"
            ],
            weaknesses: [
                "Slower than Greedy in simple cases",
                "Memory intensive for large search spaces",
                "Struggles with edge cases (343 nodes)"
            ],
            recommendation: "Best for balanced performance in typical agricultural scenarios"
        },
        genetic: {
            strengths: [
                "Handles complex optimization",
                "Adapts to extreme conditions",
                "Proposes precise interventions"
            ],
            weaknesses: [
                "Slow execution (16+s)",
                "Requires parameter tuning",
                "High computational cost"
            ],
            recommendation: "Best for detailed planning and edge cases"
        },
        csp: {
            strengths: [
                "Fastest execution (0.12-0.71s)",
                "Effective constraint propagation",
                "Precise for exact matches"
            ],
            weaknesses: [
                "Fails if no solution satisfies constraints",
                "Limited flexibility for partial matches",
                "Requires well-defined constraints"
            ],
            recommendation: "Best for real-time applications and mobile apps"
        },
        greedy: {
            strengths: [
                "Fast execution (~1s)",
                "Simple implementation",
                "Low memory usage"
            ],
            weaknesses: [
                "Misses global optima",
                "Struggles in edge cases (343 nodes)",
                "Limited to local optimization"
            ],
            recommendation: "Best for quick, low-cost solutions in standard cases"
        }
    },
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
        N: 90,
        P: 42.2,
        K: 44,
        temperature: 23,
        humidity: 82,
        ph: 6.5,
        rainfall: 202
    },
    suitabilityScores: {
        "rice": 100,
        "jute": 92.73,
        "maize": 78.45,
        "wheat": 65.21
    },
    cropDescription: "Rice is a staple food crop that thrives in warm, humid environments with well-managed water resources. It requires moderately high nitrogen levels and balanced P-K ratios. The tropical climate of your region with temperature around 23°C and humidity of 82% provides ideal conditions for rice cultivation.",
    resources: {
        "apply_N_fertilizer": 0,
        "apply_P_fertilizer": 0.2,
        "apply_K_fertilizer": 1.0,
        "irrigation_frequency": 3.3
    },
    estimatedCost: 50,
    adaptationTimeline: [
        { stage: "Initial Application", days: 0, nutrients: "P, K applied" },
        { stage: "Nutrient Uptake", days: 5, nutrients: "50% integration" },
        { stage: "Soil Stabilization", days: 10, nutrients: "80% integration" },
        { stage: "Ready for Planting", days: 15, nutrients: "100% integration" }
    ]
};

// Convert markdown to HTML
function markdownToHtml(markdown) {
    if (!markdown) return '';
    
    // Handle headers
    markdown = markdown.replace(/^# (.*$)/gm, '<h2>$1</h2>');
    markdown = markdown.replace(/^## (.*$)/gm, '<h3>$1</h3>');
    markdown = markdown.replace(/^### (.*$)/gm, '<h4>$1</h4>');
    
    // Handle lists
    markdown = markdown.replace(/^\s*- (.*$)/gm, '<li>$1</li>');
    
    // Wrap lists
    const listItems = markdown.match(/<li>.*?<\/li>/gs);
    if (listItems) {
        listItems.forEach(item => {
            if (!item.includes('</ul>')) {
                markdown = markdown.replace(item, `<ul>${item}</ul>`);
            }
        });
    }
    
    // Handle bold
    markdown = markdown.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Handle italic
    markdown = markdown.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Handle images
    markdown = markdown.replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" style="max-width: 100%; margin: 20px 0;">');
    
    // Handle paragraphs
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
algorithmTableBody.innerHTML = '';
predictionResults.algorithmResults.forEach(result => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${result.name}</td><td>${result.crop}</td><td>${result.score}</td><td>${result.scoreType}</td>`;
    algorithmTableBody.appendChild(row);
});

// Populate Expansions
document.getElementById("astarDetails").innerHTML = markdownToHtml(predictionResults.astarExpansion);
document.getElementById("geneticContent").innerHTML = markdownToHtml(predictionResults.geneticExpansion);
document.getElementById("cspContent").innerHTML = markdownToHtml(predictionResults.cspExpansion);
document.getElementById("greedyDetails").innerHTML = markdownToHtml(predictionResults.greedyExpansion);

// Render Search Trees (fallback to dynamic rendering if images not available)
const astarTreeImage = document.getElementById("astarTreeImage");
const greedyTreeImage = document.getElementById("greedyTreeImage");

if (astarTreeImage.complete && astarTreeImage.naturalHeight !== 0) {
    astarTreeImage.style.display = "block";
} else {
    renderSearchTree("astarTreeVis", predictionResults.astarTreeData);
}

if (greedyTreeImage.complete && greedyTreeImage.naturalHeight !== 0) {
    greedyTreeImage.style.display = "block";
} else {
    renderSearchTree("greedyTreeVis", predictionResults.greedyTreeData);
}

// Populate Algorithm Comparison Section
const astarStrengthsList = document.getElementById("astarStrengths");
const astarWeaknessesList = document.getElementById("astarWeaknesses");
const geneticStrengthsList = document.getElementById("geneticStrengths");
const geneticWeaknessesList = document.getElementById("geneticWeaknesses");
const cspStrengthsList = document.getElementById("cspStrengths");
const cspWeaknessesList = document.getElementById("cspWeaknesses");
const greedyStrengthsList = document.getElementById("greedyStrengths");
const greedyWeaknessesList = document.getElementById("greedyWeaknesses");

if (astarStrengthsList && astarWeaknessesList && geneticStrengthsList && geneticWeaknessesList &&
    cspStrengthsList && cspWeaknessesList && greedyStrengthsList && greedyWeaknessesList) {
    astarStrengthsList.innerHTML = '';
    astarWeaknessesList.innerHTML = '';
    geneticStrengthsList.innerHTML = '';
    geneticWeaknessesList.innerHTML = '';
    cspStrengthsList.innerHTML = '';
    cspWeaknessesList.innerHTML = '';
    greedyStrengthsList.innerHTML = '';
    greedyWeaknessesList.innerHTML = '';
    
    predictionResults.algorithmComparison.astar.strengths.forEach(strength => {
        const li = document.createElement("li");
        li.textContent = strength;
        astarStrengthsList.appendChild(li);
    });
    
    predictionResults.algorithmComparison.astar.weaknesses.forEach(weakness => {
        const li = document.createElement("li");
        li.textContent = weakness;
        astarWeaknessesList.appendChild(li);
    });
    
    predictionResults.algorithmComparison.genetic.strengths.forEach(strength => {
        const li = document.createElement("li");
        li.textContent = strength;
        geneticStrengthsList.appendChild(li);
    });
    
    predictionResults.algorithmComparison.genetic.weaknesses.forEach(weakness => {
        const li = document.createElement("li");
        li.textContent = weakness;
        geneticWeaknessesList.appendChild(li);
    });
    
    predictionResults.algorithmComparison.csp.strengths.forEach(strength => {
        const li = document.createElement("li");
        li.textContent = strength;
        cspStrengthsList.appendChild(li);
    });
    
    predictionResults.algorithmComparison.csp.weaknesses.forEach(weakness => {
        const li = document.createElement("li");
        li.textContent = weakness;
        cspWeaknessesList.appendChild(li);
    });
    
    predictionResults.algorithmComparison.greedy.strengths.forEach(strength => {
        const li = document.createElement("li");
        li.textContent = strength;
        greedyStrengthsList.appendChild(li);
    });
    
    predictionResults.algorithmComparison.greedy.weaknesses.forEach(weakness => {
        const li = document.createElement("li");
        li.textContent = weakness;
        greedyWeaknessesList.appendChild(li);
    });
    
    document.getElementById("astarRecommendation").textContent = 
        predictionResults.algorithmComparison.astar.recommendation;
    document.getElementById("geneticRecommendation").textContent = 
        predictionResults.algorithmComparison.genetic.recommendation;
    document.getElementById("cspRecommendation").textContent = 
        predictionResults.algorithmComparison.csp.recommendation;
    document.getElementById("greedyRecommendation").textContent = 
        predictionResults.algorithmComparison.greedy.recommendation;
}

// Populate Soil Adaptation Timeline
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
            backgroundColor: ["#388e3c", "#0288d1", "#ffa000", "#d32f2f"]
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