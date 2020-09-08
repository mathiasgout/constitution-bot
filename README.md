# Constitution Bot
 
 Un bot twitter permettant de twitter des articles ressemblant à ceux de la Constitution de la République Française.
<br>Les articles sont générés par un réseau de neurones récurrents entrainé avec les textes de cette constitution.

Lien vers bot : https://twitter.com/constFR_bot

<p align="center">
  <img src="https://raw.githubusercontent.com/mathiasgout/constitution_bot/master/images/screenshot_tweets.png">
</p>

## Instructions

- `main.py` permet de générer et tweeter un article.
- `train_model.py` permet d'entrainer son propre RNN. Le modèle est sauvegardé dans le dossier `models/`. 

## Requirements

Les packages suivants sont nécéssaires :

- python>=3.5
- pandas
- tensorflow
- tweepy
- numpy

### Installation locale

Il possible d'installer les packages en utilisant `pip` :
```
$ pip install -r requirements.txt
