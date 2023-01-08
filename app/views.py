from flask import Flask, render_template, url_for,session,redirect,flash,request
import requests,json,os,urllib.request,mysql.connector
from app import app

# connect database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database= "cinamon"
)


api_key = "d304673657c45d10261cad6e3f07aeb8"

# set api variable
tren_week   = "https://api.themoviedb.org/3/trending/movie/week?api_key="+api_key
tren_day    = "https://api.themoviedb.org/3/trending/movie/day?api_key="+api_key
popular     = "https://api.themoviedb.org/3/movie/popular?api_key="+api_key
detail_api  = "https://api.themoviedb.org/3/movie/{movie_id}?api_key="+api_key
trailer_api = "https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=<<api_key>>&language=en-US"


@app.route("/")
def get_movies_list(popular=popular, tren_day=tren_day, tren_week=tren_week):

    # session login
        session['isLogin'] = True
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
                "id"        : trends_day["id"],
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
                "id"        : trends_week["id"],
                "title"     : trends_week["title"],
                "popularity": int(trends_week["popularity"]),
                "image"     : "https://image.tmdb.org/t/p/w500"+trends_week["backdrop_path"],
                "media_type": trends_week["media_type"]
            }

            trending_week.append(trends_week)

        # get trending
        return render_template("index.html", movie=movies, trends=trending_day, trends_week=trending_week)


@app.route('/detail/<movie_id>', methods=('GET', 'POST'))
def detail(movie_id):
    # menyimpan route detail
        session['last_url'] = request.referrer
        # mengambil requests data dari api
        detail  = requests.get(
                "https://api.themoviedb.org/3/movie/"+movie_id+"?api_key="+api_key)
        details = detail.json()

        demovie = []
        genre   = []
        for dtl in details: 
            dtl = {
                    # "genres" : genre["name"],
                    "poster_path": "https://image.tmdb.org/t/p/w500"+details["poster_path"],
                }
        demovie.append(dtl)
        formatted_x = "{:.1f}".format(details['vote_average'])
        vote_average = details['vote_average'] = formatted_x
        # return vote_average
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
        # insert data ke database
        if request.method == 'POST':
            user_id = request.form['user_id']
            movieId = movie_id
            movie_name = request.form['movie_name']
            
            # cek apakah data movie yang akan di simpan sudah ada.

            cursor = db.cursor()
            cursor.execute('SELECT * FROM save_movie WHERE movie_id=%s OR movie_name=%s',(movieId,movie_name))
            saved = cursor.fetchone()
            if saved is None:
                cursor.execute('INSERT INTO save_movie VALUES (NULL, %s,%s,%s)',(user_id,movie_name,movieId))
                db.commit()
                flash('Movie saved!','success')
                return redirect(session['last_url'])
            else:
                flash('Movie already Saved!!','danger')
                # return redirect back, diambil last url yang sudah dibikin diatas 
                return redirect(session['last_url'])
        
        return render_template("detail.html",vote_average=vote_average, d_movie=details, demovie=demovie, genre = genre, review = reviewer)
   

@app.route('/trailer/<movie_id>')
def trailer(movie_id):

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

@app.route('/mylist')
def mylist():

    if 'loggedin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM save_movie")
        saved_movies = cursor.fetchall()
        movies = []

        for saved_movie in saved_movies:
            movie_id= saved_movie[3]
            response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key='+api_key)
            movie_data = response.json()
            poster_path = movie_data["backdrop_path"]
            movie = {
            'id': saved_movie[0],
            'user_id': saved_movie[1],
            'movie_name': saved_movie[2],
            'movie_id': saved_movie[3],
            'poster_path': poster_path
            }
            movies.append(movie)
        
        return render_template('mylist.html',row=movies)
    flash('Please login!','danger')
    return redirect(url_for('login'))

@app.route('/delete/<user_id>',methods=('GET', 'POST'))
def delete(user_id):
        # user_id = user_id
        cursor = db.cursor()
        delete = "DELETE FROM save_movie WHERE id=%s"
        cursor.execute(delete,(user_id,))
        db.commit()
        return redirect(url_for('mylist'))



    



