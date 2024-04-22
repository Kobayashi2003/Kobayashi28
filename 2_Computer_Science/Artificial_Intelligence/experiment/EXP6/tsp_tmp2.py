# This is the numba.cuda version

import os
import sys
import math
import time

import matplotx 
import matplotlib.pyplot as plt

import numpy as np
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32

import pickle
import logging

from typing import Union, TypeAlias, Optional

# from tqdm import tqdm

filename : TypeAlias = str

population_init_file = 'population_init.pkl'

logging.basicConfig(level=logging.INFO, filename='genetic_algorithm.log')



class GeneticAlgorithm:

    def __init__(self, 
                 cities_coords:         Union[np.ndarray, filename],
                 population_size:       Optional[int] = 100, 
                 generations:           Optional[int] = 1000, 
                 crossover_probability: Optional[float] = 0.8, 
                 mutation_probability:  Optional[float] = 0.01,
                 *, # enforce keyword-only arguments
                 population:            Optional[np.ndarray] = None,
                 seed:                  Optional[int] = None) -> None:

        if isinstance(cities_coords, filename):
            cities_coords = GeneticAlgorithm.load_cities_coords(cities_coords)
        self.cities_coords = cities_coords
        self.population_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

        self.population = population
        self.seed = seed

        self.best_chromosome = None

    def __repr__(self) -> None:
        if self.best_chromosome is not None:
            self.plot_cities(self.cities_coords, self.best_chromosome)
            return f"Best path: {self.best_chromosome}\nFitness: {self.fitness(self.best_chromosome, self.cities_coords)}"
        return "Genetic Algorithm for Travelling Salesman Problem"

    @staticmethod
    def load_cities_coords(file_name: filename) -> np.ndarray:
        """Load cities coordinates from a file"""
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File '{file_name}' not found")
        if not os.path.isfile(file_name):
            raise ValueError(f"'{file_name}' is not a file")
        if not file_name.endswith('.tsp'):
            raise ValueError("File must be in TSP format")

        cities_coords = []

        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith('NODE_COORD_SECTION'):
                    break

            for line in file:
                if line.startswith('EOF'):
                    break
                city = line.split()
                cities_coords.append([float(city[1]), float(city[2])])

        return np.array(cities_coords)

    @staticmethod
    def distance(city1: np.ndarray, city2: np.ndarray) -> float:
        """Calculate the distance between two cities"""
        return np.linalg.norm(city1 - city2)

    @staticmethod
    def fitness(chromosome: np.ndarray, cities: np.ndarray) -> float:
        """Calculate the fitness of a chromosome"""
        total_distance = 0
        for i in range(len(chromosome)):
            total_distance += GeneticAlgorithm.distance(cities[chromosome[i]], cities[chromosome[(i + 1) % len(chromosome)]])
        return total_distance

    @staticmethod
    def plot_cities(cities_coords: np.ndarray, path: np.ndarray) -> None:
        """Plot the cities and the path"""
        plt.figure(figsize=(10, 10), dpi=100)
        plt.title("Travelling Salesman Problem")
        plt.scatter(cities_coords[:, 0], cities_coords[:, 1], c='orange', marker='o')
        for i in range(len(path) - 1):
            plt.plot([cities_coords[path[i], 0], cities_coords[path[i + 1], 0]], 
                     [cities_coords[path[i], 1], cities_coords[path[i + 1], 1]], 'b-')
        plt.plot([cities_coords[path[-1], 0], cities_coords[path[0], 0]], 
                 [cities_coords[path[-1], 1], cities_coords[path[0], 1]], 'b-')
        plt.show()
        plt.close()

    def iterate(self, num_iterations: Optional[int] = None) -> list:
        return self.run(num_iterations).tolist()

    def run(self, num_iterations: Optional[int] = None) -> np.ndarray:
        if num_iterations is not None:
            self.generations = num_iterations
        self.best_chromosome = genetic_algorithm(
                self.cities_coords, self.population_size,
                self.generations, self.crossover_probability,
                self.mutation_probability,
                population_init=self.population, seed=self.seed)
        return self.best_chromosome
    
    def set_population_size(self, population_size: int) -> None:
        self.population_size = population_size
    
    def set_generations(self, generations: int) -> None:
        self.generations = generations
    
    def set_crossover_probability(self, crossover_probability: float) -> None:
        self.crossover_probability = crossover_probability
    
    def set_mutation_probability(self, mutation_probability: float) -> None:
        self.mutation_probability = mutation_probability
    
    def set_cities_coords(self, cities_coords: np.ndarray) -> None:
        self.cities_coords = cities_coords


def genetic_algorithm(cities_coords, population_size, generations, crossover_probability, mutation_probability, *, population_init=None, seed=None):

    # CUDA kernel (these are dependent on the number of cities and the spec of your GPU)
    threads_per_block = 1024
    # blocks_per_grid = math.ceil((population_size * len(cities_coords)) / threads_per_block)
    blocks_per_grid = max(128, math.ceil((population_size * len(cities_coords)) / threads_per_block))

    init_flg = True 

    for generation in range(generations): # if you prefer a progress bar, use tqdm(range(generations)) instead

        start = time.time()

        # Check if the user wants to stop the execution
        if os.name == 'nt':
            import msvcrt
            if msvcrt.kbhit():
                match msvcrt.getch():
                    case b'Q':
                        break
                    case b'P':
                        GeneticAlgorithm.plot_cities(cities_coords, population[0])
                        msg = f'Plot Generation: {generation + 1}/{generations}'
                        print(msg)
                        logging.info(msg)
                    case b'w':
                        mutation_probability += 0.01
                        msg = f'Mutation probability: {mutation_probability:.2f}'
                        print(msg)
                        logging.info(msg)
                    case b's':
                        mutation_probability -= 0.01
                        msg = f'Mutation probability: {mutation_probability:.2f}'
                        print(msg)
                        logging.info(msg)
                    case b'a':
                        crossover_probability += 0.01
                        msg = f'Crossover probability: {crossover_probability:.2f}'
                        print(msg)
                        logging.info(msg)
                    case b'd':
                        crossover_probability -= 0.01
                        msg = f'Crossover probability: {crossover_probability:.2f}'
                        print(msg)
                        logging.info(msg)
        elif os.name == 'posix': # TODO: I am not sure if this works
            import select
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []) and sys.stdin.read(1) == 'Q':
                break

        sys.stdout.write(f'\rGeneration: {generation + 1}/{generations}')
        sys.stdout.flush()

        if init_flg:

            # init cities device
            cities_device = cuda.to_device(cities_coords)

            # init cities table device (cities table is used to speed up the crossover kernel)
            cities_table_device = cuda.device_array((population_size, len(cities_coords)), dtype=bool)

            # Generate initial population
            if population_init is None:
                population = np.zeros((population_size, len(cities_coords)), dtype=np.int64)
                for i in range(population_size):
                    population[i] = np.random.permutation(len(cities_coords))
            else:
                # copy from the input population
                population = np.zeros((population_size, len(cities_coords)), dtype=np.int64)
                population_init_len = len(population_init)
                for i in range(population_size):
                    population[i] = population_init[i % population_init_len]

            # init population device
            population_device = cuda.device_array_like(population)
            population_device.copy_to_device(population)

            # create a space on the device to store the results of each kernel
            # - fitness kernel
            fitness_kernel_result = cuda.device_array(population_size, dtype=np.float64)
            # - selection kernel
            selection_kernel_result = cuda.device_array_like(population)
            # - crossover kernel
            crossover_kernel_result = cuda.device_array_like(population)
            # - mutation kernel
            mutation_kernel_result = cuda.device_array_like(population)

            # init fitness values device
            fitness_kernel[blocks_per_grid, threads_per_block](cities_device, population_device, fitness_kernel_result)
            cuda.synchronize()
            fitness_values = fitness_kernel_result.copy_to_host()
            fitness_values_device = cuda.device_array_like(fitness_values)
            fitness_values_device.copy_to_device(fitness_values)

            # init random number generator states
            if seed is None:
                seed = int(time.time())
            np.random.seed(seed)
            rng_states = create_xoroshiro128p_states(population_size, seed=seed)

            init_flg = False

        # selection (In fact, you can also run the selection process on the GPU device,
        # but in this case, it won't get a significant speedup, so I run it on the CPU)
        new_population = np.zeros_like(population)
        for i in range(population_size):
            tournament = np.random.choice(population_size, 5, replace=False)
            best = np.argmin(fitness_values[tournament])
            new_population[i] = population[tournament[best]]
        selection_kernel_result.copy_to_device(new_population)

        # init cities table kernel
        init_cities_table_kernel[blocks_per_grid, threads_per_block](cities_table_device)
        cuda.synchronize()

        # crossover kernel 
        crossover_kernel[blocks_per_grid, threads_per_block](selection_kernel_result, crossover_probability, rng_states, cities_table_device, crossover_kernel_result)
        cuda.synchronize()

        # mutation kernel
        mutation_kernel[blocks_per_grid, threads_per_block](crossover_kernel_result, mutation_probability, rng_states, mutation_kernel_result)
        cuda.synchronize()
        new_population = mutation_kernel_result.copy_to_host()

        # fitness_kernel
        fitness_kernel[blocks_per_grid, threads_per_block](cities_device, mutation_kernel_result, fitness_kernel_result)
        cuda.synchronize()
        new_fitness_values = fitness_kernel_result.copy_to_host()

        # update population
        all_population = np.vstack([population, new_population])
        all_fitness_values = np.hstack([fitness_values, new_fitness_values])

        idx = np.argsort(all_fitness_values)
        population = all_population[idx[:population_size]]
        fitness_values = all_fitness_values[idx[:population_size]]

        population_device.copy_to_device(population)
        fitness_values_device.copy_to_device(fitness_values)

        # check if the population is valid
        if generation % 10000 == 0:
            for p in population:
                if len(set(p)) != len(cities_coords):
                    logging.error('Invalid population')
                    raise Exception('Invalid population')
            else:
                with open(population_init_file, 'wb') as f:
                    pickle.dump(population, f)
                logging.info(f'Population saved at generation {generation}, Fitness: {fitness_values[0]}')

        sys.stdout.write(f' - Best fitness: {fitness_values[0]:.2f} - Time: {time.time() - start:.5f}s\n')
        sys.stdout.flush()

    return population[0] 

@cuda.jit
def init_cities_table_kernel(cities_table):
    # max number of threads is cities_table.shape[0] * cities_table.shape[1] (population_size * cities_size)
    idx = cuda.threadIdx.x + cuda.blockDim.x * cuda.blockIdx.x
    if idx < cities_table.shape[0] * cities_table.shape[1]:
        cities_table[idx // cities_table.shape[1], idx % cities_table.shape[1]] = False

@cuda.jit
def fitness_kernel(cities_coords, population, fitness_kernel_result):
    # max number of threads is population.shape[0] (population size)
    idx = cuda.threadIdx.x + cuda.blockDim.x * cuda.blockIdx.x
    if idx < population.shape[0]: # population size 

        fitness_kernel_result[idx] = 0

        for i in range(population.shape[1]): # number of cities
            city1 = population[idx, i]
            city2 = population[idx, (i + 1) % population.shape[1]]
            fitness_kernel_result[idx] += math.sqrt((cities_coords[city1, 0] - cities_coords[city2, 0]) ** 2 +
                                                    (cities_coords[city1, 1] - cities_coords[city2, 1]) ** 2)

@cuda.jit
def crossover_kernel(population, prob_crossover, rng_states, cities_table, crossover_kernel_result):
    # max number of threads is population.shape[0] (population size)
    idx = cuda.threadIdx.x + cuda.blockDim.x * cuda.blockIdx.x
    if idx < population.shape[0]: # population size

        parent1 = population[idx]
        parent2 = population[(idx + 1) % population.shape[0]]

        start = int(xoroshiro128p_uniform_float32(rng_states, idx) * len(parent1))
        end = int(xoroshiro128p_uniform_float32(rng_states, idx) * len(parent1))

        if xoroshiro128p_uniform_float32(rng_states, idx) < prob_crossover and start != end:

            if start > end:
                start, end = end, start

            for i in range(start, end):
                crossover_kernel_result[idx, i] = parent1[i]
                cities_table[idx, parent1[i]] = True

            blank_pointer = 0
            for i in range(len(parent2)):
                if not cities_table[idx, parent2[i]]:
                    if blank_pointer == start:
                        blank_pointer = end
                    crossover_kernel_result[idx, blank_pointer] = parent2[i]
                    blank_pointer += 1

        else:
            for i in range(len(crossover_kernel_result[idx])):
                crossover_kernel_result[idx, i] = parent1[i]

@cuda.jit
def mutation_kernel(population, prob_mutation, rng_states, mutation_kernel_result):
    # max number of threads is population.shape[0] (population size)
    idx = cuda.threadIdx.x + cuda.blockDim.x * cuda.blockIdx.x
    if idx < population.shape[0]: # population size

        mutation_idx1 = int(xoroshiro128p_uniform_float32(rng_states, idx) * len(population[idx]))
        mutation_idx2 = int(xoroshiro128p_uniform_float32(rng_states, idx) * len(population[idx]))

        if xoroshiro128p_uniform_float32(rng_states, idx) < prob_mutation and mutation_idx1 != mutation_idx2:

            if mutation_idx1 > mutation_idx2:
                mutation_idx1, mutation_idx2 = mutation_idx2, mutation_idx1

            for i in range(len(mutation_kernel_result[idx])):
                if i < mutation_idx1 or i >= mutation_idx2:
                    mutation_kernel_result[idx, i] = population[idx, i]
                else:
                    mutation_kernel_result[idx, i] = population[idx, mutation_idx2 - i + mutation_idx1 - 1]

        else:
            for i in range(len(mutation_kernel_result[idx])):
                mutation_kernel_result[idx, i] = population[idx, i]


@lambda _:_ ()
def example2():
    dataset_path = 'data/datasets/ja9847.tsp'

    population_size = 1000
    generations = 10_000_000
    crossover_probability = 0.95
    mutation_probability = 0.9

    cities_coords = []

    with open(dataset_path, 'r') as file:
        for line in file:
            if line.startswith('NODE_COORD_SECTION'):
                break
        for line in file:
            if line.startswith('EOF'):
                break
            cities_coords.append(list(map(float, line.split()[1:])))
    cities_coords = np.array(cities_coords)

    population_init = None
    if os.path.exists(population_init_file):
        try:
            with open(population_init_file, 'rb') as f:
                population_init = pickle.load(f)
            logging.info('Population loaded')
        except:
            logging.warning('Invalid population file')

    start = time.time()
    logging.info(f'Starting genetic algorithm at {time.ctime()}')
    best_chromosome = genetic_algorithm(cities_coords=cities_coords, 
                                        population_size=population_size, 
                                        generations=generations, 
                                        crossover_probability=crossover_probability, 
                                        mutation_probability=mutation_probability,
                                        population_init=population_init)
    logging.info(f'Genetic algorithm finished at {time.ctime()}')
    assert len(np.unique(best_chromosome)) == len(cities_coords)
    print(f'\nTime: {time.time() - start}')

    plot_title = (f'{dataset_path.split("/")[-1].split(".")[0]}' +
             f'\nTime: {time.time() - start}' +
             f'\nPopulation size: {population_size}' +
             f'\nCrossover probability: {crossover_probability}' +
             f'\nMutation probability: {mutation_probability}')

    with plt.style.context(matplotx.styles.onedark):
        plt.figure(figsize=(10, 10), dpi=100)
        plt.title(plot_title)
        plt.scatter(cities_coords[:, 0], cities_coords[:, 1], c='orange', zorder=1)
        for i in range(len(best_chromosome) - 1):
            city1 = best_chromosome[i]
            city2 = best_chromosome[i + 1]
            plt.plot([cities_coords[city1, 0], cities_coords[city2, 0]], [cities_coords[city1, 1], cities_coords[city2, 1]], c='blue', zorder=2)
        plt.plot([cities_coords[best_chromosome[-1], 0], cities_coords[best_chromosome[0], 0]], [cities_coords[best_chromosome[-1], 1], cities_coords[best_chromosome[0], 1]], c='blue', zorder=2)

        if not os.path.exists('data/img'):
            os.makedirs('data/img')
        plt.savefig(f'data/img/{dataset_path.split("/")[-1].split(".")[0]}.png')
        plt.show()
        plt.close()

# @lambda _:_ ()
def example1():
    dataset_path = 'data/datasets/qa194.tsp'
    ga = GeneticAlgorithm(dataset_path)
    solution = ga.iterate(10_000)
    print(ga)


if __name__ == "__main__":
    ...
