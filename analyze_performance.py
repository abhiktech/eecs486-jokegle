# Algorithm
# - Extract jokes
# - Build queries
# - For each query, figure out which jokes are relevant and not-relevant
# - For each query, at different rank cutoffs, calculate precision and recall (round recall to certain number of decimal points)
# - Average the precision at each recall point
# - Plot the graph, potentially compute area

import json
from preprocess import preprocess
from joke_engine import JokeEngineDriver
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

class JokeEnginePerformanceAnalyzer:

    def __init__(self):
        self.inverted_index = self.get_jokes()
        self.queries = ["dog", "college", "computers", "animals", "football", "sports", "family", "country", "phone", "ball", "flag", "funny", "sad", "tired", "school", "anime", "cow", "study", "dance", "music", "wheels", "bus", "elephant", "girl", "boy", "i'm tired of studying", "peanuts are tasty", "airplanes are scary", "i hate exams", "beans are gassy", "my daughter is sassy", "bollywood movies", "the quick brown fox jumped over the lazy dog"]
        self.relevances = []
        self.joke_engine = JokeEngineDriver()
        self.precision_recall_points = []

    def run(self):
        self.compute_query_and_joke_relevances()
        self.compute_precision_and_recall_points()
        # self.plot_precision_recall_curve()

    def get_jokes(self):
        with open("joke_data.json", "r") as ii_file:
            inverted_index = json.load(ii_file)
        return inverted_index

    def compute_query_and_joke_relevances(self):
        for query in self.queries:
            query_tokens = preprocess(query)
            query_weights = self.joke_engine.get_query_weights(query_tokens)
            jokes, max_similarity_score = self.joke_engine.compute_similarity_scores(query_weights, self.inverted_index[:])
            
            query_relevances = {}
            num_relevant = 0

            for joke in jokes:
                similarity_funniness_weighted_average = self.joke_engine.get_similarity_and_funniness_weighted_average(joke["similarity_score"], joke["funniness_score"], max_similarity_score)
                if similarity_funniness_weighted_average >= 0.5:
                    query_relevances[joke["joke_id"]] = True
                    num_relevant += 1
                else:
                    query_relevances[joke["joke_id"]] = False

            query_relevances["num_relevant"] = num_relevant
            # print(query + " " + str(num_relevant))

            self.relevances.append(query_relevances)
        
    def compute_precision_and_recall_points(self):
        query_index = 0
        
        precision_recall_points = []

        for query in self.queries:
            query_tokens = preprocess(query)
            
            rank_cutoffs = [50, 100, 150, 200, 250]
            # rank_cutoffs = [5]

            for rank_cutoff in rank_cutoffs:
                top_jokes = self.joke_engine.get_initial_top_jokes(query_tokens, rank_cutoff)[0]
                
                num_relevant = 0
                for joke in top_jokes:
                    if self.relevances[query_index][joke["joke_id"]]:
                        num_relevant += 1
                precision_recall_points.append((round(num_relevant / self.relevances[query_index]["num_relevant"], 4), num_relevant / rank_cutoff))

            query_index += 1

        precision_recall_dict = {}

        for recall, precision in precision_recall_points:
            # print(str(recall) + " " + str(precision))
            if recall not in precision_recall_dict:
                precision_recall_dict[recall] = []
            precision_recall_dict[recall].append(precision)

        for recall, precisions in precision_recall_dict.items():
            self.precision_recall_points.append((recall, sum(precisions) / len(precisions)))

    def plot_precision_recall_curve(self):
        # Unpack xy tuples into separate x and y lists
        x_list, y_list = zip(*self.precision_recall_points)

        # Plot the xy data using Matplotlib
        plt.plot(x_list, y_list, 'ro')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Average Recall/Precision Curve')
        plt.savefig('plot.png')


def main():
    performance_analyzer = JokeEnginePerformanceAnalyzer()
    performance_analyzer.run()

if __name__ == "__main__":
    main()
