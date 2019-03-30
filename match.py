import sys

query = ""
args = sys.argv[1:]
if len(args)>=1:
    for x in args:
        query += "+" + x
api = '957b84a258254334bcaee1428e3e2d7d'

import requests
url = ('https://newsapi.org/v2/everything?'
       'q='+query+
       '&apiKey='+api)
response = requests.get(url)
json = response.json()

articles = json['articles']
headline = [article['title'] for article in articles]
description = [article['description'] for article in articles]

all_text = headline + description

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(ngram_range=(1,1), stop_words = 'english')
X = cv.fit_transform(all_text)
names = cv.get_feature_names() # This are the entity names (i.e. keywords)
print(names, X)

Xc = (X.T * X) # This is the matrix manipulation step
Xc.setdiag(0) # We set the diagonals to be zeroes as it's pointless to be 1

import pandas as pd
names = cv.get_feature_names() # This are the entity names (i.e. keywords)
df = pd.DataFrame(data = Xc.toarray(), columns = names, index = names)
df.to_csv('output.csv', sep = ',')
