from preprocess import preprocess
import json
import math

class JokeEngineDriver:

    def __init__(self):
        self.inverted_index, self.term_idfs = self.load_data()

    def run(self):
        print("Welcome to Jokegle, a search engine where you can look for jokes!")

        is_running = True

        while is_running:
            query = input("Search for a jokes using keywords: ")
            query_tokens = preprocess(query)

            initial_top_jokes, query_weight = self.get_initial_top_jokes(query_tokens)

            query_joke_relevances = self.get_user_feedback(initial_top_jokes)

            updated_top_jokes = self.get_updated_top_jokes(initial_top_jokes, query_weight, query_joke_relevances)

            self.display_updated_top_jokes(updated_top_jokes)

            is_running = input("Search for more jokes? yes or no: ") != "no"

    def load_data(self):
        inverted_index = term_idfs = None
        with open("joke_data.json", "r") as ii_file:
            inverted_index = json.load(ii_file)
        
        with open("term_idfs.json", "r") as ti_file:
            term_idfs = json.load(ti_file)
        
        return inverted_index, term_idfs
    
    def get_similarity_and_funniness_weighted_average(self, similarity_score, funniness_score):
        return similarity_score * 2 + funniness_score

    def get_sorted_jokes(self, query_weights):
        jokes = self.inverted_index[:]

        for i, joke in enumerate(jokes):
            similarity_score = 0

            for term, weight in query_weights.items():
                if term in joke["weights"]:
                    similarity_score += joke["weights"][term] * weight

            jokes[i]["similarity_score"] = similarity_score

        jokes = sorted(jokes, reverse=True, key=lambda v: self.get_similarity_and_funniness_weighted_average(v["similarity_score"], v["funniness_score"]))
        
        return jokes

    def get_initial_top_jokes(self, query_tokens):
        initial_top_jokes = None
        query_weights = {}
        
        # Compute max tf
        max_tf = 1
        tfs = {}
        for token in query_tokens:
            tfs[token] = tfs.get(token, 0) + 1
            max_tf = max(max_tf, tfs[token])

        N = len(self.inverted_index)

        # Compute query term weights
        for token in query_tokens:
            if token in self.term_idfs:
                idf = self.term_idfs[token]
            else:
                idf = math.log(N, 2)
            query_weights[token] = (0.5 + (0.5 * tfs[token]) / max_tf) * idf

        initial_top_jokes = self.get_sorted_jokes(query_weights)[:10]

        return initial_top_jokes, query_weights

    def get_user_feedback(self, initial_top_jokes):
        query_joke_relevances = None
        return query_joke_relevances

    def get_updated_top_jokes(self, initial_top_jokes, original_query_weights):
        # initial_top_jokes is a list of joke objects which each contain whether the joke
        # was marked relevant or irrelevant by the user, the joke's id, and the joke's term weights
        # query_weights is a dictionary of the query's term weights

        updated_top_jokes = None

        alpha = 1
        beta = 1
        gamma = 1

        new_query_weights = original_query_weights.copy()
        for term, weight in new_query_weights.items():
            new_query_weights[term] = alpha * weight


        seen_ids = set()
        for joke in initial_top_jokes:
            seen_ids.add(joke["joke_id"])
            if joke["relevant"]:
                for key, value in joke["weights"].items():
                    if key in new_query_weights:
                        new_query_weights[key] += beta * value
                    else:
                        new_query_weights[key] = beta * value
            else:
                for key, value in joke["weights"].items():
                    if key in new_query_weights:
                        new_query_weights[key] -= gamma * value
                    else:
                        new_query_weights[key] = gamma * value
        

        for key, value in new_query_weights.items():
             new_query_weights[key] = max(0, value)


        # Use new query to get new top jokes
        updated_top_jokes = None




    
        return updated_top_jokes

    def display_updated_top_jokes(self, updated_top_jokes):
        return


def main():
    joke_engine = JokeEngineDriver()
    joke_engine.run()

if __name__ == "__main__":
    main()