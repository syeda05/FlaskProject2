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

@app.route("/")   #complete
def view_recipes():
    recipes= getAllRecipes()
    #print(recipes)
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.jpg')
    return render_template("home.html",logo=logo,recipe_list=recipes)

@app.route("/deleteRecipe",methods=['GET','POST']) #complete
def deleteRecipe():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.jpg')
    recipe_id = request.args.get("id")
    db.collection("recipes").document(recipe_id).delete()
    return render_template("delete-confirmation.html",logo=logo)


@app.route("/addRecipe",methods=['GET','POST'])
def addRecipe():                                   #complete
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.jpg')
    recipe_name=""
    form = UploadFileForm()

    if request.method=="GET":
        return render_template('add-recipe.html',logo=logo,form=form)
    
    #getting last id 
    if request.method == "POST":
        recipes_list = getAllRecipes()
        new_id = len(recipes_list)+80

        recipe_id = str(new_id)
        recipe_name = request.form.get("fname")
        recipe_ingredients = request.form.get("fingredients").split(',')
        recipe_instructions = request.form.get("finstructions")
        recipe_rating = request.form.get("frating")
        recipe_category = request.form.get("fcategory")
        
        if form.validate_on_submit():
            file = form.file.data #grab the file
            recipe_image = file.filename # =>'donut.png'
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
            recipe_dic = {"image":recipe_image,"id":recipe_id,"name":recipe_name,"ingredient":recipe_ingredients,"instruction":recipe_instructions,"rating":recipe_rating,"category":recipe_category}
            db.collection("recipes").document(recipe_id).set(recipe_dic)
        return render_template("add-confirmation.html",logo=logo,r_name=recipe_name)

@app.route("/editRecipe",methods=['GET','POST']) #complete
def editRecipe():

    #using os to get path of logo image
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.jpg')

    if request.method=='GET': 
        
        recipe_id = request.args.get("id") 
        doc_ref = db.collection("recipes").document(recipe_id)
        doc = doc_ref.get()
        doc = doc.to_dict()
        ingredients = str(doc["ingredient"])
        ingredients = ingredients.strip("'")
        ingredients = ingredients[1:(len(ingredients)-1)] #=>'dough','chocolate'
        ingredients = ingredients.replace("'","") 

        return render_template("edit-recipe.html",logo=logo,recipe=doc,ingredients=ingredients)
    

    if request.method == 'POST':
        recipe_id = request.form.get("fid")
        recipe_name = request.form.get("fname")
        recipe_ingredients = request.form.get("fingredients").split(",")
        recipe_instructions = request.form.get("finstructions")
        recipe_rating = request.form.get("frating")
        recipe_category = request.form.get("fcategory")
        
        new_recipe = {"id":recipe_id,"name":recipe_name,"ingredient":recipe_ingredients,"instruction":recipe_instructions,"rating":recipe_rating,"category":recipe_category}
        print(type(new_recipe))
        db.collection("recipes").document(recipe_id).update(new_recipe)
        return render_template('edit-confirmation.html',logo=logo,r_name=recipe_name)