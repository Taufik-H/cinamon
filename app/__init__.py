from flask import Flask

app = Flask(__name__)

from app import views,auth
app.static_folder = 'static'