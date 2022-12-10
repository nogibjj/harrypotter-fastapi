import pandas as pd
from collections import Counter

import nltk
from wordcloud import STOPWORDS
from nltk.corpus import stopwords


"""
    The code in this file is inspired by CHANR 's Harry Potter analysis 
    https://www.kaggle.com/code/chandanarprasad/analysis-of-harry-potter-books
"""

# Read .txt data into a variable
def read_book(bookid):
    text_file = open("Data/Book" + str(bookid) + ".txt", "r", encoding="utf-8")
    data = text_file.read()
    text_file.close()
    data = data.replace("\n", "").replace("\r", "")
    return data


character_list = pd.read_csv("Data/characters_list.csv")

# Change the all words to lower cases and remove punctuations
def case_punc(book):
    book = book.lower()
    book = " ".join([word for word in book.split() if word.isalnum()])
    return book


# Find default English stop words
stopwords = nltk.corpus.stopwords.words("english")

# Defining context specific stopwords
STOPWORDS = [
    "harry",
    "potter",
    "hermione",
    "ron",
    "j",
    "k",
    "rowling",
    "s",
    "t",
    "said",
    "page",
    "professor",
    "know",
    "back",
    "i",
    "j.k",
    "like",
    "could",
    "would",
    "philosophers",
    "stone",
    "chamber",
    "secrets",
    "prisoner",
    "azbakan",
    "goblet",
    "fire",
    "order",
    "phoenix",
    "half",
    "blood",
    "prince",
    "deathly",
    "hallows",
    "looked",
    "one",
    "got",
    "get",
    "see",
    "going",
    "go",
    "told",
    "look",
    "looking",
    "tell",
    "saw",
    "think",
    "around",
    "though",
    "even",
    "still",
]

stopwords = stopwords + list(STOPWORDS)

# Remove stopwords from the books
def remove_stopwords(book_sw):
    book_sw = " ".join([word for word in book_sw.split() if word not in stopwords])
    return book_sw


# Calculate the frequency of top 20 most common terms in each book
def frequency(book_tf):
    book_tf = Counter(book_tf.split()).most_common(20)
    return book_tf


def get_freq(book_id):
    book_n = read_book(book_id)
    book_n = case_punc(book_n)
    book_n_rs = remove_stopwords(book_n)
    term_freq = frequency(book_n_rs)
    return term_freq


# '\n Top 20 most common words in book ' + book_id + '\n' +
