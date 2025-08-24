from collections import deque
import heapq
from .NodeClass import Node 
from .Problem_definition import CropPredictionProblem , CropState
class GraphSearch:
    def __init__(self, problem):
        """
        Initialize the general search process with a problem instance.
        """
        self.problem = problem
        self.use_cost = False
        self.use_heuristic = False

    def set_frontier(self, search_strategy="Greedy_search"):
        """Set up the frontier based on the search strategy."""
        if search_strategy == "A*":
            self.use_cost = True
            self.use_heuristic = True
        elif search_strategy == "Greedy_search":
            self.use_cost = False
            self.use_heuristic = True
        

    def search(self, search_strategy="A*", max_depth=float('inf'), initial_node=None):
        """Execute the search algorithm."""
        print(f"Starting {search_strategy} search...")
        
        self.set_frontier(search_strategy)
        
        # Ensure we have a valid initial state
        if not hasattr(self.problem, 'initial_state') or self.problem.initial_state is None:
            raise ValueError("Problem does not have a valid initial state")
            
        # Create root node
        root = initial_node or Node(
            state=self.problem.initial_state,
            parent=None,
            action=None,
            cost=0,
            h=self.problem.heuristic(self.problem.initial_state) if hasattr(self.problem, 'heuristic') else 0
        )
        
        print(f"Root node created with state: {root.state}")
        
        frontier = [root]
        heapq.heapify(frontier)
        self.root = root
        explored = {}
        nodes_expanded = 0

        # Track best node for each crop
        crop_candidates = {}  # {crop_name: (total_cost, node)}

        while frontier:
            current_node = heapq.heappop(frontier)
            nodes_expanded += 1
            
            print(f"Expanding node {nodes_expanded}: {current_node.state}")

            # Track last expanded for visualization
            self.last_expanded = current_node
            
            # Compute total cost f(n)
            current_total_cost = current_node.cost
            if self.use_heuristic and hasattr(self.problem, 'heuristic'):
                try:
                    heuristic_cost = self.problem.heuristic(current_node.state)
                    current_total_cost += heuristic_cost
                except Exception as e:
                    print(f"Warning: Heuristic calculation failed: {e}")

            # Check if this is a goal state
            try:
                is_goal, crop_name = self.problem.is_goal(current_node.state)
                print(f"Goal check result: is_goal={is_goal}, crop_name={crop_name}")
            except Exception as e:
                print(f"Error in goal check: {e}")
                continue

            # Update best node for this crop if it has a lower total cost
            if crop_name:
                if crop_name not in crop_candidates or current_total_cost < crop_candidates[crop_name][0]:
                    crop_candidates[crop_name] = (current_total_cost, current_node)
                    print(f"Updated candidate for {crop_name}: cost={current_total_cost}")

            if is_goal:
                print(f"Goal found after expanding {nodes_expanded} nodes")
                return current_node, crop_name, current_total_cost

            if current_node.depth >= max_depth:
                print(f"Max depth {max_depth} reached, continuing...")
                continue

            # Create state hash for exploration tracking
            try:
                state_hash = hash(tuple(current_node.state.environment))
            except Exception as e:
                print(f"Error creating state hash: {e}")
                continue

            if state_hash in explored and explored[state_hash] <= current_node.cost:
                continue

            explored[state_hash] = current_node.cost
            
            # Get valid actions
            try:
                valid_actions = self.problem.get_valid_actions(current_node.state)
                print(f"Found {len(valid_actions) if valid_actions else 0} valid actions")
            except Exception as e:
                print(f"Error getting valid actions: {e}")
                continue

            if not valid_actions:
                continue

            for action in valid_actions:
                try:
                    # Apply action to get new state
                    child_state = self.problem.apply_action(current_node.state, action)
                    if child_state is None:
                        continue
                        
                    # Calculate costs
                    action_cost = 0
                    if self.use_cost and hasattr(self.problem, 'get_action_cost'):
                        try:
                            action_cost = self.problem.get_action_cost(action)
                        except Exception as e:
                            print(f"Warning: Could not get action cost: {e}")
                    
                    new_cost = current_node.cost + action_cost
                    
                    h_value = 0
                    if self.use_heuristic and hasattr(self.problem, 'heuristic'):
                        try:
                            h_value = self.problem.heuristic(child_state)
                        except Exception as e:
                            print(f"Warning: Could not calculate heuristic: {e}")

                    child_node = Node(
                        state=child_state,
                        parent=current_node,
                        action=action,
                        cost=new_cost,
                        h=h_value
                    )

                    # Link for visualization
                    current_node.children.append(child_node)

                    # Check if we should add to frontier
                    try:
                        child_state_hash = hash(tuple(child_state.environment))
                    except Exception as e:
                        print(f"Error creating child state hash: {e}")
                        continue
                        
                    if child_state_hash not in explored or explored[child_state_hash] > child_node.cost:
                        heapq.heappush(frontier, child_node)

                except Exception as e:
                    print(f"Error processing action {action}: {e}")
                    continue

        # No exact solution found, return top 5 crops with lowest total costs
        if crop_candidates:
            top_crops = sorted(crop_candidates.items(), key=lambda x: x[1][0])[:5]
            top_crops_result = [(crop, total_cost, node) for crop, (total_cost, node) in top_crops]
            print(f"No exact solution found. Returning top {len(top_crops_result)} crops with lowest total costs after expanding {nodes_expanded} nodes.")
            return None, top_crops_result, None
        else:
            print(f"No crops found after expanding {nodes_expanded} nodes.")
            return None, [], None