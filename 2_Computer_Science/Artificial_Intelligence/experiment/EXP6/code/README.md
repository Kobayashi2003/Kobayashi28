# LAB6 高级搜索

code文件夹下有三个文件，分别为`tsp.py`、`tsp_numba.py`和`tsp_cuda.py`。

三个文件分别对应了GA算法的一般实现、numba类优化实现以及cuda优化实现。

下面给出各个文件的运行样例：（推荐在python 3.10.9左右的版本进行运行）

## tsp.py

请在运行之前确保已经安装了numpy以及matplotlib库

```py
def example():

    np.random.seed(int(time.time()))

    dataset_name = 'wi29'
    tsp = GeneticAlgTSP('data/datasets/' + dataset_name + '.tsp', 100)

    start = time.time()
    best_chromosome = tsp.iterate(500)
    print(f'Time: {time.time() - start}')


    print(best_chromosome)
    GeneticAlgTSP.plot_cities(tsp.cities, best_chromosome)
```

对于该版本，若想要使用初始的种群，请在创建`GeneticAlgTSP`对象时将初始种群赋给`tsp.population`

## tsp_numba.py

请在运行之前确保已经安装了numpy、matplotlib以及numba库

```py
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
```

该版本不支持自定义初始种群


### tsp_cuda.py

请在运行之前确保已经安装了typing_extension、numpy、matplotlib以及numba库

```py
def example():
    dataset_path = 'data/datasets/lu980.tsp'
    ga = GeneticAlgorithm(dataset_path)
    solution = ga.iterate(50_000)
    print(ga)
```

对于该版本，若想要使用初始的种群，可以使用：

```py
# initial_population 的 population_size 可与 GeneticAlgorithm 的 population_size 不同，但请务必保证二者的城市数量相同
ga = GeneticAlgorithm(dataset_path, population=initial_population)
```

此外，我在data文件夹中提供了ja9847的迭代数据，若想使用它，可以使用`pickle`库进行读取：

```py
import pickle

with open('data/ja9847.pkl', 'rb') as file:
    initial_population = pickle.load(file)
```