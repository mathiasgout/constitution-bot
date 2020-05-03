import pandas as pd
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from data_preparation import data_preparation

ARTICLES_PATH = "articles.csv"
TOKENIZER_PATH = "tokenizer.json"
MODEL_PATH = "models/model_gru_dropout.hdf5"


""" Importation et preprocessing """
articles = pd.read_csv(ARTICLES_PATH)

# Transformation d'un df à 1 colonne en une série
articles = articles.articles

# Preprocessing des articles
articles = data_preparation(articles)


""" Tokenizer """
tokenizer = Tokenizer(lower=True, filters=',;:!"#$%&()*+/<=>?@[\\]^_`{|}~\t\n')
tokenizer.fit_on_texts(articles)

# On enregistre l'object Tokenizer
tokenizer_json = tokenizer.to_json()
with open(TOKENIZER_PATH, 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer_json, ensure_ascii=False))

# Les articles tokenizés
sequences = tokenizer.texts_to_sequences(articles)

# L'index des mots, son reverse et la taille du vocabulaire
word_index = tokenizer.word_index
vocab_size = len(word_index)


""" Creation de X et y """
# Création d'un grand vecteur avec tout les mots
text = [item for sublist in sequences for item in sublist]

# Création de X et y par fenêtre coulissante
def sliding_window(text, sentence_len):
    seq = []
    for i in range(len(text)-sentence_len):
        seq.append(text[i:(i+sentence_len)])

    X = []
    y = []
    for window in seq:
        X.append(window[:(sentence_len-1)])
        y.append(window[-1])
    
    return X, y

# On va entrainer le modèle sur les 29 premiers mots pour prédire le 30ème
X, y = sliding_window(text, 30)
X = np.array(X)
y = keras.utils.to_categorical(y, vocab_size+1)


""" Creation du modèle """
def build_model():
    model = keras.Sequential()
    model.add(keras.layers.Embedding(input_dim=vocab_size+1, output_dim=50, input_length=len(X[0])))
    model.add(keras.layers.GRU(units=100, return_sequences=True))
    model.add(keras.layers.GRU(100))
    model.add(keras.layers.Dense(100, activation="relu"))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(vocab_size+1, activation="softmax"))
    
    model.summary()
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    
    return model


""" Entrainement """
model = build_model()
checkpoint = keras.callbacks.ModelCheckpoint(MODEL_PATH, monitor='loss', verbose=1, save_best_only=True, mode='min')
model.fit(X, y, epochs=500, batch_size=128, use_multiprocessing=True, callbacks=[checkpoint])


