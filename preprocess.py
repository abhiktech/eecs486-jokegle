from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

def preprocess(text):

    text = text.lower()
    text = word_tokenize(text)
    text = removeStopWords(text)
    text = stemWords(text)

    text = [token for token in text if not token in string.punctuation]

    return text
    



def removeStopWords(text):
    stop_words = set(stopwords.words('english'))
    text = [w for w in text if not w in stop_words]
    return text

def stemWords(text):
    stemmer = PorterStemmer()

    text = [stemmer.stem(w) for w in text]
    return text

def removeEscapes(text):
    # Sample string with escape characters
    #my_string = "This is a string with escape characters: \n\t and \""
    #print(my_string)
    # Encode the string using 'unicode_escape' encoding
    #my_encoded_string = my_string.encode('unicode_escape')

    # Decode the encoded string using 'utf-8' encoding
    #my_decoded_string = my_encoded_string.decode('utf-8')

    # Print the decoded string without escape characters
    #print(my_decoded_string)
    pass



if __name__ == '__main__':
    x = preprocess("A blackjack's dealer and a player with a thirteen count in his hand\nwere arguing about whether or not it was appropriate to tip the\ndealer.\n\nThe player said, \"When I get bad cards, it's not the dealer's fault.\nAccordingly, when I get good cards, the dealer obviously had nothing\nto do with it so, why should I tip him?\"\n\nThe dealer said, \"When you eat out do you tip the waiter?\"\n\n\"Yes.\"\n\n\"Well then, he serves you food, I'm serving you cards, so you should\ntip me.\"\n\n\"Okay, but, the waiter gives me what I ask for. I'll take an eight.\"")
    print(x)

    #removeEscapes("fs")
    
