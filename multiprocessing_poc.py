from multiprocessing import Process, Queue, Pool
import time
import json
import os


def share_best_lives(best_lives, generation_no):
    shared_file_name = f"shared_best_lives_generation_{generation_no}.json"

    # Write best lives to a JSON file
    with open(shared_file_name, "w") as file:
        json.dump(best_lives, file)


def accumulate_shared_best_lives(generations):
    shared_best_lives = []

    for generation_no in range(0, generations, 10):
        shared_file_name = f"shared_best_lives_generation_{generation_no}.json"

        if os.path.exists(shared_file_name):
            # Read best lives from the JSON file
            with open(shared_file_name, "r") as file:
                best_lives = json.load(file)
                shared_best_lives.extend(best_lives)


def run_ga_in_parallel(num_processes):
    pool = Pool(processes=num_processes)

    for _ in range(num_processes):
        process = pool.apply_async(
            main(),
        )

    pool.close()
    pool.join()


def main():
    for generation in range(100):


if __name__ == "__main__":
    run_ga_in_parallel(4)