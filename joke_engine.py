


class JokeEngineDriver:

    def __init__(self):
        self.inverted_index = None # TODO: Change

    def run(self):
        print("Welcome to Jokegle, a search engine where you can look for jokes!")

        is_running = True

        while is_running:
            query = input("Search for a jokes using keywords: ")

            is_running = input("Search for more jokes? yes or no: ") != "no"

    def get_top_jokes(self):
        return

    def get_user_feedback(self):
        return

    def get_updated_jokes(self):
        return


def main():
    joke_engine = JokeEngineDriver()
    joke_engine.run()

if __name__ == "__main__":
    main()