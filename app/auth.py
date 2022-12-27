from flask import Flask, render_template,redirect,url_for,flash,session,request
from flask_mysqldb import MySQL
import requests
from werkzeug.security import check_password_hash, generate_password_hash
from app import app

# membuat koneksi ke database
app.secret_key = 'cinemabreakdown'
app.config['MYSQL_HOST']      = 'localhost'
app.config['MYSQL_USER']      = 'root'
app.config['MYSQL_PASSWORD']  = ''
app.config['MYSQL_DB']        = 'cinamon'
mysql = MySQL(app)

@app.route('/registrasi',methods =('GET','POST'))
def registrasi():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # check username / email
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM user WHERE username=%s OR email=%s',(username,email))
    akun = cursor.fetchone()
    if akun is None:
      cursor.execute('INSERT INTO user VALUES (NULL, %s,%s,%s)',(username,email,generate_password_hash(password)))
      mysql.connection.commit()
      flash('Registration Done!!','success')
    else:
      flash('Username or email is already register','danger')
  
  return render_template('registrasi.html')

# route login
@app.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      
      #cek data email
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM user WHERE email=%s',(email, ))
      akun = cursor.fetchone()
      if akun is None:
        flash('Login failed, please check your username','danger')
      elif not check_password_hash(akun[3], password):
        flash('Login faild, please check your password','danger')
      else:
        session['loggedin'] = True
        session['username'] = akun[1]
        return redirect(url_for('get_movies_list'))
    return render_template('login.html')

# logout
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('login'))