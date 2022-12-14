from flask import Flask, render_template, jsonify
import requests,json,os,urllib.request
from app import app


@app.route("/")
def get_movies_list():
    
    url = "https://api.themoviedb.org/3/movie/popular?api_key=d304673657c45d10261cad6e3f07aeb8&language=en-US&page=1".format(
        os.environ.get("TMDB_API_KEY"))
    # get genre name

    response = urllib.request.urlopen(url)
    movies = response.read()
    dict = json.loads(movies)
    movies = []
    
    
    for movie in dict["results"]:
        movie = {
            "title": movie["title"],
            "overview": movie["overview"],
            "original_title": movie["original_title"],
            "backdrop_path": "https://image.tmdb.org/t/p/original"+movie["backdrop_path"],
            "poster_path": "https://image.tmdb.org/t/p/w500"+movie["poster_path"],
            "rating":movie["vote_average"],
            "popularity":int(movie["popularity"]),
            "date":movie["release_date"]
        }
        

        movies.append(movie)
    popular = movies[0:3]

    # return popular
    return render_template("index.html", movie=movies, popular=popular)


@app.route('/tren')
def trending():
    url = "https://api.themoviedb.org/3/trending/movie/week?api_key=d304673657c45d10261cad6e3f07aeb8".format(
        os.environ.get("TMDB_API_KEY"))
    response = urllib.request.urlopen(url)
    trend = response.read()
    dict = json.loads(trend)
    dict['results']
    return dict


    
         
