from collections import deque
import heapq
from .NodeClass import Node 

class GraphSearch:
    def __init__(self, problem):
        """
        Initialize the general search process with a problem instance.
        """
        self.problem = problem
        self.use_cost = True
        self.use_heuristic = False

    def set_frontier(self, search_strategy="Greedy_search"):
        """Set up the frontier based on the search strategy."""
        if search_strategy == "A*":
            self.use_cost = True
            self.use_heuristic = True
        elif search_strategy == "Greedy_search":
            self.use_cost = False
            self.use_heuristic = True
        else:
            raise ValueError(f"Unsupported search strategy: {search_strategy}")

    def search(self, search_strategy="A*", max_depth=float('inf'), initial_node=None):
        self.set_frontier(search_strategy)
        root = initial_node or Node(
            state=self.problem.initial_state,
            parent=None,
            action=None,
            cost=0,
            h=self.problem.heuristic(self.problem.initial_state)
        )
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

             # Track last expanded for visualization
            self.last_expanded = current_node
            # Compute total cost f(n)
            current_total_cost = (
                current_node.cost + self.problem.heuristic(current_node.state)
                if self.use_heuristic else current_node.cost
            )

            is_goal, crop_name = self.problem.is_goal(current_node.state)

            # Update best node for this crop if it has a lower total cost
            if crop_name:
                if crop_name not in crop_candidates or current_total_cost < crop_candidates[crop_name][0]:
                    crop_candidates[crop_name] = (current_total_cost, current_node)

            if is_goal:
                print(f"Goal found after expanding {nodes_expanded} nodes")
                return current_node, crop_name, current_total_cost

            if current_node.depth >= max_depth:
                continue

            state_hash = hash(tuple(current_node.state.environment))
            if state_hash in explored and explored[state_hash] <= current_node.cost:
                continue

            explored[state_hash] = current_node.cost
            valid_actions = self.problem.get_valid_actions(current_node.state)

            for action in valid_actions:
                child_state = self.problem.apply_action(current_node.state, action)
                action_cost = self.problem.get_action_cost(action)
                new_cost = current_node.cost + (action_cost if self.use_cost else 0)
                h_value = self.problem.heuristic(child_state) if self.use_heuristic else 0

                child_node = Node(
                    state=child_state,
                    parent=current_node,
                    action=action,
                    cost=new_cost,
                    h=h_value
                )

                # link for visualization
                current_node.children.append(child_node)

                child_state_hash = hash(tuple(child_state.environment))
                if child_state_hash not in explored or explored[child_state_hash] > child_node.cost:
                    heapq.heappush(frontier, child_node)

        # No exact solution found, return top 5 crops with lowest total costs
        top_crops = sorted(crop_candidates.items(), key=lambda x: x[1][0])[:5]
        top_crops_result = [(crop, total_cost, node) for crop, (total_cost, node) in top_crops]
        print(f"No exact solution found. Returning top 5 crops with lowest total costs after expanding {nodes_expanded} nodes.")
        return None, top_crops_result, None

