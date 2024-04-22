import sys
import math
import time
import numpy as np
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32

import msvcrt

def genetic_algorithm(cities_coords, population_size, generations, crossover_probability, mutation_probability):

    # Generate initial population
    population = np.zeros((population_size, len(cities_coords)), dtype=np.int64)
    for i in range(population_size):
        population[i] = np.random.permutation(len(cities_coords))

    # CUDA kernel
    threads_per_block = 1024
    blocks_per_grid = math.ceil((population_size * len(cities_coords)) / threads_per_block)

    # fitness kerbel
    fitness_kernel_result = cuda.device_array(population_size, dtype=np.float64)
    # selection kernel
    selection_kernel_result = cuda.device_array_like(population)
    # crossover kernel
    crossover_kernel_result = cuda.device_array_like(population)
    # mutation kernel
    mutation_kernel_result = cuda.device_array_like(population)

    population_bak = population.copy()

    init_flg = True 

    for generation in range(generations):

        start = time.time()

        if msvcrt.kbhit() and msvcrt.getch() == b'Q':
            break

        sys.stdout.write(f'\rGeneration: {generation + 1}/{generations}')
        sys.stdout.flush()

        if init_flg:

            # init cities device
            cities_device = cuda.to_device(cities_coords)

            # init cities table device (cities table is used to speed up the crossover kernel)
            cities_table_device = cuda.device_array((population_size, len(cities_coords)), dtype=bool)

            # init population device
            population_device = cuda.device_array_like(population)
            population_device.copy_to_device(population)

            # init fitness values device
            fitness_kernel[blocks_per_grid, threads_per_block](cities_device, population_device, fitness_kernel_result)
            cuda.synchronize()
            fitness_values = fitness_kernel_result.copy_to_host()
            fitness_values_device = cuda.device_array_like(fitness_values)
            fitness_values_device.copy_to_device(fitness_values)

            # init rng states
            rng_states = create_xoroshiro128p_states(threads_per_block * blocks_per_grid, seed=int(time.time()))

            init_flg = False


        # selection kernel
        selection_kernel[blocks_per_grid, threads_per_block](population_device, fitness_values_device, rng_states, selection_kernel_result)
        cuda.synchronize()

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

        if generation % 1000 == 0:

            for p in population:
                if len(set(p)) != len(cities_coords):
                    # raise Exception('Invalid population')
                    sys.stdout.write('\033[91m' + ' - Invalid population' + '\033[0m\n')
                    population = population_bak.copy()
                    init_flg = True
                    break
            else:
                population_bak = population.copy()

        sys.stdout.write(f' - Best fitness: {fitness_values[0]:.2f} - Time: {time.time() - start:.5f}s\n')

    return population[0], generation

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
def selection_kernel(population, fitness_values, rng_states, selection_kernel_result):
    # max number of threads is population.shape[0] (population size)
    idx = cuda.threadIdx.x + cuda.blockDim.x * cuda.blockIdx.x
    if idx < population.shape[0]:

        random_idx = int(xoroshiro128p_uniform_float32(rng_states, idx) * population.shape[0])
        min_idx = random_idx
        min_values = fitness_values[random_idx]

        for _ in range(5):
            random_idx = int(xoroshiro128p_uniform_float32(rng_states, idx) * population.shape[0])
            if fitness_values[random_idx] < min_values:
                min_values = fitness_values[random_idx]
                min_idx = random_idx

        for i in range(len(selection_kernel_result[idx])):
            selection_kernel_result[idx, i] = population[min_idx, i]

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



def load_dataset(dataset_path: str) -> np.ndarray:
    import os
    import sys

    if not os.path.exists(dataset_path):
        sys.exit(f'Dataset not found: {dataset_path}')
    if not dataset_path.endswith('.tsp'):
        sys.exit('Dataset must be a .tsp file')

    skip_rows = 0
    with open(dataset_path, 'r') as file:
        for line in file:
            skip_rows += 1
            if line.startswith('NODE_COORD_SECTION'):
                break

    return np.loadtxt(dataset_path, delimiter=' ', skiprows=skip_rows, usecols=(1, 2))

def draw_plot(cities_coords: np.ndarray, best_chromosome: np.ndarray, img_title: str, save_name: str) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 10), dpi=100)
    plt.title(img_title)
    plt.scatter(cities_coords[:, 0], cities_coords[:, 1], c='orange', zorder=1)
    for i in range(len(best_chromosome) - 1):
        city1 = best_chromosome[i]
        city2 = best_chromosome[i + 1]
        plt.plot([cities_coords[city1, 0], cities_coords[city2, 0]], [cities_coords[city1, 1], cities_coords[city2, 1]], c='blue', zorder=2)
    plt.plot([cities_coords[best_chromosome[-1], 0], cities_coords[best_chromosome[0], 0]], [cities_coords[best_chromosome[-1], 1], cities_coords[best_chromosome[0], 1]], c='blue', zorder=2)
    plt.savefig(save_name)
    plt.show()
    plt.close()

if __name__ == "__main__":
    # dataset_path = 'data/datasets/wi29.tsp'
    # dataset_path = 'data/datasets/dj38.tsp'
    # dataset_path = 'data/datasets/qa194.tsp'
    # dataset_path = 'data/datasets/lu980.tsp'
    dataset_path = 'data/datasets/ja9847.tsp'

    population_size = 1000
    generations = 5_000_000
    crossover_probability = 0.95
    mutation_probability = 0.7

    cities_coords = load_dataset(dataset_path)

    start = time.time()
    best_chromosome, g = genetic_algorithm(cities_coords=cities_coords, 
                                        population_size=population_size, 
                                        generations=generations, 
                                        crossover_probability=crossover_probability, 
                                        mutation_probability=mutation_probability)

    print(f'\nTime: {time.time() - start}')
    # count different cities in best chromosome
    print(f'Unique cities: {len(np.unique(best_chromosome))}')

    title = (f'{dataset_path.split("/")[-1].split(".")[0]}' +
             f'\nTime: {time.time() - start}' +
             f'\nPopulation size: {population_size}' +
             f'\nGenerations: {g}' +
             f'\nCrossover probability: {crossover_probability}' +
             f'\nMutation probability: {mutation_probability}')

    best_chromosome = np.append(best_chromosome, best_chromosome[0])
    draw_plot(cities_coords, best_chromosome, save_name=f'data/img/plot_{dataset_path.split("/")[-1].split(".")[0]}.png', img_title=title)
