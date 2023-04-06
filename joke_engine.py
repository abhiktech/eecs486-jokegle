from preprocess import preprocess

class JokeEngineDriver:

    def __init__(self):
        self.inverted_index = self.load_data_into_inverted_index()

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

    def load_data_into_inverted_index(self):
        inverted_index = None
        return inverted_index
    
    def get_initial_top_jokes(self, query_tokens):
        initial_top_jokes = None
        query_weight = None
        return initial_top_jokes, query_weight

    def get_user_feedback(self, initial_top_jokes):
        query_joke_relevances = None
        return query_joke_relevances

    def get_updated_top_jokes(self, initial_top_jokes, query_weights, query_joke_relevances):
        updated_top_jokes = None
        return updated_top_jokes

    def display_updated_top_jokes(self, updated_top_jokes):
        return


def main():
    joke_engine = JokeEngineDriver()
    joke_engine.run()

if __name__ == "__main__":
    main()