from flask import Flask, render_template, jsonify
import requests,json,os,urllib.request
from app import app

api_key ="d304673657c45d10261cad6e3f07aeb8"
#set api variable
tren_week = "https://api.themoviedb.org/3/trending/movie/week?api_key="+api_key
tren_day = "https://api.themoviedb.org/3/trending/movie/day?api_key="+api_key
popular = "https://api.themoviedb.org/3/movie/popular?api_key="+api_key
@app.route("/")
def get_movies_list(popular = popular,tren_day = tren_day, tren_week = tren_week): 
    url = popular
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

    url = requests.get(tren_day)
    trend_day = url.json()
    trending_day = []
    for trends_day in trend_day["results"]:
        trends_day ={  
         "title":trends_day["title"],
         "popularity":int(trends_day["popularity"]),
         "image": "https://image.tmdb.org/t/p/w500"+trends_day["backdrop_path"],
         "media_type":trends_day["media_type"]
        } 
    
        trending_day.append(trends_day)
    # get trend week
    
    url = requests.get(tren_week)
    trend_week = url.json()
    trending_week = []
    for trends_week in trend_week["results"]:
        trends_week ={  
         "title":trends_week["title"],
         "popularity":int(trends_week["popularity"]),
         "image": "https://image.tmdb.org/t/p/w500"+trends_week["backdrop_path"],
         "media_type":trends_week["media_type"]
        } 
    
        trending_week.append(trends_week)
    # get trending
    return render_template("index.html", movie=movies, trends = trending_day, trends_week = trending_week)

