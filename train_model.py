import os
import datetime
import pandas as pd
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from data_preparation import data_preparation
from build_model import build_model

""" Check for 'models' folder """
# Check if "models" folder exist
DIR_MODEL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "models")
if os.path.exists(DIR_MODEL_PATH) is False:
    os.mkdir(DIR_MODEL_PATH)

# Create model file name based on the current time
now = datetime.datetime.now().strftime("%Y%m%d%H%M")
MODEL_PATH = DIR_MODEL_PATH + "/model_" + now + ".hdf5"


""" Imports and data preparation """
DIR_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_tokenizer")
ARTICLES_PATH = os.path.join(DIR_DATA_PATH, "articles.csv")
articles = pd.read_csv(ARTICLES_PATH)

# Transformation d'un df à 1 colonne en une série
articles = articles.articles

# Preprocessing des articles
articles = data_preparation(articles)


""" Tokenizer """
TOKENIZER_PATH = os.path.join(DIR_DATA_PATH, "tokenizer.json")
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


""" X and y creation """
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


""" Training """
model = build_model(vocab_size=vocab_size, input_length=len(X[0]))
checkpoint = keras.callbacks.ModelCheckpoint(MODEL_PATH, monitor='loss', verbose=1, save_best_only=True, mode='min')
model.fit(X, y, epochs=500, batch_size=128, use_multiprocessing=True, callbacks=[checkpoint])

print("Your model file : {}".format(MODEL_PATH))
