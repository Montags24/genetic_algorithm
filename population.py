from life import Life
import random
import math
import time
import multiprocessing
from functools import partial


class Population:
    """
    Represents a population of individuals and provides information about them.

    Attributes:
    - lives: A list of Life objects, each containing gene information.
    - survivors: Proportion of lives that survives the selection process.
    - children: Populated with offspring from survivors.
    - fittest: Life object with the best fitness value.

    Methods:
    - get_fittest(): Calculates and returns the Life object with the best fitness value.
    - selection(): Represents the selection process, implemented by a user-defined function.
    - procreation(): Represents the procreation process, implemented by a user-defined function.
    """

    def __init__(
        self,
        no_of_lives,
        gene,
        ga_calculate_fitness_proxy,
        ga_generate_random_life,
        # ga_selection,
        ga_procreation,
        ga_mutation,
        initialise,
        maximise_fitness_proxy,
        child_procreation_rate,
        selection_method,
    ):
        """
        Initialize a Population instance.

        Args:
        - no_of_lives: The number of individuals in the population.
        - gene: Gene information relevant to the optimization problem.
        - ga_calculate_fitness_proxy: Function to calculate the fitness proxy.
        - ga_generate_random_life: Function to generate random gene information.
        - ga_selection: Function representing Darwinian Selection.
        - ga_procreation: Function representing Darwinian Procreation.
        - ga_mutation: Function for gene mutation.
        - initialise: Boolean flag to perform initial population generation.
        - maximise_fitness_proxy: Flag indicating whether to maximize the fitness proxy.
        - child_procreation_rate: Number of children = Number of survivors * procreation rate
        """
        self.lives = []
        self.survivors = []
        self.children = []
        self.fittest = None
        # Store the functions for selection and procreation
        self.procreation_func = ga_procreation
        self.child_procreation_rate = child_procreation_rate
        self.selection_method = selection_method
        # Store the boolean for maximise_fitness_proxy
        self.maximise_fitness_proxy = maximise_fitness_proxy

        if initialise:
            for _ in range(0, no_of_lives):
                life = Life(
                    gene=gene,
                    ga_calculate_fitness_proxy=ga_calculate_fitness_proxy,
                    ga_generate_random_life=ga_generate_random_life,
                    ga_mutation=ga_mutation,
                )
                self.lives.append(life)
            self.get_fittest()

    def get_fittest(self):
        if self.maximise_fitness_proxy:
            self.lives = sorted(self.lives, key=lambda x: x.fitness_proxy, reverse=True)
        else:
            self.lives = sorted(
                self.lives, key=lambda x: x.fitness_proxy, reverse=False
            )
        self.fittest = self.lives[0]
        return self.fittest

    def selection(self):
        if self.selection_method == "t_s":
            self.survivors = self.tournament_selection()
        elif self.selection_method == "r_s":
            pass
        else:
            pass
            # self.survivors = self.selection_func(self.lives)
        return self.survivors

    def procreation(self):
        self.children = []
        no_of_children = len(self.survivors) * self.child_procreation_rate
        for _ in range(no_of_children):
            parent_1 = random.choice(self.survivors)
            parent_2 = random.choice(self.survivors)
            self.children.append(self.procreation_func(parent_1, parent_2))
        return self.children

    # # Function to generate a single child
    # def generate_single_child(self, _):
    #     parent_1 = random.choice(self.survivors)
    #     parent_2 = random.choice(self.survivors)
    #     return self.procreation_func(parent_1, parent_2)

    # def procreation(self):
    #     self.children = []
    #     no_of_children = len(self.survivors) * self.child_procreation_rate

    #     # Number of parallel processes to run
    #     num_processes = multiprocessing.cpu_count()

    #     # Create a pool of worker processes
    #     pool = multiprocessing.Pool(processes=num_processes)

    #     # Use the pool to generate children in parallel
    #     generate_single_child_partial = partial(self.generate_single_child)
    #     children = pool.map(generate_single_child_partial, range(no_of_children))

    #     # Close the pool
    #     pool.close()
    #     pool.join()

    #     # Add the children to the list
    #     self.children.extend(children)

    #     return self.children

    def tournament_selection(self):
        """
        Perform Darwinian selection to choose survivors from the initial population.

        Args:
        - population: List of Life objects representing the current population.

        Returns:
        - survivors: List of selected Life objects.
        """
        # Tournament selection
        tournament_size = 5
        survivor_rate = 0.5
        population_size = len(self.lives)
        survivors = []
        tournament_pop = []

        def tournament_selection():
            for _ in range(tournament_size):
                tournament_pop.append(random.choice(self.lives))
            return tournament_pop_get_fittest()

        def tournament_pop_get_fittest():
            if self.maximise_fitness_proxy:
                sorted_list = sorted(
                    tournament_pop, key=lambda x: x.fitness_proxy, reverse=True
                )
            else:
                sorted_list = sorted(
                    tournament_pop, key=lambda x: x.fitness_proxy, reverse=False
                )
            return sorted_list[0]

        for _ in range(math.floor(population_size * survivor_rate)):
            survivor = tournament_selection()
            survivors.append(survivor)
            tournament_pop = []

        return survivors

    def rank_selection(self):
        pass

    def roulette_wheel_selection(self):
        pass