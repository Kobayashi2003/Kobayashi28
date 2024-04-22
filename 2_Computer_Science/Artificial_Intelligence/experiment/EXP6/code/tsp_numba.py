# This is the numba version

import time

import numba
import numpy as np
from numba import int64, float64

import matplotlib.pyplot as plt


spec = [
    ('cities', numba.float64[:, :]),
    ('population', numba.int64[:, :]),
    ('population_size', numba.int64),
    ('fitness_record', numba.float64[:]),
    ('prob_crossover', numba.float64),
    ('prob_mutation', numba.float64)
]

@numba.experimental.jitclass(spec)
class GeneticAlgTSP:

    def __init__(self, cities_coords: np.ndarray, population_size: int = 100) -> None:
        self.cities = cities_coords
        self.population_size = population_size
        self.generate_population(population_size)
        self.prob_crossover = 0.95
        self.prob_mutation = 0.1

    def generate_population(self, population_size: int) -> None:
        """Generate initial population

        Args:
            population_size (int): Number of chromosomes in the population
        """
        self.population = np.zeros((population_size, self.cities.shape[0]), dtype=int64)
        for i in range(population_size):
            self.population[i] = np.random.permutation(self.cities.shape[0])

    def distance(self, city1: np.ndarray, city2: np.ndarray) -> float:
        """Calculate the distance between two cities

        Args:
            city1 (np.ndarray): The first city [x, y]
            city2 (np.ndarray): The second city [x, y]

        Returns:
            float: The distance between the two cities 
        """
        return np.linalg.norm(city1 - city2)

    def fitness(self, chromosome: np.ndarray) -> float:
        """Calculate the fitness of a chromosome

        Args:
            chromosome (np.ndarray): The chromosome to calculate the fitness

        Returns:
            float: The fitness of the chromosome
        """
        total_distance = 0
        for i in range(len(chromosome)):
            total_distance += self.distance(self.cities[chromosome[i]], self.cities[chromosome[(i + 1) % len(chromosome)]])
        return total_distance

    def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        """Crossover operator

        Args:
            parent1 (np.ndarray): First parent
            parent2 (np.ndarray): Second parent

        Returns:
            np.ndarray: Offspring
        """

        offsprings = np.zeros((2, len(parent1)), dtype=int64)
        start = np.random.randint(len(parent1))
        end = np.random.randint(start, len(parent1))

        offsprings[0, start:end] = parent1[start:end]
        offsprings[1, start:end] = parent2[start:end]

        for i in range(len(parent2)):
            if parent2[i] not in offsprings[0]:
                for j in range(len(offsprings[0])):
                    if offsprings[0, j] == 0:
                        offsprings[0, j] = parent2[i]
                        break

        for i in range(len(parent1)):
            if parent1[i] not in offsprings[1]:
                for j in range(len(offsprings[1])):
                    if offsprings[1, j] == 0:
                        offsprings[1, j] = parent1[i]
                        break

        return offsprings

    def mutation(self, chromosome: np.ndarray) -> np.ndarray:
        """Mutation operator

        Args:
            chromosome (np.ndarray): Chromosome to mutate

        Returns:
            np.ndarray: Mutated chromosome
        """
        idx1 = np.random.randint(0, len(chromosome))
        idx2 = np.random.randint(idx1, len(chromosome))
        chromosome[idx1:idx2] = chromosome[idx1:idx2][::-1]
        return chromosome

    def selection(self, fitness_values: np.ndarray) -> np.ndarray:
        """Select the best chromosomes

        Args:
            fitness_values (np.ndarray): Fitness values of the population

        Returns:
            np.ndarray: The best chromosomes
        """
        parents = np.zeros((2, self.cities.shape[0]), dtype=int64)
        for i in range(2):
            tournament = np.random.choice(self.population_size, 5)
            best = np.argmin(fitness_values[tournament])
            parents[i] = self.population[tournament[best]]
        return parents
    
    def iterate(self, generations: int) -> np.ndarray:
        """Run the Genetic Algorithm

        Args:
            generations (int): Number of generations to run

        Returns:
            np.ndarray: The best chromosome
        """

        self.fitness_record = np.zeros(generations, dtype=float64)

        for g in range(generations):

            print(f"Generation {g+1}/{generations}")

            fitness_values = np.zeros(self.population_size * 2, dtype=float64)
            for i in range(self.population_size):
                fitness_values[i + self.population_size] = self.fitness(self.population[i])

            new_population = np.zeros((self.population_size * 2, self.cities.shape[0]), dtype=int64)
            new_population[self.population_size:] = self.population

            for i in range(0, self.population_size, 2):
                parent1, parent2 = self.selection(fitness_values[self.population_size:])

                if np.random.rand() < self.prob_crossover:
                    offspring1, offspring2 = self.crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                if np.random.rand() < self.prob_mutation:
                    offspring1 = self.mutation(offspring1)
                if np.random.rand() < self.prob_mutation:
                    offspring2 = self.mutation(offspring2)

                new_population[i] = offspring1
                new_population[i + 1] = offspring2

            for i in range(self.population_size):
                fitness_values[i] = self.fitness(new_population[i])

            self.population = new_population[np.argsort(fitness_values)][:self.population_size]
            self.fitness_record[g] = self.fitness(self.population[0])

        return self.population[0]
       

# @lambda _:_ ()
def example():
    np.random.seed(int(time.time()))

    dataset_path = 'data/datasets/lu980.tsp'

    cities_coords = []

    with open(dataset_path, 'r') as file:
        for line in file:
            if (line.startswith('NODE_COORD_SECTION')):
                break
        for line in file:
            if (line.startswith('EOF')):
                break
            cities_coords.append(list(map(float, line.split()[1:])))

    cities_coords = np.array(cities_coords)

    time_start = time.time()

    ga = GeneticAlgTSP(cities_coords, 100)
    best_chromosome = ga.iterate(20_000)

    print(f'Time: {time.time() - time_start}')
    print(f'Fitness: {ga.fitness(best_chromosome)}')
    print(f'BEST CHROMOSOME: {best_chromosome}')

    best_chromosome = np.append(best_chromosome, best_chromosome[0])
    plt.plot(cities_coords[best_chromosome][:, 0], cities_coords[best_chromosome][:, 1], 'o-')
    plt.show()
    plt.close()


if __name__ == '__main__':
    ...