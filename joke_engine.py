from preprocess import preprocess
import json
import math
import os

class JokeEngineDriver:

    def __init__(self):
        self.inverted_index, self.term_idfs, self.bad_words = self.load_data()
        self.is_bad_word_filter_on = False

    def run(self):
        print("Welcome to Jokegle, a search engine where you can look for jokes!")
        print()
        
        bad_word_filter_user_choice = input("Turn profanity filter on? yes or no: ")
        while bad_word_filter_user_choice not in ("yes", "no"):
            bad_word_filter_user_choice = input("Please enter 'yes' or 'no': ")

        self.is_bad_word_filter_on = bad_word_filter_user_choice == 'yes'
        
        is_running = True

        while is_running:
            query = input("Search for jokes using keywords: ")
            print()
            query_tokens = preprocess(query)


            initial_top_jokes, query_weight = self.get_initial_top_jokes(query_tokens, 5)

            print()
            print("Here are your initial top jokes")
            print()

            query_joke_relevances = self.get_user_feedback(initial_top_jokes)

            updated_top_jokes = self.get_updated_top_jokes(query_joke_relevances, query_weight)

            print()
            print("Here are your updated top jokes")
            print()
            self.display_updated_top_jokes(updated_top_jokes)

            is_running = input("Search for more jokes? yes or no: ") != "no"
            print()

        self.update_joke_data_json()

    def load_data(self):
        inverted_index = term_idfs = None
        with open("joke_data.json", "r") as ii_file:
            inverted_index = json.load(ii_file)
        
        with open("term_idfs.json", "r") as ti_file:
            term_idfs = json.load(ti_file)

        bad_words = open("bad_words.txt", "r").readlines()
        bad_words_preprocessed = []
        
        for bad_word in bad_words:
            bad_word = bad_word.strip()
            if ' ' not in bad_word:
                result = preprocess(bad_word)
                if len(result) == 1:
                    bad_words_preprocessed.append(result[0])
        
        return inverted_index, term_idfs, bad_words_preprocessed
    
    def get_similarity_and_funniness_weighted_average(self, similarity_score, funniness_score, max_similarity_score):
        # TODO: Make this much better
        similarity_score_weight = 0.8
        funniness_score_weight = 1 - similarity_score_weight
        return similarity_score_weight * similarity_score / max_similarity_score + funniness_score_weight * (funniness_score - 1) / 4

    def compute_similarity_scores(self, query_weights, jokes):
        max_similarity_score = 0
        for i, joke in enumerate(jokes):
            similarity_score = 0

            for term, weight in query_weights.items():
                if term in joke["weights"]:
                    similarity_score += joke["weights"][term] * weight

            jokes[i]["similarity_score"] = similarity_score
            if similarity_score > max_similarity_score:
                max_similarity_score = similarity_score

        return jokes, max_similarity_score

    def get_sorted_jokes(self, query_weights):
        jokes = self.inverted_index[:]
        jokes, max_similarity_score = self.compute_similarity_scores(query_weights, jokes)
        jokes = sorted(jokes, reverse=True, key=lambda v: self.get_similarity_and_funniness_weighted_average(v["similarity_score"], v["funniness_score"], max_similarity_score))
        return jokes

    def get_query_weights(self, query_tokens):
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

        return query_weights

    def get_initial_top_jokes(self, query_tokens, num_jokes):
        initial_top_jokes = None
        query_weights = self.get_query_weights(query_tokens)
        sorted_jokes = self.get_sorted_jokes(query_weights)
        initial_top_jokes = []

        if self.is_bad_word_filter_on:
            for joke in sorted_jokes:
                bad_word_exists = False
                for bad_word in self.bad_words:
                    if bad_word in joke['preprocessed_tokens']:
                        bad_word_exists = True
                        break
                if not bad_word_exists:
                    initial_top_jokes.append(joke)
                if len(initial_top_jokes) == num_jokes:
                    break
        else:
            initial_top_jokes = sorted_jokes[:num_jokes]

        return initial_top_jokes, query_weights

    def get_user_feedback(self, initial_top_jokes):
        for i, joke in enumerate(initial_top_jokes):
            print(joke['text'])
            
            relevance_score = input("Is this a good joke? yes or no: ")
            while relevance_score not in ("yes", "no"):
                relevance_score = input("Please enter 'yes' or 'no': ")

            try:
                funniness_score = int(input("How funny was this joke? Rate on a scale of 1 to 5: "))
            except ValueError:
                funniness_score = 0
            while funniness_score > 5 or funniness_score < 1:
                try:
                    funniness_score = int(input("Please enter a rating between 1 to 5: "))
                except ValueError:
                    pass

            old_funniness_score = self.inverted_index[joke["joke_id"]]["funniness_score"]
            funniness_updates = self.inverted_index[joke["joke_id"]]["funniness_updates"]

            self.inverted_index[joke["joke_id"]]["funniness_score"] = (old_funniness_score * funniness_updates + funniness_score) / (funniness_updates + 1)
            self.inverted_index[joke["joke_id"]]["funniness_updates"] += 1

            initial_top_jokes[i]["is_relevant"] = relevance_score == 'yes'
            
            print()
        
        return initial_top_jokes

    def get_updated_top_jokes(self, initial_top_jokes, original_query_weights):
        # initial_top_jokes is a list of joke objects which each contain whether the joke
        # was marked relevant or irrelevant by the user, the joke's id, and the joke's term weights
        # query_weights is a dictionary of the query's term weights

        alpha = 1
        beta = 1
        gamma = 1

        new_query_weights = original_query_weights.copy()
        for term, weight in new_query_weights.items():
            new_query_weights[term] = alpha * weight

        seen_ids = set()
        for joke in initial_top_jokes:
            seen_ids.add(joke["joke_id"])
            if joke["is_relevant"]:
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
                        new_query_weights[key] = -gamma * value
        
        # Make sure all weights are non-negative
        for key, value in new_query_weights.items():
             new_query_weights[key] = max(0, value)

        # Use new query to get new top jokes
        updated_top_jokes = []
        jokes_by_sim_scores = self.get_sorted_jokes(new_query_weights)

        combined_jokes = updated_top_jokes + initial_top_jokes

        # Only return jokes that haven't been seen before
        for joke in jokes_by_sim_scores:
            is_duplicate = False
            for updated_joke in combined_jokes:
                jokes_list = set(joke['weights'].keys())
                updated_jokes_list = set(updated_joke['weights'].keys())
                intersection = len(list(jokes_list.intersection(updated_jokes_list)))
                union = (len(joke['weights'].keys()) + len(updated_joke['weights'].keys())) - intersection
                jaccard_sim = float(intersection) / union
                if jaccard_sim > 0.5:
                    is_duplicate = True

            if joke["joke_id"] not in seen_ids and not is_duplicate:
                if self.is_bad_word_filter_on:
                    bad_word_exists = False
                    for bad_word in self.bad_words:
                        if bad_word in joke["preprocessed_tokens"]:
                            bad_word_exists = True
                            break
                    if not bad_word_exists:
                        updated_top_jokes.append(joke)
                else:
                    updated_top_jokes.append(joke)

            if len(updated_top_jokes) == 10:
                break

        return updated_top_jokes

    def display_updated_top_jokes(self, updated_top_jokes):
        for i in range(len(updated_top_jokes)):
            joke = updated_top_jokes[i]
            print(str(i+1) + ". " + joke["text"])
            print("\n")
        return
    
    def update_joke_data_json(self):
        # os.remove('joke_data.json')
        # with open("joke_data.json", "w") as outfile:
        #     json.dump(self.inverted_index, outfile)
        pass
    
def main():
    joke_engine = JokeEngineDriver()
    joke_engine.run()

if __name__ == "__main__":
    main()