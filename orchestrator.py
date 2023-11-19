from flask import Flask, jsonify
import multiprocessing
from spawn_app import SpawnApp
import os
from config import Config
import requests
import json


config = Config()


def start_orchestrator(ip, port):
    app = Flask(__name__)
    print(f"Running orchestrator flask app on IP address: {ip} and port: {port}")

    @app.route("/")
    def main():
        return "Orchestrator has started successfully..."

    @app.route("/dashboard")
    def dashboard():
        host_addresses = config.host_addresses
        msg = {
            "best life": {},
        }
        best_fitness_proxy = 9999
        for i, host_address in enumerate(host_addresses):
            ip = host_address["ip"]
            port = host_address["port"]
            url = f"http://{ip}:{port}/get_best_life"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                fitness_proxy = data["best_fitness_proxy"]
                generation_no = data["generation_no"]
                msg[f"host_{i}"] = {
                    "Generation": generation_no,
                    "Fitness proxy": fitness_proxy,
                }
                if fitness_proxy < best_fitness_proxy:
                    best_fitness_proxy = fitness_proxy
                    msg["best life"]["Host"] = f"Host_{i}"
                    msg["best life"]["Fitness proxy"] = f"{fitness_proxy}"

        return jsonify(msg)

    app.run(debug=False, host=ip, port=port)


def spawn_process(ip, port):
    spawn_instance = SpawnApp(ip=ip, port=port)
    spawn_instance.run_app()


if __name__ == "__main__":
    # Start the Flask app in a separate process
    main_flask_process = multiprocessing.Process(
        target=start_orchestrator,
        args=(config.orchestrator_address["ip"], config.orchestrator_address["port"]),
    )
    main_flask_process.start()

    # Start the Spawn_App instance in the main process
    for host_address in config.host_addresses:
        spawned_flask_process = multiprocessing.Process(
            target=spawn_process, args=(host_address["ip"], host_address["port"])
        )
        spawned_flask_process.start()
