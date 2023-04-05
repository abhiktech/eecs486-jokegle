# EECS 486 Final Project - create_inverted_index.py

import json

def read_dataset():
    """Imports the datasets from the GitHub repository."""
    dataset = []
    for fname in ["stupidstuff.json", "wocka.json", "reddit_jokes.json"]:
        with open(fname, "r") as file:
            curr_file = json.loads(file.read())
            dataset += curr_file

    return dataset

def preprocess(dataset):
    pass

def run():
    import_dataset = read_dataset()
    print(import_dataset[5])
    preprocessed = preprocess(import_dataset)

run()