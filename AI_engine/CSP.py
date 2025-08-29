
import numpy as np
from collections import defaultdict, deque
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
class CSPVariable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = list(domain)

class CSPConstraint:
    def __init__(self, variables, constraint_function, is_soft=False, penalty=0):
        self.variables = variables
        self.constraint_function = constraint_function
        self.is_soft = is_soft
        self.penalty = penalty

    def is_satisfied(self, assignment):
        return self.constraint_function(assignment)

    def get_penalty(self, assignment):
        return self.penalty if self.is_soft and not self.is_satisfied(assignment) else 0

class AgriculturalCSP:
    def __init__(self, crop_requirements, initial_environment, resource_limits):
        self.crop_requirements = crop_requirements
        self.initial_environment = {f: initial_environment[i] for i, f in enumerate(['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])}
        self.resource_limits = resource_limits
        self.feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        self.variables = {}
        self.constraints = []
        self.best_assignment = {}
        self.best_score = -float('inf')
        self._initialize_variables()
        self._add_constraints()

    def _initialize_variables(self):
        domain_ranges = {
            'Fertilizer_N': np.arange(0, 201, 10),
            'Fertilizer_P': np.arange(0, 201, 10),
            'Fertilizer_K': np.arange(0, 201, 10),
            'Irrigation': np.arange(0, 301, 10),
            'Organic_Matter': np.arange(0, 21, 1),
            'Crop': list(self.crop_requirements.keys())
        }
        for var, domain in domain_ranges.items():
            self.variables[var] = CSPVariable(var, domain)

    def _add_constraints(self):
        for feature in ['N', 'P', 'K', 'temperature', 'humidity', 'ph']:
            def climate_constraint(assignment, feature=feature):
                if 'Crop' not in assignment:
                    return True
                crop = assignment['Crop']
                min_val, max_val = self.crop_requirements[crop][feature]
                return min_val <= self.initial_environment[feature] <= max_val
            self.constraints.append(CSPConstraint(['Crop'], climate_constraint))

        def water_constraint(assignment):
            if 'Crop' not in assignment or 'Irrigation' not in assignment:
                return True
            crop = assignment['Crop']
            min_val, max_val = self.crop_requirements[crop]['rainfall']
            total_water = self.initial_environment['rainfall'] + assignment['Irrigation']
            return min_val <= total_water <= max_val
        self.constraints.append(CSPConstraint(['Crop', 'Irrigation'], water_constraint))

        def fertilizer_limit(assignment):
            total_fertilizer = sum(assignment.get(f, 0) for f in ['Fertilizer_N', 'Fertilizer_P', 'Fertilizer_K'])
            return total_fertilizer <= self.resource_limits['fertilizer']
        self.constraints.append(CSPConstraint(['Fertilizer_N', 'Fertilizer_P', 'Fertilizer_K'], fertilizer_limit))

        def irrigation_limit(assignment):
            if 'Irrigation' in assignment:
                return assignment['Irrigation'] <= self.resource_limits['water']
            return True
        self.constraints.append(CSPConstraint(['Irrigation'], irrigation_limit))

        def organic_matter_limit(assignment):
            if 'Organic_Matter' in assignment:
                return assignment['Organic_Matter'] <= self.resource_limits['organic_matter']
            return True
        self.constraints.append(CSPConstraint(['Organic_Matter'], organic_matter_limit))

        def minimize_fertilizer(assignment):
            total_fertilizer = sum(assignment.get(f, 0) for f in ['Fertilizer_N', 'Fertilizer_P', 'Fertilizer_K'])
            return total_fertilizer <= 100
        self.constraints.append(CSPConstraint(['Fertilizer_N', 'Fertilizer_P', 'Fertilizer_K'], minimize_fertilizer, is_soft=True, penalty=10))

        def minimize_irrigation(assignment):
            if 'Irrigation' in assignment:
                return assignment['Irrigation'] <= 50
            return True
        self.constraints.append(CSPConstraint(['Irrigation'], minimize_irrigation, is_soft=True, penalty=5))

        def minimize_organic_matter(assignment):
            if 'Organic_Matter' in assignment:
                return assignment['Organic_Matter'] <= 5
            return True
        self.constraints.append(CSPConstraint(['Organic_Matter'], minimize_organic_matter, is_soft=True, penalty=8))

    def _compute_environmental_value(self, assignment, feature):
        base_value = self.initial_environment[feature]
        if feature == 'N':
            return base_value + (assignment.get('Fertilizer_N', 0) * 0.375 + assignment.get('Organic_Matter', 0) * 0.055)
        elif feature == 'P':
            return base_value + (assignment.get('Fertilizer_P', 0) * 0.2 + base_value * assignment.get('Organic_Matter', 0) * 0.085)
        elif feature == 'K':
            return base_value + (assignment.get('Fertilizer_K', 0) * 0.5 + assignment.get('Organic_Matter', 0) * 41.7)
        elif feature == 'ph':
            return base_value + (assignment.get('Organic_Matter', 0) * 0.017)
        elif feature == 'rainfall':
            return base_value + assignment.get('Irrigation', 0)
        return base_value

    def _evaluate_assignment(self, assignment):
        if not assignment or 'Crop' not in assignment:
            return -float('inf')
        crop = assignment['Crop']
        cost_F = sum(assignment.get(f, 0) * 1.0 for f in ['Fertilizer_N', 'Fertilizer_P', 'Fertilizer_K'])
        cost_I = assignment.get('Irrigation', 0) * 0.05
        cost_O = assignment.get('Organic_Matter', 0) * 10.0
        environment = {f: self._compute_environmental_value(assignment, f) for f in self.feature_names}
        match_count = 0
        total_features = len(self.feature_names)
        for feature, value in environment.items():
            min_val, max_val = self.crop_requirements[crop][feature]
            if min_val <= value <= max_val:
                match_count += 1
        suitability = match_count / total_features if total_features > 0 else 0
        score = suitability - (cost_F + cost_I + cost_O)
        return score

    def is_consistent(self, variable, value, assignment):
        assignment[variable] = value
        for constraint in self.constraints:
            if not constraint.is_soft and variable in constraint.variables:
                if not constraint.is_satisfied(assignment):
                    del assignment[variable]
                    return False
        del assignment[variable]
        return True

    def select_unassigned_variable(self, assignment):
        unassigned = [var for var in self.variables if var not in assignment]
        if not unassigned:
            return None
        if 'Crop' in unassigned:
            return 'Crop'
        return min(unassigned, key=lambda var: len(self.variables[var].domain))

    def order_domain_values(self, variable, assignment):
        def count_conflicts(value):
            conflicts = 0
            assignment[variable] = value
            for other_var in self.variables:
                if other_var != variable and other_var not in assignment:
                    for other_value in self.variables[other_var].domain:
                        if not self.is_consistent(other_var, other_value, assignment):
                            conflicts += 1
            del assignment[variable]
            return conflicts
        return sorted(self.variables[variable].domain, key=count_conflicts)

    def _ac3(self):
        queue = deque([(xi, xj) for c in self.constraints if not c.is_soft for xi in c.variables for xj in c.variables if xi != xj])
        while queue:
            xi, xj = queue.popleft()
            if self._revise(xi, xj):
                if not self.variables[xi].domain:
                    return False
                for c in self.constraints:
                    if not c.is_soft and xi in c.variables:
                        for xk in c.variables:
                            if xk != xi and xk != xj:
                                queue.append((xk, xi))
        return True

    def _revise(self, xi, xj):
        revised = False
        values_to_remove = []
        for x in self.variables[xi].domain:
            consistent = False
            for y in self.variables[xj].domain:
                assignment = {xi: x, xj: y}
                if all(c.is_satisfied(assignment) for c in self.constraints if not c.is_soft and set(c.variables).issubset({xi, xj})):
                    consistent = True
                    break
            if not consistent:
                values_to_remove.append(x)
                revised = True
        for x in values_to_remove:
            self.variables[xi].domain.remove(x)
        return revised

    def _forward_check(self, var, assignment):
        removals = defaultdict(list)
        for other_var in self.variables:
            if other_var != var and other_var not in assignment:
                for value in list(self.variables[other_var].domain):
                    if not self.is_consistent(other_var, value, assignment):
                        self.variables[other_var].domain.remove(value)
                        removals[other_var].append(value)
                if not self.variables[other_var].domain:
                    self._restore_domains(removals)
                    return None
        return removals

    def _restore_domains(self, removals):
        for var, values in removals.items():
            for value in values:
                if value not in self.variables[var].domain:
                    self.variables[var].domain.append(value)
            self.variables[var].domain.sort()

    def backtracking_search(self, max_iterations=1000):
        if not self._ac3():
            return self.best_assignment
        result = self._backtrack({}, 0, max_iterations)
        if result is None:
            return self.best_assignment
        return result

    def _backtrack(self, assignment, iterations, max_iterations):
        if iterations >= max_iterations:
            return None
        current_score = self._evaluate_assignment(assignment)
        if current_score > self.best_score:
            self.best_assignment = assignment.copy()
            self.best_score = current_score
        if len(assignment) == len(self.variables):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                removals = self._forward_check(var, assignment)
                if removals is not None:
                    result = self._backtrack(assignment, iterations + 1, max_iterations)
                    if result is not None:
                        return result
                    self._restore_domains(removals)
                del assignment[var]
        return None

class CSPSolver:
    def __init__(self, initial_environment, crop_requirements, resource_limits):
        self.initial_environment = initial_environment
        self.crop_requirements = crop_requirements
        self.resource_limits = resource_limits
        self.feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

    def solve(self, max_iterations=1000):
        csp = AgriculturalCSP(self.crop_requirements, self.initial_environment, self.resource_limits)
        solution = csp.backtracking_search(max_iterations)
        result = {
            'solution': solution,
            'crop': solution.get('Crop', 'None'),
            'resources': {k: v for k, v in solution.items() if k in ['Fertilizer_N', 'Fertilizer_P', 'Fertilizer_K', 'Irrigation', 'Organic_Matter']},
            'environment': {f: csp._compute_environmental_value(solution, f) for f in self.feature_names},
            'objective_score': csp._evaluate_assignment(solution),
            'alternative_crops': self._rank_alternative_crops(solution, csp),
            'constraint_satisfaction': self._check_constraints(solution, csp)
        }
        return result

    def _rank_alternative_crops(self, solution, csp):
        suitability_scores = {}
        environment = {f: csp._compute_environmental_value(solution, f) for f in self.feature_names}
        for crop, ranges in self.crop_requirements.items():
            match_count = 0
            total_features = 0
            details = []
            for feature, (min_val, max_val) in ranges.items():
                total_features += 1
                current_value = environment[feature]
                if min_val <= current_value <= max_val:
                    match_count += 1
                    details.append(f"{feature}: {current_value:.1f} ✓ (Range: {min_val}-{max_val})")
                else:
                    details.append(f"{feature}: {current_value:.1f} ✗ (Range: {min_val}-{max_val})")
            suitability = (match_count / total_features) * 100 if total_features > 0 else 0
            suitability_scores[crop] = {'percentage': suitability, 'details': details}
        return suitability_scores

    def _check_constraints(self, solution, csp):
        satisfaction = {}
        for constraint in csp.constraints:
            vars_str = ','.join(constraint.variables)
            satisfaction[vars_str] = {
                'satisfied': constraint.is_satisfied(solution),
                'is_soft': constraint.is_soft,
                'penalty': constraint.get_penalty(solution)
            }
        return satisfaction
 

def get_crop_requirements_csp(file_path=os.path.join(DATA_DIR, 'Crop_Data.csv')):
    try:
        df = pd.read_csv(file_path)
        if 'label' not in df.columns:
            raise ValueError("Error: 'label' column not found in the CSV file.")
        features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        crop_stats = df.groupby('label')[features].agg(['min', 'max'])
        crop_requirements = {}
        for crop in crop_stats.index:
            feature_ranges = {}
            for feature in features:
                min_val = crop_stats.loc[crop, (feature, 'min')]
                max_val = crop_stats.loc[crop, (feature, 'max')]
                feature_ranges[feature] = (round(min_val, 1), round(max_val, 1))
            crop_requirements[crop] = feature_ranges
        return crop_requirements
    except Exception as e:
        print(f"Error reading crop data: {e}")
        return None

def run_csp(initial_environment, crop_requirements=None, resource_limits=None, max_iterations=1000, visualize=True, mode="classify"):
    """
    Run the CSP solver for crop recommendation.

    Args:
        initial_environment: Initial environmental conditions (numpy array).
        crop_requirements: Crop requirements dictionary or None to load from file.
        resource_limits: Resource constraints dictionary.
        max_iterations: Maximum iterations for backtracking.
        visualize: Whether to generate visualizations.
        mode: 'predict' (return only the best crop with details) or 'classify' (top 5 crops with details and visualization).

    Returns:
        dict: CSP result dictionary.
    """
    if not isinstance(initial_environment, np.ndarray):
        initial_environment = np.array(initial_environment)

    if crop_requirements is None:
        crop_requirements = get_crop_requirements_csp()
    if not crop_requirements:
        print("Error: Failed to load crop requirements.")
        return None

    if resource_limits is None:
        resource_limits = {'fertilizer': 300, 'water': 300, 'organic_matter': 20}


    print("\nInitial Environment:")
    for feature, value in zip(['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'], initial_environment):
        print(f"{feature}: {value:.1f}")

    solver = CSPSolver(initial_environment, crop_requirements, resource_limits)
    result = solver.solve(max_iterations)

    # Sort crops by suitability
    sorted_crops = sorted(result['alternative_crops'].items(), key=lambda x: x[1]['percentage'], reverse=True)
        

    return result