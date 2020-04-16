from tensorflow import keras
from random import randint
import time
import twitter_credentials
import pandas as pd
import json
from tweepy import OAuthHandler
from tweepy import API


class ArticlePoster:
    TOKENIZER_PATH = "C:/Users/mathi/Documents/amusement/python/constitution/tokenizer.json"
    MODEL_PATH = "C:/Users/mathi/Documents/amusement/python/constitution/models/model_gru_dropout.hdf5"
    ARTICLES_PATH = "C:/Users/mathi/Documents/amusement/python/constitution/articles.csv"
    ACCES_TOKEN = twitter_credentials.ACCES_TOKEN
    ACCES_TOKEN_SECRET = twitter_credentials.ACCES_TOKEN_SECRET
    CONSUMER_KEY = twitter_credentials.CONSUMER_KEY
    CONSUMER_SECRET = twitter_credentials.CONSUMER_SECRET
    
    
    def __init__(self):
        
        self.articles = pd.read_csv(self.ARTICLES_PATH)
        self.articles = self.articles.articles
        
        # Chargement de l'objet Tokenizer
        with open(self.TOKENIZER_PATH) as f:
                data = json.load(f)
                self.tokenizer = keras.preprocessing.text.tokenizer_from_json(data)
        
        self.reversed_word_index = self.tokenizer.index_word        
        
        # Création du début des phrases
        sequences = self.tokenizer.texts_to_sequences(self.articles)            
        self.start_sentences = [sequence[0:k] for sequence in sequences for k in [2,3,4,5,6]]
        
        # Chargement du modèle
        self.model = keras.models.load_model(self.MODEL_PATH)
        
        # Authentification twitter
        self.auth = OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.auth.set_access_token(self.ACCES_TOKEN, self.ACCES_TOKEN_SECRET)

        
    def generate_article(self, number_stops):
        """ Fonction pour générer un article avec un nombre de phrase choisit """
        
        stop = 0
        tokenized_seq = [self.start_sentences[randint(0, len(self.start_sentences)-1)]]
        while stop < number_stops:
            padded_sequence = keras.preprocessing.sequence.pad_sequences(tokenized_seq, maxlen=29, padding="pre", truncating="pre")
            predicted_proba = self.model.predict(padded_sequence)
            tokenized_seq[0].append(predicted_proba.argmax())
            
            # 3 est le token pour "."
            if tokenized_seq[0][-1] == 3:
                stop = stop + 1
        
        listed_article = [self.reversed_word_index[token] for token in tokenized_seq[0]]
        article = " ".join(listed_article)
        
        return article
    
    
    def article_shaping(self):
        """ Fonction pour mettre en forme l'article généré """
        
        # On génère un article qui a entre 3 et 5 phrases
        article = self.generate_article(randint(3,5))
        
        article = article[0].upper() + article[1:len(article)]
        for i in range(len(article)-3):
            if article[i] == ".":
                article = article[0:i+2] + article[i+2].upper() + article[i+3:len(article)]
        
        article = article.replace(" .", ".")
        article = article.replace("président", "Président")
        article = article.replace("république", "République")
        article = article.replace("gouvernement", "Gouvernement")
        article = article.replace("france", "France")
        article = article.replace("parlement", "Parlement")
        article = article.replace("constitution", "Constitution")
        article = article.replace("charte", "Charte")
        article = article.replace("droits de l'homme", "Droits de l'Homme")
        article = article.replace("la marseillaise", '"La Marseillaise"')
        article = article.replace("liberté egalité fraternité", '"Liberté Egalité Fraternité"')
        
        return article        
        
    
    @staticmethod
    def text_to_list(text):
        """ Une fonction qui transforme un texte composé de mots en une liste de mots """
        
        word = ""
        list_words = []
        for i in range(len(text)):
            if text[i] != " ":
                word = word + text[i]
            else:
                list_words.append(word)
                word = ""
        list_words.append(word)
        
        return list_words
    
    
    @staticmethod
    def place_comma(idx, list_words, article):
        """ Une fonction qui place la virgule au bon endroit """
        
        article_tmp = article
        word = list_words[idx]
        word_len = len(word)
        
        nb_dup = 0
        for i in range(len(list_words[:idx])):
            if word in list_words[i]:
                nb_dup = nb_dup + 1
            
        for _ in range(nb_dup):
            word_idx = article_tmp.find(word)
            article_tmp = article_tmp[:word_idx] + "z"*word_len + article_tmp[word_idx+word_len:]
    
        real_word_idx = article_tmp.find(word)
        article = article[:real_word_idx+word_len] + "," + article[real_word_idx+word_len:]
            
        return article
    
    
    def fix_article(self):
        """ Une fonction qui place les virgules dans un article """
        
        article = self.article_shaping()
        
        # Création d'un dictionnaire des mots de l'article
        list_words = self.text_to_list(article)
        article_idx = {k:list_words[k] for k in range(len(list_words))}
        
        while True:
            print("\n")
            print("article = " + article)
            print("\n")
            print(article_idx)
            while True:
                try:
                    word_idx = int(input("\nAprès quel mot voulez vous placer une virgule ? (donnez l'index du mot et -1 si vous ne voulez pas) : "))
                    print("\n")
                    if word_idx < len(list_words) and word_idx >= -1:
                        break
                    print("Donnez un index cohérent.")
                except ValueError:
                    print("Donnez l'index d'un mot ou -1.")
            
            if word_idx == -1:
                return article
            else:
                 article = self.place_comma(word_idx, list_words, article)
                 

    def text_to_tweet(self):
        """ Une fonction qui met en forme le tweet ou la liste de tweet si len(article) > 280 """
        
        text = self.fix_article()
        while True:
            try:
                num_article = int(input("Article numéro ? : "))
                if num_article < 100 and num_article > 0:
                    break
            except ValueError:
                print("Donnez un nombre entre 1 et 100.")
        
        text = "ARTICLE {}.\n\n".format(num_article) + text
        remain_len = len(text)
        
        if remain_len < 280:
            return [text]
        
        text_list = []
        while remain_len >= 274:
            idx = 274
            while text[idx] not in ",.":
                idx = idx - 1
                if idx < 150 and text[idx] == " ":
                    break
            extract_text = text[:idx+1] + " (" + str(len(text_list)+1) + "/zzz)"
            text_list.append(extract_text)
            text = text[idx+1:]
            remain_len = len(text)
        
        text_list.append(text + " (" + str(len(text_list)+1) + "/zzz)")
        
        for i in range(len(text_list)):
            if text_list[i][0] == " ":
                text_list[i] = text_list[i][1:]
            text_list[i] = text_list[i].replace("zzz", str(len(text_list)))
            text_list[i] = text_list[i].replace("  ", " ")
        
        return text_list
    
    
    def post_tweets(self):
        """ Une fonction qui poste les tweets """
        
        tweet_list = self.text_to_tweet()
        
        api = API(auth_handler=self.auth, wait_on_rate_limit=True)
    
        api.update_status(tweet_list[0])
        
        for i in range(1, len(tweet_list)):
            time.sleep(1)
            prv_tweet = api.user_timeline(count=1)
            prv_tweet_id = prv_tweet[0].id
            api.update_status(tweet_list[i], in_reply_to_status_id=prv_tweet_id)
            
            
if __name__ == "__main__":
    post = ArticlePoster()
    post.post_tweets()
