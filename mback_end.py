from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.tokenize import word_tokenize
import json
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime


movie_data = pd.read_csv(r"movie-data/d.csv")
movie_index = pd.Series(movie_data.index, movie_data['title'].str.lower())
url = "https://yts.mx/movies/"
app = Flask(__name__)

def get_movies(movie_name):
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movie_data.overview)
    cosine_scores = linear_kernel(tfidf_matrix, tfidf_matrix)
    index = movie_index[movie_name]
    movie_scores = cosine_scores[index]
    movie_scores = list(enumerate(movie_scores))
    movie_scores = sorted(movie_scores, key=lambda x: x[1], reverse=True)
    top_index = [i[0] for i in movie_scores]
    top_picks = movie_data.loc[movie_data.index[top_index[0:1001]]]
    return top_picks

def genre_classifier(data):
    data.reset_index(inplace=True, drop=True)
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(data.genres)
    cosine_score = linear_kernel(tfidf_matrix, tfidf_matrix)
    movie_scores = cosine_score[0]
    movie_scores = list(enumerate(movie_scores))
    movie_scores_sorted = sorted(movie_scores, key=lambda x:x[1], reverse=True)
    top_index = [i[0] for i in movie_scores_sorted]
    top10_movies = data.loc[data.index[top_index[1:11]]]
    return top10_movies


def scrape_data(data):
    data.reset_index(inplace=True)
    imdb_rating = []
    thumbnail_link = []
    download_link = []
    movie_name = []
    for i in range(len(data)):
        movie_name.append(data.title[i])
        name = data.title[i].lower()
        date = data.release_date[i]
        name = re.sub(r'[^a-z0-9 '']', "", name)
        name = word_tokenize(name)
        date = datetime.strptime(date, "%Y-%m-%d")
        date = date.year
        name.append(str(date))
        name = "-".join(name)
        page = requests.get(url + name)
        print(page)
        if page.status_code == 200:
            html = BeautifulSoup(page.content, 'lxml')
            rating = html.find_all("span", itemprop='ratingValue')
            imdb_rating.append(rating[0].text)
            link = html.find_all('img', attrs={'class': 'img-responsive'})
            link = link[0]['src']
            thumbnail_link.append(link)
            download_link.append(url+name)
        else:
            imdb_rating.append("--")
            thumbnail_link.append("#")
            download_link.append(url+name)

    data = {'imdb_rating': imdb_rating, 'thumbnail_link': thumbnail_link, "download_link": download_link, "movie_name": movie_name}
    return data


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/page1", methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        movie_list = movie_data.title
        status = "not_found"
        for i in movie_list:
            if i.lower() == movie_name.lower():
                status = "found"
                break;
        if status == "not_found":
            data = {"status": "not_found"}
            data = json.dumps(data)
            return render_template("page1.html", data=data)
        else:
            top_picks = get_movies(movie_name.lower())
            top_10 = genre_classifier(top_picks)
            movies = scrape_data(top_10)
            data = {"status": "found"}
            data.update(movies)
            print(data)
            data = json.dumps(data)
            return render_template("page1.html", data=data)
        # movie_list = get_movies(movie_name)
        # return render_template("page1.html", data=movie_name)
    else:
        return render_template("page1.html")

if __name__ == '__main__':
    app.run(debug=True)
