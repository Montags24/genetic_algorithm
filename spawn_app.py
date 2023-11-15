from flask import Flask, jsonify, request
import threading
import time
from queue import Queue
from config import Config
from genetic_algorithm_poc import (
    ga_calculate_fitness_proxy,
    ga_generate_random_life,
    ga_mutation,
    ga_procreation,
)
from darwinian_evolution import Darwinian_evolution


class Spawn_App:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.app = Flask(__name__)
        self.best_life = None
        self.is_running = False
        self.genetic_algorithm_thread = None
        self.darwinian_evolution_thread = None

    def run_genetic_algorithm(self):
        config = Config()

        darwinian_evolution = Darwinian_evolution(
            gene=config.cities,
            ga_calculate_fitness_proxy=ga_calculate_fitness_proxy,
            ga_generate_random_life=ga_generate_random_life,
            ga_procreation=ga_procreation,
            ga_mutation=ga_mutation,
            no_of_lives=config.no_of_lives,
            maximise_fitness_proxy=config.maximise_fitness_proxy,
            max_generations=100,
            elitism=config.elitism,
            child_procreation_rate=config.child_procreation_rate,
            selection_method=config.selection_method,
            ip=self.ip,
            port=self.port,
        )

        self.darwinian_evolution_thread = threading.Thread(
            target=darwinian_evolution.run_genetic_algorithm
        )
        self.darwinian_evolution_thread.start()

    def start_genetic_algorithm(self):
        self.is_running = True
        self.genetic_algorithm_thread = threading.Thread(
            target=self.run_genetic_algorithm
        )
        self.genetic_algorithm_thread.start()

    def stop_genetic_algorithm(self):
        self.is_running = False
        if self.genetic_algorithm_thread:
            self.genetic_algorithm_thread.join()

    def run_app(self):
        print(f"running app on IP: {self.ip} and port: {self.port}...")

        @self.app.route("/")
        def main():
            return f"Sub process running on IP: {self.ip} and port: {self.port}"

        @self.app.route("/get_best_life", methods=["GET"])
        def return_best_life():
            print("Handling /get_best_life request...")
            # Get the fittest life from the queue
            best_life = self.best_life
            print("Got best life:", best_life)
            return jsonify({"best_life": best_life})

        @self.app.route("/send_best_life", methods=["POST"])
        def send_best_life():
            if request.method == "POST":
                data = request.json
                print(data)
                self.best_life = data["best_life"]
                print(f"IP:{self.ip}\nBest life:{self.best_life}")
                response_data = {"message": "Received best life successfully"}
                return jsonify(response_data)

        # Start the genetic algorithm in a separate thread
        self.start_genetic_algorithm()

        # Start the Flask app
        self.app.run(
            debug=False, host=self.ip, port=self.port
        )  # Use different ports for different instances


# Uncomment the following lines to run the application
# if __name__ == "__main__":
#     spawn_instance = Spawn_App(ip="127.0.0.1", port=5001)
#     spawn_instance.run_app()
