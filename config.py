import numpy as np
import os


class Config:
    def __init__(self):
        # Initialize parameters required for the project
        self.no_of_lives = 700
        self.mutation_rate = 0.085
        self.maximise_fitness_proxy = False
        self.elitism = True
        # 't_s' tournament selection, 'r_s' rank selection
        self.selection_method = "r_s"
        self.survivor_rate = 0.5  # 350 survivors
        self.child_procreation_rate = 1  # Based on number of survivors

        # Initialize parameters specific to the project
        self.no_of_cities = 75

        # Define what needs to be optimized - this represents the life's gene
        self.cities = []
        np.random.seed(seed=0)
        for _ in range(self.no_of_cities):
            self.cities.append(dict(x=np.random.rand(), y=np.random.rand()))
