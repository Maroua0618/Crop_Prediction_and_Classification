import random
import copy
from AI_engine.NodeClass import Node

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
        population = []

        # Generate remaining chromosomes
        for _ in range(self.population_size - 1):
            chromosome = []
            for i, (_, (min_val, max_val)) in enumerate(self.problem.interventions):
                # 10% chance for zero value (except irrigation_frequency)
                if random.random() < 0.1 and min_val == 0:
                    value = 0
                else:
                    if min_val == 3:  # irrigation_frequency
                        value = random.randint(int(min_val), int(max_val))
                    else:
                        value = round(random.uniform(min_val, max_val), 1)  # One decimal place
                chromosome.append(value)
            population.append(chromosome)
        return population

    def select_parent(self, population):
        """Tournament selection."""
        tournament = random.sample(population, self.tournament_size)
        return max(tournament, key=lambda x: self.problem.evaluate(x)[0])

    def crossover(self, parent1, parent2):
        """Blend crossover."""
        child = []
        for p1, p2, (_, (min_val, max_val)) in zip(parent1, parent2, self.problem.interventions):
            alpha = random.uniform(0, 1)
            value = alpha * p1 + (1 - alpha) * p2
            value = max(min_val, min(max_val, value))
            if min_val == 3:  # irrigation_frequency
                value = round(value)
            else:
                value = round(value, 1)  # One decimal place
            child.append(value)
        return child

    def perform_mutation(self, individual):
        """Mutate one gene."""
        individual = copy.deepcopy(individual)
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
        return individual

    def evolve_population(self, population):
        """Evolve population with elitism."""
        best = max(population, key=lambda x: self.problem.evaluate(x)[0])
        new_population = [copy.deepcopy(best)]
        while len(new_population) < self.population_size:
            parent1 = self.select_parent(population)
            parent2 = self.select_parent(population)
            child = self.crossover(parent1, parent2)
            child = self.perform_mutation(child)
            new_population.append(child)
        return new_population

    def solve(self, mode="classify"):
        """Run GA."""
        population = self.initialize_population()
        best_solution = None
        best_fitness = -float('inf')
        best_crop = None
        no_improvement = 0
        for generation in range(self.generations):
            population = self.evolve_population(population)
            # Evaluate each individual in the population using the problem's evaluate method
            # and select the best one based on fitness
            current_best = max(population, key=lambda x: self.problem.evaluate(x)[0])

            # Evaluate the current best solution using the problem's evaluate method
            # to get its fitness and predicted crop
            current_fitness, current_crop = self.problem.evaluate(current_best)

            # Update the best solution, fitness, and crop if the current solution is better
            if current_fitness > best_fitness:
                best_solution = current_best
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

        # Compute suitability scores for all crops using the best solution
        suitability_scores = self.problem.compute_all_suitability(best_solution)

        # Sort crops by suitability in descending order and select the top 5
        top_crops = sorted(suitability_scores.items(), key=lambda x: x[1], reverse=True)[:5]

        # Print results based on the specified mode
        print(f"\nBest Solution: Fitness = {best_fitness:.4f}")
        # Create a dictionary mapping intervention names to their corresponding values
        # in the best solution and print it
        print(f"Interventions: {dict(zip([x[0] for x in self.problem.interventions], best_solution))}")

        if mode == "classify":
            print("\nTop 5 Crops by Suitability:")
            for crop, suitability in top_crops:
                print(f"{crop}: {suitability:.2f}%")
        elif mode == "predict":
            pass  # In predict mode, don't print the top 5 crops

        return best_solution, best_fitness, best_crop, top_crops
    
