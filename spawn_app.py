from flask import Flask


class Spawn_App:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.app = Flask(__name__)

    def run_app(self):
        print(f"In run app on IP: {self.ip} and port: {self.port}")

        # Your genetic algorithm logic here
        @self.app.route("/")
        def main():
            return f"Process running on IP: {self.ip} and port: {self.port}"

        @self.app.route("/get_best_life", methods=["GET"])
        def return_best_life():
            return "Started subprocess"

        self.app.run(
            debug=False, host=self.ip, port=self.port
        )  # Use different ports for different instances
