import json
import numpy as np
import tensorflow as tf
from keras.layers import Input, Embedding, Conv1D, MaxPooling1D, Flatten, Dense
from keras.models import Model
from keras.callbacks import EarlyStopping
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


def train(vocab_size, x_train, x_val, x_test, y_train, y_val, y_test):
    # Define the input shape
    input_shape = (100,)  # This assumes that the input sequence is 100 tokens long

    # Define the input layer
    inputs = Input(shape=input_shape)

    # Define the embedding layer
    embedding_size = 50  # You can experiment with different embedding sizes
    embedding = Embedding(input_dim=vocab_size, output_dim=embedding_size)(inputs)

    # Define the convolutional layers
    filters = 128  # You can experiment with different filter sizes
    kernel_size = 5  # You can experiment with different kernel sizes
    conv1 = Conv1D(filters=filters, kernel_size=kernel_size, activation='relu')(embedding)
    pool1 = MaxPooling1D(pool_size=2)(conv1)

    # Flatten the output
    flatten = Flatten()(pool1)

    # Define the output layer
    output = Dense(1)(flatten)

    # Define the model
    model = Model(inputs=inputs, outputs=output)

    # Compile the model
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # Train the model
    early_stopping = EarlyStopping(monitor='val_loss', patience=3)
    model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=10, callbacks=[early_stopping])

    # Evaluate the model
    print("Evaluating on test data")
    results = model.evaluate(x_test, y_test)
    print("test loss, test acc: ", results)

    return model

def predict(model, tokenizer):
    jokes = []
    with open('jokes/wocka.json', 'r') as file:
        cur_file = json.loads(file.read())
        for data in cur_file:
            jokes.append(data['body'])
    
        jokes_seq = tokenizer.texts_to_sequences(jokes)
        jokes_seq_padded = pad_sequences(jokes_seq, maxlen=100, padding='post', truncating='post')
        predicted_ratings = model.predict(jokes_seq_padded)

        for i in range(len(cur_file)):
            data = cur_file[i]
            data['rating'] = float(predicted_ratings[i][0])
        
        new_json = json.dumps(cur_file)
        with open("jokes/wocka_ratings.json", 'w+') as outfile:
            outfile.write(new_json)

if __name__ == "__main__":
    jokes = []
    ratings = []
    with open('jokes/stupidstuff.json', 'r') as file:
        cur_file = json.loads(file.read())
        for data in cur_file:
            jokes.append(data['body'])
            ratings.append(data['rating'])

    data_size = len(jokes)
    train_size = int(data_size * 0.6)
    val_size = int(data_size * 0.2)

    jokes_train = jokes[:train_size]
    jokes_val = jokes[train_size:train_size + val_size]
    jokes_test = jokes[train_size + val_size:]

    y_train = np.asarray(ratings[:train_size])
    y_val = np.asarray(ratings[train_size:train_size + val_size])
    y_test = np.asarray(ratings[train_size + val_size:])

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(jokes)
    vocab_size = len(tokenizer.word_index) + 1

    jokes_train_seq = tokenizer.texts_to_sequences(jokes_train)
    x_train = pad_sequences(jokes_train_seq, maxlen=100, padding='post', truncating='post')
    jokes_val_seq = tokenizer.texts_to_sequences(jokes_val)
    x_val = pad_sequences(jokes_val_seq, maxlen=100, padding='post', truncating='post')
    jokes_test_seq = tokenizer.texts_to_sequences(jokes_test)
    x_test = pad_sequences(jokes_test_seq, maxlen=100, padding='post', truncating='post')

    model = train(vocab_size, x_train, x_val, x_test, y_train, y_val, y_test)

    predict(model, tokenizer)