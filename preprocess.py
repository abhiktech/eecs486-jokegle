from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re

def preprocess(text):

    text = text.lower()
    text = removeQuotations(text)
    text = word_tokenize(text)
    text = removeStopWords(text)
    text = stemWords(text)

    # Remove any remaining individual punctutation
    text = [token for token in text if not token in string.punctuation]

    return text
    
def removeQuotations(text):
    text = text.replace('"', '').replace('\'', '').replace('`', '')
    return text
    

def removeStopWords(text):
    stop_words = set(stopwords.words('english'))
    text = [w for w in text if not w in stop_words]
    return text

def stemWords(text):
    stemmer = PorterStemmer()

    text = [stemmer.stem(w) for w in text]
    return text


if __name__ == '__main__':
    x = preprocess("A blackjack's dealer and a player with a thirteen count in his hand\nwere arguing about whether or not it was appropriate to tip the\ndealer.\n\nThe player said, \"When I get bad cards, it's not the dealer's fault.\nAccordingly, when I get good cards, the dealer obviously had nothing\nto do with it so, why should I tip him?\"\n\nThe dealer said, \"When you eat out do you tip the waiter?\"\n\n\"Yes.\"\n\n\"Well then, he serves you food, I'm serving you cards, so you should\ntip me.\"\n\n\"Okay, but, the waiter gives me what I ask for. I'll take an eight.\"")
    print(x)

    #removeEscapes("fs")
    
