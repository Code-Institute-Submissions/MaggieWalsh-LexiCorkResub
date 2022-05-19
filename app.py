import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import string
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

alphabetList = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@app.route("/")
@app.route("/index")
def index():
    ''' Adds letters to the home page '''
    return render_template(
        'index.html', page_title="Browse the dictionary", 
        alphabetList=alphabetList)


@app.route("/alphabet/<letter>")
def alphabet(letter):
    ''' Adds letters to the alphabet page '''
    words = mongo.db.dictionary
    found_words = list(words.find({"category" : letter.lower()}).sort("word"))
    print(letter)
    return render_template(
        'alphabet.html', page_title=letter, alphabetList=alphabetList, words=found_words)


@app.route("/register", methods=["GET", "POST"])
def register():
    ''' Adds registration function '''
    if request.method == "POST":
        # check if username exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    ''' Creates login function '''
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    ''' Dynamically creates a page for the user '''
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    ''' Logs user out '''
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Submit new word
@app.route("/submit_word", methods=["GET", "POST"])
def submit_word():
    ''' Submit new word '''
    # if user is in session, submit new word
    if request.method == "GET":
        new_word_value = request.args.get('new_word')
        if new_word_value is not None:
            new_word_value = new_word_value.lower()

    if request.method == "POST":
        existing_word = mongo.db.dictionary.find_one(
            {"word": request.form.get("word").lower()})

        if not existing_word:
            word = {
                "word": request.form.get("word").lower(),
                "category": request.form.get("category"),
                "definition": request.form.get("definition"),
                "created": session["user"]
            }
            mongo.db.dictionary.insert_one(word)
        
        # if new word is added successfully, redirect user to dashboard
            flash(
                "Word added successfully.")
            return redirect(url_for("index"))

        # if the word already exists, redirect to new instance of the form
        # and inform the word exists
        else:
            flash("This word already exists, please submit a new word")
            return redirect(url_for("submit_word"))

    categories = mongo.db.dictionary.find().sort("word")
    return render_template(
        "submit_word.html",
        categories=categories,
        new_word=new_word_value)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

