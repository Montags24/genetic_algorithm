import numpy as np
import random
import math
from typing import Type
from life import Life
from darwinian_evolution import Darwinian_evolution

# Initialize parameters required for the project
NO_OF_LIVES = 700
MAX_GENERATIONS = 501
MUTATION_RATE = 0.085
MAXIMISE_FITNESS_PROXY = False
ELITISM = True
# 't_s' tournament selection, 'r_s' rank selection
SELECTION_METHOD = "r_s"
SURVIVOR_RATE = 0.5  # 350 survivors
CHILD_PROCREATION_RATE = 1  # Based on number of survivors

# Initialize parameters specific to the project
NO_OF_CITIES = 75

# Define what needs to be optimized - this represents the life's gene
cities = []
np.random.seed(seed=0)
for _ in range(NO_OF_CITIES):
    cities.append(dict(x=np.random.rand(), y=np.random.rand()))


def ga_calculate_fitness_proxy(gene):
    """
    Calculate the fitness proxy, which is used to determine the fitness of a solution.
    In this case, we want to minimize the total distance traveled.

    Args:
    - gene: List of cities (gene) representing the route.

    Returns:
    - float: The calculated distance, which is the fitness proxy.
    """
    cities = gene
    distance = 0
    for index, city in enumerate(cities):
        if index > 0:
            previous_city = cities[index - 1]
            x_distance = city["x"] - previous_city["x"]
            y_distance = city["y"] - previous_city["y"]
            this_distance = ((x_distance**2) + (y_distance**2)) ** 0.5
            distance += this_distance
    return distance


def ga_procreation(parent_1: Type[Life], parent_2: Type[Life]):
    """
    Specify how child is procreted.

    Args:
    - parent_1: Life object.
    - parent_2: Life object

    Returns:
    - child: Life object representing offspring.
    """
    # Order crossover
    child = Life(
        gene=cities,
        ga_calculate_fitness_proxy=ga_calculate_fitness_proxy,
        ga_generate_random_life=ga_generate_random_life,
        ga_mutation=ga_mutation,
    )

    child.gene = [-1] * len(parent_1.gene)

    cross_over_start = random.randint(1, len(parent_1.gene) - 1)
    cross_over_end = random.randint(1, len(parent_1.gene) - 1)

    if cross_over_start > cross_over_end:
        cross_over_start, cross_over_end = cross_over_end, cross_over_start

    child_gene_lst = []

    for i in range(cross_over_start, cross_over_end):
        child.gene[i] = parent_1.gene[i]
        child_gene_lst.append(parent_1.gene[i])

    for i, chromosome in enumerate(child.gene):
        if chromosome == -1:
            for gene in parent_2.gene:
                if gene not in child_gene_lst:
                    child.gene[i] = gene
                    child_gene_lst.append(gene)
                    break
    child.calculate_fitness_proxy()

    return child


def ga_mutation(child_gene: list) -> list:
    """
    Specify how a child's gene is mutated.

    Args:
    - child_gene: The gene of a child.

    Returns:
    - child_gene: The mutated gene of the child.
    """
    # Inverse mutation
    if random.random() < MUTATION_RATE:
        cross_over_start = random.randint(1, len(child_gene) - 1)
        cross_over_end = random.randint(1, len(child_gene) - 1)

        if cross_over_start > cross_over_end:
            cross_over_start, cross_over_end = cross_over_end, cross_over_start

        chromosomes_to_swap = []
        for i in range(cross_over_start, cross_over_end):
            chromosomes_to_swap.append(child_gene[i])

        for i in range(cross_over_start, cross_over_end):
            chromsome_to_add = chromosomes_to_swap.pop()
            child_gene[i] = chromsome_to_add

    return child_gene


def ga_generate_random_life(gene: list) -> list:
    """
    Specify how life's gene is randomized.

    Args:
    - gene: The gene to be randomized.

    Returns:
    - gene: The randomized gene of a Life object.
    """
    cities = gene
    home_city = [cities[0]]
    remaining_cities = cities[1:]
    # np.random.seed(seed=0)
    np.random.shuffle(remaining_cities)
    cities = home_city + remaining_cities
    return cities


# if __name__ == "__main__":
#     np.random.seed(seed=0)

#     darwinian_evolution = Darwinian_evolution(
#         gene=cities,
#         ga_calculate_fitness_proxy=ga_calculate_fitness_proxy,
#         ga_generate_random_life=ga_generate_random_life,
#         ga_procreation=ga_procreation,
#         ga_mutation=ga_mutation,
#         no_of_lives=NO_OF_LIVES,
#         maximise_fitness_proxy=MAXIMISE_FITNESS_PROXY,
#         max_generations=MAX_GENERATIONS,
#         elitism=ELITISM,
#         child_procreation_rate=CHILD_PROCREATION_RATE,
#         selection_method=SELECTION_METHOD,
#     )
#     darwinian_evolution.run_genetic_algorithm()

#     1 / 0  # Used to halt the execution for testing purposes
