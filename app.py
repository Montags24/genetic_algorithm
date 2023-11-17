from flask import Flask, jsonify
import multiprocessing
from spawn_app import SpawnApp
import os


def start_orchestrator(ip, port):
    app = Flask(__name__)
    print(f"Running orchestrator flask app on IP address: {ip} and port: {port}")

    @app.route("/")
    def main():
        return "Orchestrator has started successfully..."

    app.run(debug=False, host=ip, port=port)


def spawn_process(i):
    spawn_instance = SpawnApp(ip=f"127.0.0.{i}", port=5000 + i)
    spawn_instance.run_app()


if __name__ == "__main__":
    # Start the Flask app in a separate process
    main_flask_process = multiprocessing.Process(
        target=start_orchestrator, args=("127.0.0.1", 5001)
    )
    main_flask_process.start()

    total_no_of_threads = os.cpu_count()

    # Start the Spawn_App instance in the main process
    for i in range(total_no_of_threads - 1):
        spawned_flask_process = multiprocessing.Process(target=spawn_process, args=(i,))
        spawned_flask_process.start()
