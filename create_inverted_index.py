# EECS 486 Final Project - create_inverted_index.py

import json

def read_dataset():
    """Imports the datasets from the GitHub repository."""
    dataset = []
    for fname in ["jokes/stupidstuff.json", "jokes/wocka.json"]:
        with open(fname, "r") as file:
            curr_file = json.loads(file.read())
            dataset += curr_file

    return dataset

def preprocess(dataset):
    pass

def file_structure(old_dataset):
    new_dataset = []
    current_joke_id = 0
    for joke in old_dataset:
        value = {}
        
        value["joke_id"] = current_joke_id
        current_joke_id += 1

        if "rating" not in joke:
            value["funniness"] = 3
        else:
            value["funniness"] = joke["rating"]

        value["weights"] = {} # empty for now
        value["funniness_updates"] = 1
        value["text"] = joke['body']
        new_dataset.append(value)

    return new_dataset

def run():
    import_dataset = read_dataset()
    # preprocessed = preprocess(import_dataset)
    new_data = file_structure(import_dataset)

    with open("joke_data.json", "w") as outfile:
        json.dump(new_data, outfile)

print("Indexing jokes...")
run()