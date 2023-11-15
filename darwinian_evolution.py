import cv2
import os
import imageio
import numpy as np
from population import Population


class Darwinian_evolution:
    """
    Orchestrates the genetic algorithm.

    Attributes:
    - population: Contains an instance of the Population class.
    - fittest_life: Contains information about the fittest life.
    - maximise_fitness_proxy: Flag indicating whether to maximize the fitness proxy.
    - max_generations: The maximum number of generations.
    - elitism: Flag indicating whether to use elitism.

    Methods:
    - save_best_life(): Updates the fittest_life attribute based on the current generation's fittest life.
    - GA_loop(): The main loop of the genetic algorithm.
    """

    def __init__(
        self,
        gene,
        ga_calculate_fitness_proxy,
        ga_generate_random_life,
        ga_procreation,
        ga_mutation,
        no_of_lives,
        maximise_fitness_proxy,
        max_generations,
        elitism,
        child_procreation_rate,
        selection_method,
    ):
        """
        Initialize a Darwinian_evolution instance.

        Args:
        - gene: Gene information relevant to the optimization problem.
        - ga_calculate_fitness_proxy: Function to calculate the fitness proxy.
        - ga_generate_random_life: Function to generate random gene information.
        - ga_selection: Function representing Darwinian Selection.
        - ga_procreation: Function representing Darwinian Procreation.
        - ga_mutation: Function for gene mutation.
        - no_of_lives: The number of individuals in the population.
        - maximise_fitness_proxy: Flag indicating whether to maximize the fitness proxy.
        - max_generations: The maximum number of generations.
        - elitism: Flag indicating whether to use elitism.
        """
        self.population = Population(
            gene=gene,
            no_of_lives=no_of_lives,
            ga_calculate_fitness_proxy=ga_calculate_fitness_proxy,
            ga_generate_random_life=ga_generate_random_life,
            ga_procreation=ga_procreation,
            ga_mutation=ga_mutation,
            initialise=True,
            maximise_fitness_proxy=maximise_fitness_proxy,
            child_procreation_rate=child_procreation_rate,
            selection_method=selection_method,
        )

        self.fittest_life = None
        self.maximise_fitness_proxy = maximise_fitness_proxy
        self.max_generations = max_generations
        self.elitism = elitism

        self.city_locations = gene

    def save_best_life(self):
        """
        This function stores the overall best life from the genetic algorithm. It adds it into the next generation to ensure that info on the best life is not lost.
        """
        current_gen_fittest_life = self.population.get_fittest()
        # On first run through
        if self.fittest_life is None:
            self.fittest_life = current_gen_fittest_life
        # All other run throughs
        else:
            overall_fittest_proxy = self.fittest_life.fitness_proxy
            current_gen_fittest_proxy = current_gen_fittest_life.fitness_proxy
            if self.maximise_fitness_proxy:
                if current_gen_fittest_proxy > overall_fittest_proxy:
                    self.fittest_life = current_gen_fittest_life
                else:
                    self.population.lives.append(self.fittest_life)
            else:
                if current_gen_fittest_proxy < overall_fittest_proxy:
                    self.fittest_life = current_gen_fittest_life
                else:
                    self.population.lives.append(self.fittest_life)

        return

    def generate_image(self, generation_no):
        # Generate an image every 10 generations
        img_shortest_route = create_cities_img(
            self.fittest_life, human_injection=False, generation_no=generation_no
        )
        cv2.imwrite(f"generation_{generation_no}.png", img_shortest_route)
        return img_shortest_route

    def create_gif(self, generation_best_route_images):
        # Create a GIF from the list of images
        file_name = str(self.fittest_life.fitness_proxy).replace(".", "-")
        imageio.mimsave(
            f"{file_name}.gif", generation_best_route_images, duration=0.5
        )  # Adjust the duration as needed

        # Delete all the images apart from the GIF
        for generation in range(self.max_generations):
            try:
                image_filename = f"generation_{generation}.png"
                os.remove(image_filename)
            except FileNotFoundError:
                pass

    def run_genetic_algorithm(self):
        # Effect of human injection
        # self.human_injection()

        generation_best_route_images = []

        # for generation_no in range(self.max_generations):
        generation_no = 0
        while True:
            print(f"--- Generation {generation_no} ---")
            # Natural selection
            self.population.survivors = self.population.selection()
            print(len(self.population.survivors))
            # Procreation
            self.population.children = self.population.procreation()
            # Mutation
            for life in self.population.children:
                life = life.mutation()
            # Update population
            self.population.lives = self.population.survivors + self.population.children
            # Get fittest life of current population
            self.population.get_fittest()
            # Save best life of generation if elitism set to True
            if self.elitism:
                self.save_best_life()
                print(f"Best proxy: {self.fittest_life.fitness_proxy}")
            else:
                print(f"Best proxy: {self.population.get_fittest().fitness_proxy}")

            generation_no += 1

            # if generation_no % 10 == 0:
            #     generation_best_route_images.append(self.generate_image(generation_no))

        self.create_gif(generation_best_route_images)

    def get_best_lives(self, no_of_lives):
        return self.population.get_best_lives(no_of_lives)

    def human_injection(self):
        """
        Method to explore the effects of human injection
        """
        life = {}
        life["gene"] = self.city_locations
        # Generate map with city locations and numbers
        blank_route = create_cities_img(life, generation_no=0, human_injection=True)
        cv2.imwrite(f"Blank route.png", blank_route)
        # Create hash table of city indexs to coords
        city_index_ht = {}
        for index, coord in enumerate(self.city_locations):
            city_index_ht[index] = coord

        chosen_route = [
            0,
            6,
            44,
            74,
            51,
            81,
            9,
            82,
            10,
            72,
            59,
            19,
            61,
            36,
            92,
            58,
            78,
            5,
            97,
            60,
            80,
            69,
            65,
            25,
            14,
            57,
            35,
            4,
            70,
            94,
            56,
            64,
            50,
            87,
            26,
            34,
            33,
            84,
            28,
            31,
            21,
            37,
            49,
            89,
            48,
            85,
            43,
            91,
            42,
            29,
            95,
            79,
            39,
            38,
            47,
            27,
            23,
            30,
            86,
            7,
            63,
            83,
            99,
            66,
            98,
            32,
            24,
            40,
            20,
            16,
            1,
            53,
            18,
            22,
            68,
            67,
            93,
            62,
            52,
            90,
            76,
            12,
            17,
            41,
            46,
            45,
            2,
            15,
            8,
            77,
            75,
            73,
            13,
            96,
            54,
            88,
            71,
            3,
            55,
            11,
        ]

        human_route = []
        for index in chosen_route:
            human_route.append(city_index_ht[index])

        # Introduce the human route into the population
        self.population.lives[0].gene = human_route
        self.population.lives[0].calculate_fitness_proxy()


def create_cities_img(life, generation_no, human_injection, size=1800):
    # Get the cities array from the life dictionary
    try:
        cities = life.gene
    except AttributeError:
        cities = life["gene"]
    # Create a blank image with a white background
    bar_height = 20
    img_bar = np.zeros((size + bar_height, size, 3), dtype=np.uint8) + 255
    bar = img_bar[size:, :]
    img = img_bar[:size, :]

    # Function to draw a circle for a city
    def draw_city_circle(x, y, is_starting_city=False):
        radius = 16 if is_starting_city else 10
        color = (0, 255, 0) if is_starting_city else (255, 0, 0)
        thickness = -1
        cv2.circle(img, (x, y), radius, color, thickness)

    # Function to draw a line connecting cities
    def draw_city_line(city1, city2):
        x1, y1 = int(city1["x"] * size), int(city1["y"] * size)
        x2, y2 = int(city2["x"] * size), int(city2["y"] * size)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)  # Red lines

    # Function to add city numbers next to dot
    def add_city_numbers(x, y, city_number):
        text = f"{city_number}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (x, y)
        fontScale = 1
        color = (0, 0, 0)
        thickness = 1
        cv2.putText(
            img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False
        )

    # Draw circles to represent cities
    for index, city in enumerate(cities):
        x, y = int(city["x"] * size), int(city["y"] * size)
        draw_city_circle(x, y, is_starting_city=(index == 0))
        if human_injection:
            add_city_numbers(x, y, index)

    if not human_injection:
        # Draw lines connecting cities and mark them as circles
        for i in range(len(cities)):
            draw_city_line(cities[i], cities[(i + 1) % len(cities)])

        # Display the distance and generation number
        text = f"Gen: {generation_no} Distance: {round(life.fitness_proxy, 2)}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (100, 50)
        fontScale = 1.5
        color = (0, 0, 0)
        thickness = 2
        img = cv2.putText(
            img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False
        )

    return img_bar
