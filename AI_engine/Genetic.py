import random
import copy
from AI_engine.NodeClass import Node
from .Problem_definition import CropPredictionProblem , CropState

class GeneticAlgorithm:
    """Genetic Algorithm for crop intervention optimization."""
    def __init__(self, problem, population_size=30, generations=50, mutation_rate=0.2, tournament_size=3):
        """Initialize GA."""
        self.problem = problem
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size

    def initialize_population(self):
        """Generate logical random population with zero-action chromosomes."""
        print("Initializing GA population...")
        population = []

        # Check if problem has interventions defined
        if not hasattr(self.problem, 'interventions') or not self.problem.interventions:
            print("Warning: Problem has no interventions defined")
            return []

        # Generate remaining chromosomes
        for _ in range(self.population_size):
            chromosome = []
            for i, (intervention_name, (min_val, max_val)) in enumerate(self.problem.interventions):
                try:
                    # 10% chance for zero value (except irrigation_frequency)
                    if random.random() < 0.1 and min_val == 0:
                        value = 0
                    else:
                        if min_val == 3:  # irrigation_frequency
                            value = random.randint(int(min_val), int(max_val))
                        else:
                            value = round(random.uniform(min_val, max_val), 1)  # One decimal place
                    chromosome.append(value)
                except Exception as e:
                    print(f"Error initializing intervention {intervention_name}: {e}")
                    chromosome.append(min_val)  # Default to minimum value
            
            if chromosome:  # Only add if we have valid chromosome
                population.append(chromosome)
        
        print(f"Generated population of size: {len(population)}")
        return population

    def select_parent(self, population):
        """Tournament selection."""
        if len(population) < self.tournament_size:
            tournament = population.copy()
        else:
            tournament = random.sample(population, self.tournament_size)
        
        try:
            return max(tournament, key=lambda x: self.problem.evaluate(x)[0])
        except Exception as e:
            print(f"Error in parent selection: {e}")
            return random.choice(tournament)

    def crossover(self, parent1, parent2):
        """Blend crossover."""
        child = []
        try:
            for p1, p2, (_, (min_val, max_val)) in zip(parent1, parent2, self.problem.interventions):
                alpha = random.uniform(0, 1)
                value = alpha * p1 + (1 - alpha) * p2
                value = max(min_val, min(max_val, value))
                if min_val == 3:  # irrigation_frequency
                    value = round(value)
                else:
                    value = round(value, 1)  # One decimal place
                child.append(value)
        except Exception as e:
            print(f"Error in crossover: {e}")
            # Return one of the parents as fallback
            return parent1.copy()
        
        return child

    def perform_mutation(self, individual):
        """Mutate one gene."""
        individual = copy.deepcopy(individual)
        try:
            if random.random() < self.mutation_rate:
                idx = random.randint(0, len(individual) - 1)
                min_val, max_val = self.problem.interventions[idx][1]
                delta = 0.1 * (max_val - min_val)
                value = individual[idx] + random.uniform(-delta, delta)
                value = max(min_val, min(max_val, value))
                if min_val == 3:  # irrigation_frequency
                    value = round(value)
                else:
                    value = round(value, 1)  # One decimal place
                individual[idx] = value
        except Exception as e:
            print(f"Error in mutation: {e}")
            # Return original individual if mutation fails
        
        return individual

    def evolve_population(self, population):
        """Evolve population with elitism."""
        if not population:
            return []
            
        try:
            # Keep the best individual
            best = max(population, key=lambda x: self.problem.evaluate(x)[0])
            new_population = [copy.deepcopy(best)]
            
            while len(new_population) < self.population_size:
                try:
                    parent1 = self.select_parent(population)
                    parent2 = self.select_parent(population)
                    child = self.crossover(parent1, parent2)
                    child = self.perform_mutation(child)
                    new_population.append(child)
                except Exception as e:
                    print(f"Error creating offspring: {e}")
                    # Add a random parent as fallback
                    if population:
                        new_population.append(copy.deepcopy(random.choice(population)))
                    
        except Exception as e:
            print(f"Error in population evolution: {e}")
            return population  # Return original population if evolution fails
        
        return new_population

    def solve(self, mode="classify"):
        """Run GA."""
        print(f"Starting GA in {mode} mode...")
        
        # Check if problem has required methods
        if not hasattr(self.problem, 'evaluate'):
            raise ValueError("Problem must have an 'evaluate' method")
            
        population = self.initialize_population()
        if not population:
            raise ValueError("Failed to initialize population")
            
        best_solution = None
        best_fitness = -float('inf')
        best_crop = None
        no_improvement = 0
        
        for generation in range(self.generations):
            try:
                population = self.evolve_population(population)
                if not population:
                    break
                
                # Evaluate each individual in the population using the problem's evaluate method
                # and select the best one based on fitness
                current_best = None
                current_fitness = -float('inf')
                
                for individual in population:
                    try:
                        fitness, crop = self.problem.evaluate(individual)
                        if fitness > current_fitness:
                            current_fitness = fitness
                            current_best = individual
                    except Exception as e:
                        print(f"Error evaluating individual: {e}")
                        continue

                if current_best is None:
                    print(f"No valid individuals found in generation {generation}")
                    continue
                    
                # Get the crop for the current best
                try:
                    current_fitness, current_crop = self.problem.evaluate(current_best)
                except Exception as e:
                    print(f"Error getting crop for best solution: {e}")
                    current_crop = "Unknown"

                # Update the best solution, fitness, and crop if the current solution is better
                if current_fitness > best_fitness:
                    best_solution = current_best.copy()
                    best_fitness = current_fitness
                    best_crop = current_crop
                    no_improvement = 0
                else:
                    no_improvement += 1
                    
                if generation % 10 == 0:
                    print(f"Generation {generation}: Fitness = {best_fitness:.4f}, Crop = {best_crop}")
                    
                if no_improvement >= 10:
                    print(f"Early stopping at generation {generation}")
                    break
                    
            except Exception as e:
                print(f"Error in generation {generation}: {e}")
                continue

        if best_solution is None:
            raise ValueError("GA failed to find any valid solution")

        # Compute suitability scores for all crops using the best solution
        top_crops = []
        try:
            if hasattr(self.problem, 'compute_all_suitability'):
                suitability_scores = self.problem.compute_all_suitability(best_solution)
                # Sort crops by suitability in descending order and select the top 5
                top_crops = sorted(suitability_scores.items(), key=lambda x: x[1], reverse=True)[:5]
            else:
                print("Warning: Problem does not have compute_all_suitability method")
        except Exception as e:
            print(f"Error computing suitability scores: {e}")

        # Print results based on the specified mode
        print(f"\nGA Best Solution: Fitness = {best_fitness:.4f}")
        
        # Create a dictionary mapping intervention names to their corresponding values
        if hasattr(self.problem, 'interventions') and self.problem.interventions:
            intervention_dict = dict(zip([x[0] for x in self.problem.interventions], best_solution))
            print(f"Interventions: {intervention_dict}")

        if mode == "classify":
            print("\nTop 5 Crops by Suitability:")
            for crop, suitability in top_crops:
                print(f"{crop}: {suitability:.2f}%")
        elif mode == "predict":
            pass  # In predict mode, don't print the top 5 crops

        return best_solution, best_fitness, best_crop, top_crops