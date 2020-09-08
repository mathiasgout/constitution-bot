from tensorflow import keras

def build_model(vocab_size, input_length):
    """ Build our RNN model """

    model = keras.Sequential()
    model.add(keras.layers.Embedding(input_dim=vocab_size+1, output_dim=50, input_length=input_length))
    model.add(keras.layers.GRU(units=100, return_sequences=True))
    model.add(keras.layers.GRU(100))
    model.add(keras.layers.Dense(100, activation="relu"))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(vocab_size+1, activation="softmax"))

    model.summary()
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    return model