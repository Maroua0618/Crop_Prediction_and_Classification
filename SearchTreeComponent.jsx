import { useState } from 'react';

function parseTreeData(fileContent) {
  const lines = fileContent.split('\n');
  const nodes = [];
  const actions = [];
  
  let currentState = {};
  let currentActionType = null;
  let currentActionValue = null;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    
    // Parse state values
    if (line.startsWith('N=')) {
      currentState.N = parseFloat(line.split('=')[1]);
    } else if (line.startsWith('P=')) {
      currentState.P = parseFloat(line.split('=')[1]);
    } else if (line.startsWith('K=')) {
      currentState.K = parseFloat(line.split('=')[1]);
    } else if (line.startsWith('temperature=')) {
      currentState.temperature = parseFloat(line.split('=')[1]);
    } else if (line.startsWith('humidity=')) {
      currentState.humidity = parseFloat(line.split('=')[1]);
    } else if (line.startsWith('ph=')) {
      currentState.ph = parseFloat(line.split('=')[1]);
    } else if (line.startsWith('rainfall=')) {
      currentState.rainfall = parseFloat(line.split('=')[1]);
      // Complete state, add to nodes
      if (Object.keys(currentState).length === 7) {
        nodes.push({...currentState});
      }
    } 
    // Parse actions
    else if (line.startsWith('action:')) {
      const actionParts = line.replace('action:', '').trim().split('(');
      if (actionParts.length === 2) {
        currentActionType = actionParts[0].trim();
        currentActionValue = parseFloat(actionParts[1].replace(')', ''));
        
        actions.push({
          type: currentActionType,
          value: currentActionValue,
          fromState: {...nodes[nodes.length - 1]}
        });
      }
    }
  }
  
  return { nodes, actions };
}

export default function SearchTreesComponent() {
  const [selectedAlgo, setSelectedAlgo] = useState('astar');
  
  // Mock data structure parsed from PDF files
  // In real implementation, this would be replaced with actual parsed data from astar_path.pdf and greedy_path.pdf
  const astarData = `N=60.00
P=20.00
K=100.00
temperature=20.00
humidity=50.00
ph=5.00
rainfall=200.00
action: add_organic_matter(20)
N=61.10
P=190.00
K=934.00
temperature=20.00
humidity=126.00
ph=5.34
rainfall=200.00
action: apply_N_fertilizer(100)
N=98.60
P=190.00
K=934.00
temperature=20.00
humidity=126.00
ph=5.34
rainfall=200.00`;

  const greedyData = `N=60.00
P=20.00
K=100.00
temperature=20.00
humidity=50.00
ph=5.00
rainfall=200.00
action: add_organic_matter(20)
N=61.10
P=190.00
K=934.00
temperature=20.00
humidity=126.00
ph=5.34
rainfall=200.00
action: apply_K_fertilizer(50)
N=61.10
P=190.00
K=984.00
temperature=20.00
humidity=126.00
ph=5.34
rainfall=200.00`;

  const { nodes: astarNodes, actions: astarActions } = parseTreeData(astarData);
  const { nodes: greedyNodes, actions: greedyActions } = parseTreeData(greedyData);
  
  const currentNodes = selectedAlgo === 'astar' ? astarNodes : greedyNodes;
  const currentActions = selectedAlgo === 'astar' ? astarActions : greedyActions;

  return (
    <div className="w-full p-4 bg-white rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-green-800">Search Tree Visualization</h3>
        <div className="flex space-x-2">
          <button 
            className={`px-3 py-1 rounded ${selectedAlgo === 'astar' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setSelectedAlgo('astar')}
          >
            A* Search
          </button>
          <button 
            className={`px-3 py-1 rounded ${selectedAlgo === 'greedy' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setSelectedAlgo('greedy')}
          >
            Greedy Search
          </button>
        </div>
      </div>
      
      <div className="overflow-auto p-4 border border-gray-200 rounded-lg mb-4 bg-gray-50 max-h-96">
        <h4 className="font-semibold mb-2">{selectedAlgo === 'astar' ? 'A*' : 'Greedy'} Search Tree Path</h4>
        
        {currentNodes.map((node, index) => (
          <div key={index} className="mb-6">
            <div className="bg-white p-3 rounded shadow-sm mb-2">
              <h5 className="font-semibold mb-1">State {index + 1}</h5>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div><span className="font-medium">N:</span> {node.N?.toFixed(2)}</div>
                <div><span className="font-medium">P:</span> {node.P?.toFixed(2)}</div>
                <div><span className="font-medium">K:</span> {node.K?.toFixed(2)}</div>
                <div><span className="font-medium">Temperature:</span> {node.temperature?.toFixed(2)}°C</div>
                <div><span className="font-medium">Humidity:</span> {node.humidity?.toFixed(2)}%</div>
                <div><span className="font-medium">pH:</span> {node.ph?.toFixed(2)}</div>
                <div><span className="font-medium">Rainfall:</span> {node.rainfall?.toFixed(2)} mm</div>
              </div>
            </div>
            
            {index < currentActions.length && (
              <div className="flex items-center mb-2 ml-6">
                <div className="h-8 w-0.5 bg-green-600 mr-3"></div>
                <div className="bg-green-100 text-green-800 p-2 rounded shadow-sm">
                  <span className="font-medium">Action:</span> {currentActions[index].type}({currentActions[index].value})
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div className="text-sm text-gray-600">
        <p>The visualization above shows the search path taken by the {selectedAlgo === 'astar' ? 'A*' : 'Greedy'} algorithm.</p>
        <p>For a complete tree visualization, download the full PDF from the algorithm output.</p>
      </div>
    </div>
  );
}