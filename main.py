import numpy as np
import cv2
import random
import operator
import imageio
import os

NO_OF_CITIES = 70
NO_OF_LIVES = 1000
MAX_GENERATIONS = 200
MUTATION_RATE = 0.1


def create_cities_img(life, size=600):
    # Get the route from the life dictionary
    cities = life["route"]

    # Create a blank image with a white background
    img = np.zeros((size, size, 3), dtype=np.uint8) + 255

    # Draw lines connecting cities and mark them as circles
    for index, city in enumerate(cities):
        x = int(city["x"] * size)
        y = int(city["y"] * size)
        previous_city = cities[index - 1]
        previous_x = int(previous_city["x"] * size)
        previous_y = int(previous_city["y"] * size)
        line_colour = (0, 0, 255)  # Red lines
        cv2.line(img, (x, y), (previous_x, previous_y), line_colour, thickness=2)

    for index, city in enumerate(cities):
        # Draw circles to represent cities
        x = int(city["x"] * size)
        y = int(city["y"] * size)
        img[y][x] = 0
        center_coordinates = (x, y)
        radius = 5
        color = (255, 0, 0)  # Blue circles (b, g, r)
        thickness = -1
        if index == 0:
            radius = 8
            color = (0, 255, 0)  # Green circle for the starting city
        cv2.circle(img, center_coordinates, radius, color, thickness)

        # Display the distance on the image
        text = f"Distance: {round(life['distance'], 2)}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (330, 50)  # Coordinates from bottom left of text
        fontScale = 1
        color = (0, 0, 0)
        thickness = 1
        img = cv2.putText(
            img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False
        )

    return img


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
            selected_routes.append(life)

    return selected_routes


# def crossover(lives):
#     crossover_routes = []
#     for _ in range(len(lives)):
#         new_life = {}
#         new_route = []
#         route_1 = random.choice(lives)["route"]
#         route_2 = random.choice(lives)["route"]
#         for i in range(len(route_1)):
#             if i == 0:
#                 new_route.append(route_1[i])
#             else:
#                 randint = random.randint(0, 1)
#                 if randint == 0:
#                     for city in route_1:
#                         if city not in new_route:
#                             new_route.append(city)
#                             break
#                 else:
#                     for city in route_2:
#                         if city not in new_route:
#                             new_route.append(city)
#                             break
#         new_life["route"] = new_route
#         new_life["distance"] = calculate_distance(new_route)
#         crossover_routes.append(new_life)
#     return crossover_routes


def crossover(lives):
    crossover_routes = []

    for _ in range(len(lives)):
        parent1 = random.choice(lives)
        parent2 = random.choice(lives)

        # Choose two random crossover points
        idx1, idx2 = random.sample(range(len(parent1["route"])), 2)
        start_idx, end_idx = min(idx1, idx2), max(idx1, idx2)

        # Create a copy of the parent 1 route and fill the gap with cities from parent 2
        child_route = [None] * len(parent1["route"])
        child_route[start_idx : end_idx + 1] = parent1["route"][start_idx : end_idx + 1]

        parent2_iter = (city for city in parent2["route"] if city not in child_route)

        for i in range(len(child_route)):
            if child_route[i] is None:
                child_route[i] = next(parent2_iter)

        new_life = {"route": child_route, "distance": calculate_distance(child_route)}
        crossover_routes.append(new_life)

    return crossover_routes


def mutation(lives, MUTATION_RATE):
    best_life = min(lives, key=lambda x: x["distance"])

    for life in lives:
        if random.random() < mutation_rate:
            # Perform a random swap mutation
            randint_1 = random.randint(0, len(life["route"]) - 1)
            randint_2 = random.randint(0, len(life["route"]) - 1)
            temp_route = life["route"][randint_1]
            life["route"][randint_1] = life["route"][randint_2]
            life["route"][randint_2] = temp_route
            life["distance"] = calculate_distance(life["route"])

            # Preserve the best solution found so far
            if life["distance"] > best_life["distance"]:
                life["route"] = best_life["route"]
                life["distance"] = best_life["distance"]

    return lives


if __name__ == "__main__":
    np.random.seed(seed=0)
    cities = []
    lives = []

    # Generate random city coordinates
    for _ in range(NO_OF_CITIES):
        cities.append(dict(x=np.random.rand(), y=np.random.rand()))

    # Generate random routes and calculate distances
    for _ in range(NO_OF_LIVES):
        life = dict(route=create_new_route(cities), fitness=0)
        distance = calculate_distance(life["route"])
        life["distance"] = distance
        lives.append(life)

    sorted_data = sorted(lives, key=lambda x: x["distance"])

    # Create a list to store images for each generation
    generation_images = []

    for generation in range(MAX_GENERATIONS):
        print(f"---Generation Number {generation}---")

        calculate_fitness(lives)

        survivors = select_mating_pool(lives)

        children = crossover(survivors)

        mutations = mutation(children)

        lives = survivors + mutations

        lives = sorted(lives, key=lambda x: x["distance"])
        print(f"number of survivors: {len(survivors)}")
        print(f"number of mutations: {len(mutations)}")

        min_distance_dict = min(lives, key=lambda x: x["distance"])
        print(f"Minimum distance between cities is {min_distance_dict['distance']}")

        sorted_data = sorted(lives, key=lambda x: x["distance"])
        img_shortest_after_algo = create_cities_img(sorted_data[0])

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
