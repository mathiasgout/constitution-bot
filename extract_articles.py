# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:04:39 2020

@author: mathi
"""
import pandas as pd

# data link : https://github.com/Felixaverlant/French-Constitution
CONSTITUTION_JSON_PATH = "C:/Users/mathi/Documents/amusement/python/constitution/constitution.json"
ARTICLES_PATH = "C:/Users/mathi/Documents/amusement/python/constitution/articles.csv"

df = pd.read_json(CONSTITUTION_JSON_PATH)

""" Extraction des articles """
def extract_text(article):
    return article.get("text", "") # certains articles ont été abrogés et donc n'ont pas de textes

articles = df.articles.apply(extract_text)

""" On enlève les articles abrogés """
articles = articles[articles != ""]
articles.reset_index(drop=True, inplace=True)

""" On enregistre les articles en .csv """
articles.to_csv(ARTICLES_PATH, index=False)

