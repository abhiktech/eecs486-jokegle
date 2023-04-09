# EECS 486 Final Project - create_inverted_index.py

import json
from preprocess import preprocess
import math

class InvertedIndex:

    def __init__(self):
        self.jokes_data = []
        self.terms_index = {}
        self.terms_idfs = {}

    def read_dataset(self):
        """Imports the datasets from the GitHub repository."""
        dataset = []
        for fname in ["jokes/stupidstuff.json", "jokes/wocka.json"]:
            with open(fname, "r") as file:
                curr_file = json.loads(file.read())
                dataset += curr_file

        return dataset


    def read_joke_data(self, old_dataset):
        current_joke_id = 0
        
        for joke in old_dataset:
            joke_value = {}
            
            joke_value["joke_id"] = current_joke_id
    
            if "rating" not in joke:
                joke_value["funniness_score"] = 3
            else:
                joke_value["funniness_score"] = joke["rating"]

            joke_value["weights"] = {} # empty for now
            joke_value["funniness_updates"] = 1
            joke_value["text"] = joke['body']
            joke_value["preprocessed_tokens"] = preprocess(joke_value["text"])

            self.calculate_joke_term_frequency(joke_value["preprocessed_tokens"], current_joke_id)
            
            current_joke_id += 1
            self.jokes_data.append(joke_value)

    def calculate_joke_term_frequency(self, joke_tokens, joke_id):

        for token in joke_tokens:
            if token not in self.terms_index:
                # Term is seen in collection for the first time
                self.terms_index[token] = {joke_id: 1}
            else:
                if joke_id not in self.terms_index[token]:
                    # Term is seen in document for the first time
                    self.terms_index[token][joke_id] = 1
                else:
                    # Term has been seen in document before
                    self.terms_index[token][joke_id] += 1

    def compute_term_weights(self):
        N = len(self.jokes_data)

        for i in range(N):
            joke = self.jokes_data[i]
            joke_id = joke["joke_id"]

            term_weights = {}

            for token in joke["preprocessed_tokens"]:
                tf = self.terms_index[token][joke_id]
                n = len(self.terms_index[token]) + 1 # Add one smoothing
                idf = math.log(N/n, 2)
                self.terms_idfs[token] = idf
                term_weight = tf * idf
                term_weights[token] = term_weight
            
            # Cosine normalization of joke vector
            length = math.sqrt(sum([value**2 for value in term_weights.values()]))
            for word in term_weights.keys():
                if length != 0:
                    term_weights[word] /= length
            
            self.jokes_data[i]["weights"] = term_weights

    def write_to_json(self):
        with open("joke_data.json", "w") as outfile:
            json.dump(self.jokes_data, outfile)
        with open("term_idfs.json", "w") as outfile:
            json.dump(self.terms_idfs, outfile)

    def run(self):
        import_dataset = self.read_dataset()
        self.read_joke_data(import_dataset)
        self.compute_term_weights()
        self.write_to_json()

if __name__ == '__main__':
    index = InvertedIndex()
    index.run()

'''
Structure of in-memory inverted index

terms index
{
   "abhik": {
        doc_id1: freq,
        doc_id2: freq
   },
}

num_documents

documents index (not needed due to document weighting scheme)
{
    doc_id1: max_term_freq,
    doc_id2: max_term_freq
}

Steps to compute document term weights -
1. In first pass for each document, do the following
    a) Compute term freq
    b) Store max term freq (not needed)
2. In a pass through the index, compute normalized term freqs (not needed)
3. In a pass through the new_dataset (what we are dumping into the json), compute the term weights using available tf and idf
4. In another pass, perform cosine normalization

'''