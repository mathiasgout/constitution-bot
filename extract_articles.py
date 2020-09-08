import requests
import os
import pandas as pd

# articles path
DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
if os.path.isdir(DIR_PATH) is False:
    os.mkdir(DIR_PATH)

ARTICLES_PATH = os.path.join(DIR_PATH, "articles.csv")

# data link : https://github.com/Felixaverlant/French-Constitution
r = requests.get("https://raw.githubusercontent.com/Felixaverlant/French-Constitution/master/constitution.json")
j = r.json()
df = pd.DataFrame.from_dict(j)

# Extract articles
def extract_text(article):
    # certains articles ont été abrogés et donc n'ont pas de textes
    return article.get("text", "")

articles = df.articles.apply(extract_text)

# Remove revoked articles
articles = articles[articles != ""]
articles.reset_index(drop=True, inplace=True)

#  Save articles
articles.to_csv(ARTICLES_PATH, index=False)
