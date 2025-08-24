from AI_engine.Utility_functions import agricultural_practices_effects, get_crop_requirements
import numpy as np
import pandas as pd
import copy
from copy import deepcopy
import math

class CropState:
    """
    Represents a state in the search space with environmental conditions and resource usage.
    """
    def __init__(self, environment, resource_usage=None, parent=None, action=None):
        # Environmental conditions (N, P, K, pH, temperature, humidity, etc.)
        self.environment = environment.copy()

        # Track resource usage (organic matter, irrigation, fertilizer)
        if resource_usage is None:
            self.resource_usage = {}
        else:
            self.resource_usage = resource_usage.copy()

        # Parent state and action taken to reach this state
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        """Two states are equal if they have the same environmental conditions"""
        if not isinstance(other, CropState):
            return False
        return np.array_equal(self.environment, other.environment)

    def __hash__(self):
        """Hash function to use state in sets/dictionaries"""
        return hash(tuple(self.environment))

class CropPredictionProblem:
    """
    Defines the crop prediction problem
    """
    def __init__(self, initial_state, data_file='Crop_Data.csv'):
        """
        Initialize the problem with initial state and crop growth zones.

        Parameters:
        -----------
        initial_state : CropState
            The initial environmental conditions
        crop_requirements : dict
            Mapping of crop names to their optimal environmental conditions ranges
        """
        self.initial_state = initial_state
        self.crop_requirements,self.dataset, self.features, self.crop_profiles =get_crop_requirements(data_file)
        self.interventions = [
            ('add_organic_matter', (0, 15)),  # tonnes/ha
            ('irrigation_frequency', (1, 6)),  # days
            ('apply_N_fertilizer', (0, 200)),  # kg/ha
            ('apply_P_fertilizer', (0, 75)),
            ('apply_K_fertilizer', (0, 150))
        ]

        self.costs={
            'add_organic_matter': 60.0,    # $ per tonne
            'apply_N_fertilizer': 1.3,     # $ per kg N (urea)
            'apply_P_fertilizer': 1.7,     # $ per kg P2O5 (DAP)
            'apply_K_fertilizer': 0.7,     # $ per kg K2O (potash)
            'irrigation_frequency': 10.0,  # $ per day between irrigations
            'no_action': 0.0              # No cost for no action
        }

        # Define feature names and their indices in the state vector
        self.feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        self.feature_indices = {feature: i for i, feature in enumerate(self.feature_names)}
    # Define feature weights to be used in the heuristic function
        self.feature_weights = {
            'rainfall': 0.188200,     # Highest weight
            'humidity': 0.182404,
            'K': 0.152758,
            'P': 0.139553,
            'N': 0.098114,
            'temperature': 0.079987,
            'ph': 0.059807            # Lowest weight
        }
    @staticmethod
    def choose_best_crop_from_labels(candidate_labels,
                                     weight_frost=1.0,
                                     weight_pest=1.0,
                                     weight_density=1.0,
                                     csv_path="Crop_Data.csv"):
        """
        From the normalized CSV, pick the label of the crop (string)
        among `candidate_labels` that minimizes:
            score = wf*frost_risk + wp*pest_pressure - wd*crop_density
        """
        df_norm = pd.read_csv(csv_path)
        best_score = float('inf')
        best_row = None

        for _, row in df_norm.iterrows():
            if row['label'] in candidate_labels:
                score = (
                    weight_frost   * row['frost_risk'] +
                    weight_pest    * row['pest_pressure'] -
                    weight_density * row['crop_density']
                )
                if score < best_score:
                    best_score = score
                    best_row = row

        if best_row is None:
            raise ValueError(f"No rows found for labels: {candidate_labels}")

        return best_row['label']  # ✅ Return just the label (string)

    def is_goal(self, current_state):
        """
        Check if the current state is a goal state (suitable for any crop).
        """
        candidates = []
        best_crop = None
        best_match_count = -1

        for crop_name, crop_ranges in self.crop_requirements.items():
            is_suitable, match_count = self._is_suitable_for_crop(current_state.environment, crop_name)

            if is_suitable:
                candidates.append(crop_name)
            elif match_count > best_match_count:
                best_match_count = match_count
                best_crop = crop_name

        if candidates:
            best_crop_label = self.choose_best_crop_from_labels(
                candidates,
                weight_frost=1.0,
                weight_pest=1.0,
                weight_density=1.0,
                csv_path="Crop_Data.csv"
            )
            return True, best_crop_label

        return False, best_crop

    def _is_suitable_for_crop(self, environment, crop_name):
        """
        Check if the environment is suitable for a specific crop.
        Returns: (is_suitable, match_count) tuple
        """
        crop_ranges = self.crop_requirements[crop_name]
        match_count = 0
        total_features = 0

        # Check each relevant environmental factor
        for feature, (min_val, max_val) in crop_ranges.items():
            idx = self.feature_indices.get(feature)
            if idx is not None and idx < len(environment):
                total_features += 1
                if min_val <= environment[idx] <= max_val:
                    match_count += 1
                else:
                    # Not in optimal range
                    pass

        # All features must match for suitability
        return match_count == total_features, match_count



    def get_valid_actions(self, state):
        """
        Dynamically generate valid actions based on available practices from the effects data.
        """
        valid_actions = []


        standard_amounts = {
           'add_organic_matter': [0, 5, 10],                 # tonnes/ha
            'apply_N_fertilizer': [0, 50, 100, 150],   # kg N/ha
            'apply_P_fertilizer': [0, 25, 50, 75],          # kg P₂O₅/ha
            'apply_K_fertilizer': [0, 50, 100, 150],        # kg K₂O/ha
            'irrigation_frequency': [1,2,3,4,5,6],          # days between irrigation
        }

        for action_type in agricultural_practices_effects.keys():
            if action_type in standard_amounts:
                for amt in standard_amounts[action_type]:
                    valid_actions.append((action_type, amt))

        # Optional: add "no action" for control scenarios
        valid_actions.append(('no_action', 0))

        return valid_actions

    def apply_action(self, state, action):
        """
        Apply an action to a state and return the new state using realistic effects data.
        """
        action_type, amount = action
        new_environment = state.environment.copy()
        new_resource_usage = state.resource_usage.copy() if state.resource_usage else {}

        if action_type in agricultural_practices_effects:
            effects = agricultural_practices_effects[action_type]["effects"]

            for feature, effect_info in effects.items():
                effect_per_unit = effect_info["effect_per_unit"]

                # Get the index of the feature from the state's feature mapping
                if feature in self.feature_indices:
                    idx = self.feature_indices[feature]
                    new_environment[idx] += amount * effect_per_unit

            # Track the applied resource
            if action_type not in new_resource_usage:
                new_resource_usage[action_type] = 0
            new_resource_usage[action_type] += amount

        # Create and return new state
        return CropState(new_environment, new_resource_usage)

    def get_action_cost(self, action):
        """
        Compute the cost (USD) of applying a given action at the specified amount.
        Unit costs and environmental factors are applied.
        """
        action_type, amount = action

        # Base costs (USD per unit action)
        base_rates = {
            'add_organic_matter': 60.0,    # $ per tonne
            'apply_N_fertilizer': 1.3,     # $ per kg N (urea)
            'apply_P_fertilizer': 1.7,     # $ per kg P2O5 (DAP)
            'apply_K_fertilizer': 0.7,     # $ per kg K2O (potash)
            'irrigation_frequency': 10.0,  # $ per day between irrigations
            'no_action': 0.0              # No cost for no action
        }



        # Use log(1 + amount) for diminishing returns
        if amount <= 0:
            return 0.0
        base_cost = base_rates.get(action_type, 0.0)
        cost = base_cost * np.log1p(amount)
        return float(cost)

    def heuristic(self, state):
        """
        Weighted heuristic function estimating cost to goal.

        Calculates how close the current environment is to any crop's optimal conditions
        using weighted cosine similarity. Returns a value that represents distance to goal,
        where lower values indicate states closer to being suitable for some crop.

        Feature weights prioritize: rainfall (0.188200), humidity (0.182404), K (0.152758),
        P (0.139553), N (0.098114), temperature (0.079987), and pH (0.059807).

        Returns:
            float: A value where lower values indicate better alignment with a crop's requirements
        """
        # Get the current environment vector
        current_environment = state.environment

        # Track the best (highest) similarity found so far
        best_similarity = -1.0  # Cosine similarity ranges from -1 to 1

        for crop_name, crop_ranges in self.crop_requirements.items():
            # Build vectors for comparison - using only features that exist in our feature_indices
            current_vector = []
            target_vector = []
            weight_vector = []

            for feature, (min_val, max_val) in crop_ranges.items():
                if feature in self.feature_indices:
                    idx = self.feature_indices[feature]

                    # Make sure the index is valid for our environment vector
                    if idx < len(current_environment):
                        current_value = current_environment[idx]
                        # Use midpoint of range as target value
                        target_value = (min_val + max_val) / 2
                        # Get the weight for this feature
                        weight = self.feature_weights.get(feature, 1.0)

                        current_vector.append(current_value)
                        target_vector.append(target_value)
                        weight_vector.append(weight)

          
            current_vector = np.array(current_vector)
            target_vector = np.array(target_vector)
            weight_vector = np.array(weight_vector)

            # Calculate weighted cosine similarity if vectors aren't empty
            if len(current_vector) > 0 and len(target_vector) > 0:
                # Apply weights to the current and target vectors
                weighted_current = current_vector * weight_vector
                weighted_target = target_vector * weight_vector

                # Compute magnitudes of weighted vectors
                norm_current = np.linalg.norm(weighted_current)
                norm_target = np.linalg.norm(weighted_target)

                # Compute similarity (avoid division by zero)
                if norm_current > 0 and norm_target > 0:
                    dot_product = np.dot(weighted_current, weighted_target)
                    similarity = dot_product / (norm_current * norm_target)
                    best_similarity = max(best_similarity, similarity)

        # Convert similarity to a distance metric (lower is better for A* search)
        # Cosine similarity ranges from -1 to 1, so this gives us a range of 0-2
        # where 0 is perfect alignment and 2 is perfect opposition
        return 1 - best_similarity


    def get_total_cost(self, g, state, use_cost, use_heuristic):
        """
        Calculate f(n) = g(n) + h(n) for a node.
        """

        total_cost = g if use_cost else 0
        if use_heuristic:
                total_cost += self.heuristic(state)
        return total_cost

    # functions for Genetic Algorithm

    def apply_interventions(self, chromosome):
        """Apply interventions to user conditions."""
        state_arr = copy.deepcopy(self.initial_state.environment)
        # convert the state from np array to dictionarry 
        state = {self.features[i]: state_arr[i] for i in range(len(self.features))}
        for i, (action, _) in enumerate(self.interventions):
            param = chromosome[i]
            effects = agricultural_practices_effects[action]["effects"]
            for feature, effect in effects.items():
                if feature in ['N', 'P', 'humidity']:  # Percentage increase
                    state[feature] *= (1 + param * effect["effect_per_unit"] / 100)
                else:  # Absolute increase (K, ph)
                    state[feature] += param * effect["effect_per_unit"]
        # Cap values
        for f in self.features:
            min_val, max_val = self.dataset[f].min(), self.dataset[f].max()
            state[f] = max(min_val, min(max_val, state[f]))
        return state

    def find_closest_crop(self, state):
        """Find crop with smallest Euclidean distance to state."""
        min_distance = float('inf')
        closest_crop = None
        for crop, means in self.crop_profiles.items():
            distance = math.sqrt(sum((state[f] - means[f]) ** 2 for f in self.features))
            if distance < min_distance:
                min_distance = distance
                closest_crop = crop
        return closest_crop, min_distance

    def evaluate(self, chromosome):  #fitness function
        """Compute fitness: distance to closest crop + cost."""
        # Apply interventions
        state = self.apply_interventions(chromosome)
        # Find closest crop
        closest_crop, distance = self.find_closest_crop(state)
        # Normalize distance
        max_distance = math.sqrt(sum((self.dataset[f].max() - self.dataset[f].min()) ** 2 for f in self.features))
        distance_score = 1 - (distance / max_distance)
        # Cost
        total_cost = sum(chromosome[i] * self.costs[action] for i, (action, _) in enumerate(self.interventions))
        max_cost = 500  # Estimated max
        cost_score = 1 - (total_cost / max_cost) if total_cost <= max_cost else 0
        # Fitness
        fitness = 0.7 * distance_score + 0.3 * cost_score
        return fitness, closest_crop

    def compute_all_suitability(self, chromosome):
        """Compute suitability scores for all crops."""
        state = self.apply_interventions(chromosome)
        max_distance = math.sqrt(sum((self.dataset[f].max() - self.dataset[f].min()) ** 2 for f in self.features))
        suitability_scores = {}
        for crop, means in self.crop_profiles.items():
            distance = math.sqrt(sum((state[f] - means[f]) ** 2 for f in self.features))
            suitability = (1 - (distance / max_distance)) * 100  # Convert to percentage
            suitability_scores[crop] = suitability
        return suitability_scores


