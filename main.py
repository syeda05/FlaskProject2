from flask import Flask,redirect, url_for, render_template, request, flash

#importing os to get path address of images in static folder
import os

#for uploading images for add recipe
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

#for database
import firebase_admin
from firebase_admin import credentials, firestore



app = Flask(__name__)
app.config['SECRET_KEY']='supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/images'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit= SubmitField("Submit")


def db_connection():
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    return db

def getAllRecipes():
    collection = db.collection("recipes").get()
    recipes_list=[]
    for r in collection:
        recipes_list.append(r.to_dict())
    return recipes_list

db = db_connection()
recipes_list = getAllRecipes()
recipe_list_backup = recipes_list

@app.route("/")   
def view_recipes():
    recipes= getAllRecipes()
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.jpg')
    return render_template("home.html",logo=logo,recipe_list=recipes)