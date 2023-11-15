from flask import Flask, jsonify
import multiprocessing
from spawn_app import Spawn_App

# Dictionary to store information about spawned processes
spawned_processes = {}


def start_genetic_algorithm(ip, port):
    # Logic to start genetic algorithm on the specified IP and port
    app = Flask(__name__)
    print(f"In run app on IP: {ip} and port: {port}")

    # Your genetic algorithm logic here
    @app.route("/")
    def main():
        return "Started successfully!!!!!!!"

    app.run(
        debug=False, host=ip, port=port
    )  # Use different ports for different instances


def stop_genetic_algorithm(ip, port):
    # Logic to stop genetic algorithm on the specified IP and port
    # You might need to send a signal to the spawned process to gracefully shut down
    # Update the spawned_processes dictionary accordingly
    pass


def spawn_process(i):
    spawn_instance = Spawn_App(ip=f"127.0.0.{i}", port=5000 + i)
    spawn_instance.run_app()


if __name__ == "__main__":
    # Start the Flask app in a separate process
    flask_process = multiprocessing.Process(
        target=start_genetic_algorithm, args=("127.0.0.1", 5001)
    )
    flask_process.start()

    # Start the Spawn_App instance in the main process
    for i in range(2, 5):
        flask_process = multiprocessing.Process(target=spawn_process, args=(i,))
        flask_process.start()
