import pandas as pd

# data link : https://github.com/Felixaverlant/French-Constitution
CONSTITUTION_JSON_PATH = "constitution.json"
ARTICLES_PATH = "articles.csv"

df = pd.read_json(CONSTITUTION_JSON_PATH)


# Extract articles
def extract_text(article):
    # certains articles ont été abrogés et donc n'ont pas de textes
    return article.get("text", "")


articles = df.articles.apply(extract_text)

# Remove revoked articles
articles = articles[articles != ""]
articles.reset_index(drop=True, inplace=True)

#  Save articles
articles.to_csv(ARTICLES_PATH, index=False)
