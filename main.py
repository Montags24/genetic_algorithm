import numpy as np
import cv2
import random
import operator

NO_OF_CITIES = 20
NO_OF_LIVES = 10000
MAX_GENERATIONS = 1000


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
    home = [cities[0]]
    copy_cities = cities[1:]
    random.shuffle(copy_cities)
    route = home + copy_cities
    return route


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
    for life in lives:
        life["fitness"] = 1 / (
            life["distance"] + 1
        )  # Adding 1 to avoid division by zero
    return


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

    # Calculate fitness for each route
    calculate_fitness(lives)

    # Create images for the shortest and longest routes
    img_shortest = create_cities_img(lives[0])
    img_longest = create_cities_img(lives[-1])

    # Save images to files
    cv2.imwrite("test_shortest.png", img_shortest)
    cv2.imwrite("test_longest.png", img_longest)

    # 1 / 0
