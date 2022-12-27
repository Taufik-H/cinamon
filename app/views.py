from flask import Flask, render_template, url_for,session,redirect,flash
import requests,json,os,urllib.request
from app import app
from app import auth


api_key = "d304673657c45d10261cad6e3f07aeb8"

# set api variable
tren_week   = "https://api.themoviedb.org/3/trending/movie/week?api_key="+api_key
tren_day    = "https://api.themoviedb.org/3/trending/movie/day?api_key="+api_key
popular     = "https://api.themoviedb.org/3/movie/popular?api_key="+api_key
detail_api  = "https://api.themoviedb.org/3/movie/{movie_id}?api_key="+api_key
trailer_api = "https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=<<api_key>>&language=en-US"


@app.route("/")
def get_movies_list(popular=popular, tren_day=tren_day, tren_week=tren_week):
    if 'loggedin' in session:
    # cek status login
        
        url         = popular
        response    = urllib.request.urlopen(url)
        movies      = response.read()
        dict        = json.loads(movies)
        movies      = []
    

        for movie in dict["results"]:
            movie = {
                "movie_id"      : movie["id"],
                "title"         : movie["title"],
                "overview"      : movie["overview"],
                "original_title": movie["original_title"],
                "backdrop_path" : "https://image.tmdb.org/t/p/original"+movie["backdrop_path"],
                "poster_path"   : "https://image.tmdb.org/t/p/w500"+movie["poster_path"],
                "rating"        : movie["vote_average"],
                "popularity"    : int(movie["popularity"]),
                "date"          : movie["release_date"]
            }

            movies.append(movie)

        url         = requests.get(tren_day)
        trend_day   = url.json()
        trending_day= []
        
        for trends_day in trend_day["results"]:
            trends_day = {
                "title"     : trends_day["title"],
                "popularity": int(trends_day["popularity"]),
                "image"     : "https://image.tmdb.org/t/p/w500"+trends_day["backdrop_path"],
                "media_type": trends_day["media_type"]
            }

            trending_day.append(trends_day)
        # get trend week

        url             = requests.get(tren_week)
        trend_week      = url.json()
        trending_week   = []
        for trends_week in trend_week["results"]:
            trends_week = {
                "title"     : trends_week["title"],
                "popularity": int(trends_week["popularity"]),
                "image"     : "https://image.tmdb.org/t/p/w500"+trends_week["backdrop_path"],
                "media_type": trends_week["media_type"]
            }

            trending_week.append(trends_week)

        # get trending
        return render_template("index.html", movie=movies, trends=trending_day, trends_week=trending_week)
    flash('Please login!','danger')
    return redirect(url_for('login'))

@app.route('/detail/<movie_id>')
def detail(movie_id):
    if 'loggedin' in session:
        detail  = requests.get(
                "https://api.themoviedb.org/3/movie/"+movie_id+"?api_key="+api_key)
        details = detail.json()

        demovie = []
        genre   = []
        for dtl in details: 
            dtl = {
                    # "genres" : genre["name"],
                    "poster_path": "https://image.tmdb.org/t/p/w500"+details["poster_path"]
                }
        demovie.append(dtl)
        for gen in details["genres"]:
                gen = {
                    "name":gen["name"]
                }
                genre.append(gen)
            # reviewer
        review_api = requests.get(
                "https://api.themoviedb.org/3/movie/"+movie_id+"/reviews?api_key="+api_key)
        review_json = review_api.json()
        reviewer = []
        for rev in review_json["results"]:
                rev = {
                    "author"        : rev["author"],
                    "author_details": rev["author_details"],
                    "content"       : rev["content"],
                    "date"          : rev["created_at"]
                }
                reviewer.append(rev)
        return render_template("detail.html", d_movie=details, demovie=demovie, genre = genre, review = reviewer)
    flash('Please login!','danger')
    return redirect(url_for('login'))

@app.route('/trailer/<movie_id>')
def trailer(movie_id):
    if 'loggedin' in session:
        trailer_api     = requests.get("https://api.themoviedb.org/3/movie/" +
                                    movie_id+"/videos?api_key="+api_key+"&language=en-US")
        trailers        = trailer_api.json()
        trailer         = []
        for tr in trailers["results"]:
            if tr["type"] == "Trailer":
                    tr  = {
                        "name": tr["name"],
                        "key": tr["key"]
                    }
                # for t in tr["list"]:
                #     print(t)
                    trailer.append(tr)
            # get review movie
            review_api  = requests.get(
                "https://api.themoviedb.org/3/movie/"+movie_id+"/reviews?api_key="+api_key)
            review_json = review_api.json()
            reviewer    = []
            for rev in review_json["results"]:
                rev = {
                    "author"        : rev["author"],
                    "author_details": rev["author_details"],
                    "content"       : rev["content"],
                    "date"          : rev["created_at"]
                }
                reviewer.append(rev)

            # return value
        return render_template('trailer.html', trailer=trailer[0], movie_id=movie_id, review=reviewer)
    flash('Please login!','danger')
    return redirect(url_for('login'))





