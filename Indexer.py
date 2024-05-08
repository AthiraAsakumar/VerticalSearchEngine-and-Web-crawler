from nltk.stem.porter import PorterStemmer
import collections
from nltk.corpus import stopwords
import string

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from flask import Flask, render_template, request

stopwords_ = stopwords.words("english")
stemmer = PorterStemmer()
nltk.download("punkt")
nltk.download("stopwords")


file_path="publicationurls.csv"
def i_idx(file_path):
    crawled_data = pd.read_csv("publicationurls.csv")
    article_titles = crawled_data["Title"]
    i_idx = {}
    document_id = 0
    for article_id in article_titles:
        tokens = word_tokenize(article_id)
        tokens = [t.translate(str.maketrans("", "", string.punctuation))
                 for t in tokens]
        tokens = [article_id for article_id in tokens if article_id]
        tokens_lwr = [w.lower() for w in tokens]
        removed_stopwords = [w for w in tokens_lwr if w not in stopwords_]
        stemmed_title = [stemmer.stem(w) for w in removed_stopwords]
        for a in stemmed_title:
            vl_ = i_idx.get(a)
            if vl_ == None:
                tmp_list = [1, [document_id]]
                i_idx[a] = tmp_list
            else:
                tmp_list = i_idx[a]
                if document_id not in tmp_list[1]:
                    tmp_list[1].append(document_id)
                    tmp_list[0] += 1
        document_id += 1
    ordered_index = collections.OrderedDict(
        sorted(i_idx.items()))
    return ordered_index
title_i_idx = i_idx(file_path)


def preprocessing(query_text):

    tokens = word_tokenize(query_text)
    tokens = [t.translate(str.maketrans("", "", string.punctuation))
             for t in tokens]
    tokens = [article_id for article_id in tokens if article_id]
    tokens_lwr = [w.lower() for w in tokens]
    removed_stopwords = [w for w in tokens_lwr if w not in stopwords_]
    st_qry = [stemmer.stem(w) for w in removed_stopwords]

    return st_qry


def searchfunction(st_qry, title_i_idx):
    matching_docs = []
    for tm in st_qry:
        pl = title_i_idx.get(tm)
        if pl is not None:
            matching_docs.append(pl[1])

    return matching_docs


def searchfunction_results1(matching_docs):
    dataframe = pd.read_csv(file_path)
    rstIDS = list(set.intersection(*map(set, matching_docs)))
    results1 = dataframe.iloc[rstIDS].T.to_dict("dict")

    return results1

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/searchfunction", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        query = request.form.get("searchfunction_term")
#print(query)
        idx = i_idx(file_path=file_path)
        stem_query = preprocessing(query)
        p_result = searchfunction(stem_query, idx)
        result_list = searchfunction_results1(p_result)
        return render_template("results.html", result_list=result_list)
    else:
        return render_template("index.html")
app.run()