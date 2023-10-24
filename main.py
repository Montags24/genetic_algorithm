import numpy as np
import cv2
import random
import imageio
import os
import math
import threading
import time

NO_OF_CITIES = 70
NO_OF_LIVES = 2000
MAX_GENERATIONS = 200
MUTATION_RATE = 0.075
MUTATION_SWAPS = 10


def create_cities_img(life, generation_no, human_injection, size=1200):
    # Get the route from the life dictionary
    cities = life["route"]

    # Create a blank image with a white background
    bar_height = 20
    img_bar = np.zeros((size + bar_height, size, 3), dtype=np.uint8) + 255
    bar = img_bar[size:, :]
    img = img_bar[:size, :]

    # Function to draw a circle for a city
    def draw_city_circle(x, y, is_starting_city=False):
        radius = 8 if is_starting_city else 5
        color = (0, 255, 0) if is_starting_city else (255, 0, 0)
        thickness = -1
        cv2.circle(img, (x, y), radius, color, thickness)

    # Function to draw a line connecting cities
    def draw_city_line(city1, city2):
        x1, y1 = int(city1["x"] * size), int(city1["y"] * size)
        x2, y2 = int(city2["x"] * size), int(city2["y"] * size)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)  # Red lines

    if not human_injection:
        # Draw lines connecting cities and mark them as circles
        for i in range(len(cities)):
            draw_city_line(cities[i], cities[(i + 1) % len(cities)])

    for index, city in enumerate(cities):
        # Draw circles to represent cities
        x, y = int(city["x"] * size), int(city["y"] * size)
        draw_city_circle(x, y, is_starting_city=(index == 0))

        if human_injection:
            # Display the index of the city
            cv2.putText(
                img,
                str(index),
                (x - 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

    if not human_injection:
        # Display the distance and generation number
        text = f"Distance: {round(life['distance'], 2)} Gen: {generation_no}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (175, 50)
        fontScale = 1
        color = (0, 0, 0)
        thickness = 1
        img = cv2.putText(
            img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False
        )

        # Set the bar color based on the survival mechanism
        color = {
            "procreation": (0, 255, 0),
            "fittest": (255, 0, 0),
            "mutation": (0, 0, 255),
        }.get(
            life["survival_mechanism"], (0, 0, 0)
        )  # Default to black
        bar[:] = color

    return img_bar


def create_new_route(cities):
    # Initialise route with starting city
    route = [cities[0]]
    # Create list of remaining cities
    remaining_cities = cities[1:]
    # Shuffle remaining cities
    random.shuffle(remaining_cities)
    # Add remaining cities back to route
    route += remaining_cities
    return route


# Calculate distance for given route
def calculate_distance(cities):
    distance = 0
    for index, city in enumerate(cities):
        if index > 0:
            previous_city = cities[index - 1]
            x_distance = city["x"] - previous_city["x"]
            y_distance = city["y"] - previous_city["y"]
            this_distance = ((x_distance**2) + (y_distance**2)) ** 0.5
            distance += this_distance
    return distance


def calculate_fitness(lives):
    # Calculate fitness as the inverse of distance (shorter distance = higher fitness)
    fitness = 1
    for life in lives:
        life["fitness"] = fitness
        fitness -= 1 / len(lives)
    return


def select_mating_pool(lives):
    selected_routes = []

    for life in lives:
        danger = random.uniform(0, 1)
        if life["fitness"] > danger:
            life["survival_mechanism"] = "fittest"
            selected_routes.append(life)

    return selected_routes


def crossover(lives):
    crossover_routes = []

    for _ in range(len(lives)):
        father = random.choice(lives)
        mother = random.choice(lives)

        if father["fitness"] > mother["fitness"]:
            father, mother = mother, father

        father_percentage_to_inject = father["fitness"] / (
            father["fitness"] + mother["fitness"]
        )

        father_no_cities_to_inject = math.floor(
            (father_percentage_to_inject * NO_OF_CITIES) / 2
        )

        father_city_pairs_to_inject = []
        for _ in range(father_no_cities_to_inject):
            while True:
                rand_point_along_route = random.randint(1, len(father["route"]) - 2)
                if rand_point_along_route % 2 == 0:
                    rand_point_along_route -= 1
                father_city_pair = father["route"][
                    rand_point_along_route : rand_point_along_route + 2
                ]

                if father_city_pair not in father_city_pairs_to_inject:
                    father_city_pairs_to_inject.append(father_city_pair)
                    break

        child_route = []

        is_not_in_father = True

        for mother_city in mother["route"]:
            for father_city_pair in father_city_pairs_to_inject:
                if mother_city == father_city_pair[0]:
                    is_not_in_father = False
                    child_route += father_city_pair
                    break
                elif mother_city == father_city_pair[1]:
                    is_not_in_father = False
                    break
            if is_not_in_father:
                child_route.append(mother_city)

            is_not_in_father = True

        new_life = {
            "route": child_route,
            "distance": calculate_distance(child_route),
            "survival_mechanism": "procreation",
        }
        crossover_routes.append(new_life)

    return crossover_routes


def select_route_manually(cities):
    human_life = {"route": cities}

    # Create a blank route image for manual selection
    blank_route = create_cities_img(human_life, generation_no=0, human_injection=True)

    # Save the image for the current generation
    cv2.imwrite("blank_route.png", blank_route)

    # Generate a hash table of index to city numbers
    index_to_city = {i: city for i, city in enumerate(human_life["route"])}

    # Specify the route by city indices
    route_indices = [
        0,
        22,
        18,
        1,
        25,
        28,
        31,
        21,
        37,
        33,
        34,
        26,
        4,
        35,
        5,
        36,
        19,
        10,
        9,
        6,
        3,
        11,
        15,
        13,
        8,
        17,
        12,
        2,
        16,
        20,
        24,
        32,
        7,
        30,
        23,
        27,
        38,
        39,
        29,
        14,
    ]

    # Convert route indices to city coordinates
    selected_route = [index_to_city[int(index)] for index in route_indices]

    return selected_route


def mutation(lives, MUTATION_RATE):
    mutated_children = []

    for life in lives:
        if random.random() < MUTATION_RATE:
            # Perform a random swap mutation
            for _ in range(MUTATION_SWAPS):
                randint_1 = random.randint(1, len(life["route"]) - 1)
                randint_2 = random.randint(1, len(life["route"]) - 1)
                life["route"][randint_1], life["route"][randint_2] = (
                    life["route"][randint_2],
                    life["route"][randint_1],
                )

                life["distance"] = calculate_distance(life["route"])
                life["survival_mechanism"] = "mutation"
                mutated_children.append(life)

    return mutated_children


if __name__ == "__main__":
    np.random.seed(seed=0)
    cities = []
    # Generate random city coordinates
    for _ in range(NO_OF_CITIES):
        cities.append(dict(x=np.random.rand(), y=np.random.rand()))

    # # Exploration of human injection
    # human_life_to_inject = dict(
    #     route=select_route_manually(cities), fitness=0, survival_mechanism="procreation"
    # )
    # human_life_to_inject["distance"] = calculate_distance(human_life_to_inject["route"])

    # human_route_img = create_cities_img(
    #     human_life_to_inject, generation_no=0, human_injection=False
    # )
    # # Save the image for the current generation
    # cv2.imwrite(f"Human route.png", human_route_img)

    lives = []
    # lives.append(human_life_to_inject)

    # Generate random routes and calculate distances
    maximum_concurrent_threads = 20

    def threaded_create_and_calculate(
        lives, fitness=0, survival_mechanism="procreation"
    ):
        life = dict(
            route=create_new_route(cities), fitness=0, survival_mechanism="procreation"
        )
        distance = calculate_distance(life["route"])
        life["distance"] = distance
        lives.append(life)

        return

    threads = []
    time_started = time.time()
    for _ in range(NO_OF_LIVES):
        threaded_function = threaded_create_and_calculate
        kwargs = dict(fitness=0, survival_mechanism="procreation")
        args = [lives]
        thread = threading.Thread(target=threaded_function, args=args, kwargs=kwargs)
        threads.append(thread)
        thread.start()
        # Pause until active thread count is okay
        while threading.active_count() > maximum_concurrent_threads:
            time.sleep(0.01)

    while len(lives) < NO_OF_LIVES:
        time.sleep(0.01)
    time_finished = time.time()
    time_taken = time_finished - time_started
    1 / 0

    lives = sorted(lives, key=lambda x: x["distance"])
    # Create a list to store images for each generation
    generation_images = []

    for generation in range(MAX_GENERATIONS):
        print(f"-----Generation Number {generation}-----")

        calculate_fitness(lives)

        survivors = select_mating_pool(lives)
        survivors = survivors[0 : int(NO_OF_LIVES / 3)]

        children = crossover(survivors)

        mutations = mutation(children, MUTATION_RATE)

        lives = survivors + children + mutations

        lives = sorted(lives, key=lambda x: x["distance"])
        print(f"number of survivors: {len(survivors)}")
        print(f"number of children: {len(children)}")
        print(f"number of mutations: {len(mutations)}")

        min_distance_dict = min(lives, key=lambda x: x["distance"])
        print(f"Minimum distance between cities is {min_distance_dict['distance']}")

        # sorted_data = sorted(lives, key=lambda x: x["distance"])
        img_shortest_after_algo = create_cities_img(
            lives[0], generation_no=generation, human_injection=False
        )

        # Append the current generation's image to the list
        generation_images.append(img_shortest_after_algo)

        # Save the image for the current generation
        cv2.imwrite(f"generation_{generation}.png", img_shortest_after_algo)

    # Create a GIF from the list of images
    imageio.mimsave(
        "evolution.gif", generation_images, duration=0.5
    )  # Adjust the duration as needed

    # Delete all the images apart from the GIF
    for generation in range(MAX_GENERATIONS):
        image_filename = f"generation_{generation}.png"
        os.remove(image_filename)

    # 1 / 0
