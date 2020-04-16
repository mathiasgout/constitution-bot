# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 18:25:48 2020

@author: mathi
"""
def data_preparation(articles):

    articles_copy = articles.copy()
    
    # "(" et ")"
    articles_copy[16] = articles_copy[16].replace("(1)", "")
    articles_copy[19] = articles_copy[19].replace("(1er alinéa)", "")
    
    # "-"
    articles_copy = articles_copy.str.replace("2008-724", "2008724")
    articles_copy = articles_copy.str.replace("34-1", "341")
    articles_copy = articles_copy.str.replace("61-1", "611")
    articles_copy = articles_copy.str.replace("71-1", "711")
    articles_copy = articles_copy.str.replace("2013-1114", "20131114")
    articles_copy = articles_copy.str.replace("46-I", "46I")
    articles_copy = articles_copy.str.replace("46 I", "46I")
    articles_copy = articles_copy.str.replace("2009-1523", "20091523")
    articles_copy = articles_copy.str.replace("53-2", "532")
    articles_copy = articles_copy.str.replace("72-4", "724")
    articles_copy = articles_copy.str.replace("72-3", "723")
    articles_copy = articles_copy.str.replace("88-1028", "881028")
    articles_copy = articles_copy.str.replace("99-209", "99209")
    articles_copy = articles_copy.str.replace("2008-103", "2008103")
    articles_copy = articles_copy.str.replace("88-5", "885")
    
    # "’"
    articles_copy[11] = articles_copy[11].replace("l’a", "l'a")
    
    # "°"
    articles_copy = articles_copy.str.replace("n°", "numéro")
    articles_copy[101] = articles_copy[101].replace("2°", "deuxième")
   
    # "."
    articles_copy = articles_copy.str.replace(".", " . ")
    
    return articles_copy
    