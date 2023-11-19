import time
from config import Config
from genetic_algorithm_poc import (
    ga_calculate_fitness_proxy,
    ga_generate_random_life,
    ga_mutation,
    ga_procreation,
)
from darwinian_evolution import Darwinian_evolution


class TestGeneticAlgorithm:
    def __init__(self):
        self.config = Config()

        self.darwinian_evolution = Darwinian_evolution(
            gene=self.config.cities,
            ga_calculate_fitness_proxy=ga_calculate_fitness_proxy,
            ga_generate_random_life=ga_generate_random_life,
            ga_procreation=ga_procreation,
            ga_mutation=ga_mutation,
            no_of_lives=self.config.no_of_lives,
            maximise_fitness_proxy=self.config.maximise_fitness_proxy,
            max_generations=100,
            elitism=self.config.elitism,
            child_procreation_rate=self.config.child_procreation_rate,
            selection_method=self.config.selection_method,
            ip="test"
            port=self.port,
        )

    def run_algorithm(self):
        self.darwinian_evolution.run_genetic_algorithm()


if __name__ == "__main__":
    test_genetic_algorithm = TestGeneticAlgorithm
    test_genetic_algorithm.run_algorithm()
