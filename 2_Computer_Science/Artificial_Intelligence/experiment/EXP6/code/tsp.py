import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt


class GeneticAlgTSP:

    __slots__ = ['cities', 'population', 'population_size', 'prob_crossover', 'prob_mutation']

    def __init__(self, dataset_filename: str, population_size: int = 100) -> None:
        if (not dataset_filename.endswith('.tsp')):
            print(f"File {dataset_filename} is not a TSP file")
            sys.exit(1)
        if (not os.path.exists(dataset_filename)):
            print(f"File {dataset_filename} does not exist")
            sys.exit(1)

        cities = []

        # read the cities from the dataset file
        with open(dataset_filename, 'r') as file:
            for line in file:
                if line.startswith('NODE_COORD_SECTION'):
                    break
            for line in file:
                if line.startswith('EOF'):
                    break
                cities.append(list(map(float, line.strip().split()[1:])))

        self.cities = np.array(cities)
        self.population = None
        self.population_size = population_size
        self.prob_crossover = 0.95
        self.prob_mutation = 0.1

    def generate_init_population(self) -> None:
        """Generate initial population

        Args:
            population_size (int): Number of chromosomes in the population
        """
        self.population = np.zeros((self.population_size, self.cities.shape[0]), dtype=int)
        for i in range(self.population_size):
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
        # return int(np.linalg.norm(city1 - city2))

    def fitness(self, chromosome: np.ndarray) -> float:
        """Calculate the fitness of a chromosome

        Args:
            chromosome (np.ndarray): The chromosome to calculate the fitness

        Returns:
            float: The fitness of the chromosome
        """
        total_distance = 0
        for i in range(len(chromosome)):
            total_distance += self.distance(self.cities[chromosome[i]], self.cities[chromosome[(i+1) % len(chromosome)]])
        return total_distance

    def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        """Crossover two parents to create a child (Partial-Mapped Crossover, PMX)

        Args:
            parent1 (np.ndarray): The first parent
            parent2 (np.ndarray): The second parent

        Returns:
            np.ndarray: Two children
        """

        point1 = np.random.randint(0, len(parent1))
        point2 = np.random.randint(point1, len(parent1))
        piece1 = parent1[point1:point2]
        piece2 = parent2[point1:point2]
        child1 = np.zeros(len(parent1), dtype=int)
        child2 = np.zeros(len(parent2), dtype=int)

        mapping = []
        # generate mapping
        for i in range(len(piece1)):
            p1, p2 = piece1[i], piece2[i]
            idx1, idx2 = -1, -1
            for j in range(len(mapping)):
                if p1 in mapping[j]:
                    idx1 = j
                if p2 in mapping[j]:
                    idx2 = j
            if idx1 == -1 and idx2 == -1:
                mapping.append([p1, p2])
            elif idx1 == -1:
                mapping[idx2].remove(p2)
                mapping[idx2].append(p1)
            elif idx2 == -1:
                mapping[idx1].remove(p1)
                mapping[idx1].append(p2)
            else:
                mapping.pop(idx2)

        for i in range(len(child1)):
            for m in mapping:
                if parent1[i] in m:
                    child1[i] = m[m.index(parent1[i]) - 1]
                    break
            else:
                child1[i] = parent1[i]

            for m in mapping:
                if parent2[i] in m:
                    child2[i] = m[m.index(parent2[i]) - 1]
                    break
            else:
                child2[i] = parent2[i]

        return child1, child2

    def mutate(self, chromosome: np.ndarray) -> np.ndarray:
        """Inversion Mutation

        Args:
            chromosome (np.ndarray): The chromosome to mutate

        Returns:
            np.ndarray: The mutated chromosome
        """
        point1 = np.random.randint(0, len(chromosome))
        point2 = np.random.randint(point1, len(chromosome))
        chromosome[point1:point2] = chromosome[point1:point2][::-1]
        return chromosome 

    def selection(self) -> np.ndarray:
        """Tournament selection

        Returns:
            np.ndarray: The selected parents
        """
        parents = np.zeros((2, self.population.shape[1]), dtype=int)
        for i in range(2):
            tournament = np.random.choice(self.population.shape[0], 5, replace=False)
            best = np.argmin([self.fitness(self.population[tournament[j]]) for j in range(5)])
            parents[i] = self.population[tournament[best]]
        return parents

    def iterate(self, num_iterations: int) -> np.ndarray:
        """Run the genetic algorithm for a number of iterations

        Args:
            num_iterations (int): Number of iterations to run the genetic algorithm

        Returns:
            np.ndarray: The best chromosome found
        """

        if self.population is None:
            self.generate_init_population()

        for _ in range(num_iterations):

            sys.stdout.write(f'\rIteration: {_+1}/{num_iterations}')
            sys.stdout.flush()

            new_population = np.copy(self.population)
            for _ in range(0, self.population.shape[0], 2):
                parent1, parent2 = self.selection()
                if np.random.rand() < self.prob_crossover:
                    child1, child2 = self.crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2
                if np.random.rand() < self.prob_mutation:
                    child1 = self.mutate(child1)
                if np.random.rand() < self.prob_mutation:
                    child2 = self.mutate(child2)
                new_population = np.append(new_population, [child1], axis=0)
                new_population = np.append(new_population, [child2], axis=0)
            # choose population_size best chromosomes
            self.population = new_population[np.argsort([self.fitness(new_population[i]) for i in range(new_population.shape[0])])[:self.population_size]]

        sys.stdout.write(f'\rbest fitness: {self.fitness(self.population[np.argmin([self.fitness(self.population[i]) for i in range(self.population.shape[0])])])}\n')
        sys.stdout.flush()

        best_chromosome = np.argmin([self.fitness(self.population[i]) for i in range(self.population.shape[0])])
        return self.population[best_chromosome]

    @staticmethod
    def plot_cities(cities_coords: np.ndarray, path: np.ndarray) -> None:
        """Plot the cities and the path

        Args:
            cities_coords (np.ndarray): The coordinates of the cities
            path (np.ndarray): The path to plot
        """
        plt.plot(cities_coords[path][:, 0], cities_coords[path][:, 1], 'o-')
        plt.show()


def example():

    np.random.seed(int(time.time()))

    dataset_name = 'wi29'
    tsp = GeneticAlgTSP('data/datasets/' + dataset_name + '.tsp', 100)

    start = time.time()
    best_chromosome = tsp.iterate(500)
    print(f'Time: {time.time() - start}')


    print(best_chromosome)
    GeneticAlgTSP.plot_cities(tsp.cities, best_chromosome)


if __name__ == '__main__':
    ...