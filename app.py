import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for,
    )
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

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
    """Adds letters to the home page"""
    words = list(mongo.db.dictionary.aggregate([{'$sample': {'size': 1}}]))
    return render_template(
        "index.html",
        page_title="Browse the dictionary", alphabetList=alphabetList,
        words=words
    )


@app.route("/alphabet/<letter>")
def alphabet(letter):
    """Adds words to the alphabet page"""
    alpha_list = alphabetList
    words = mongo.db.dictionary
    found_words = list(
        words.find({"category_name": letter.lower()}).sort("word")
    )
    if letter in alpha_list:
        return render_template(
            "alphabet.html",
            page_title=letter,
            alphabetList=alphabetList,
            words=found_words
            )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Adds registration function"""
    if request.method == "POST":
        # check db for username
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Creates login function"""
    if request.method == "POST":
        # check db for username
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # if password not in db
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # if username not in db
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """Dynamically creates profile page for new user"""
    # user's name retrieved from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    words = list(mongo.db.dictionary.find({'created_by': username}))

    if session["user"]:
        return render_template("profile.html", username=username, words=words)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """Logs user out"""
    # log user out
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/submit_word", methods=["GET", "POST"])
def submit_word():
    """Submit word"""
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if request.method == "GET":
        new_word_value = request.args.get("new_word")
        if new_word_value is not None:
            new_word_value = new_word_value.lower()
    if request.method == "POST":
        existing_word = mongo.db.dictionary.find_one(
            {"word": request.form.get("word").lower()}
        )

        if not existing_word:
            word = {
                "word": request.form.get("word").lower(),
                "category_name": request.form.get("category").lower(),
                "definition": request.form.get("definition"),
                "use": request.form.get("use"),
                "created_by": session["user"],
            }
            mongo.db.dictionary.insert_one(word)
            flash("Word added successfully.")
            return redirect(url_for("index"))
            # redirect if word exists
        else:
            flash(
                "Looks like this word already exists, try adding another word."
                )
            if session["user"]:
                return redirect(url_for("submit_word"))

    words = list(mongo.db.dictionary.find())
    return render_template(
        "submit_word.html", dictionary=words, alphabet=alphabetList)


@app.route("/edit_word/<word_id>", methods=["GET", "POST"])
def edit_word(word_id):
    """Edit word"""
    dictionary = mongo.db.dictionary
    if request.method == "POST":
        existing_word = mongo.db.dictionary.find_one(
            {"_id": ObjectId(word_id)})
        print(request.form.get("category"))

        if existing_word:
            submit = {
                "word": request.form.get("word"),
                "category_name": request.form.get("category").lower(),
                "definition": request.form.get("definition"),
                "use": request.form.get("use"),
                "created_by": session["user"],
            }
            dictionary.replace_one({"_id": ObjectId(word_id)}, submit)
            flash("Word updated successfully.")
            return redirect(url_for("profile", username=session["user"]))

    word = dictionary.find_one({"_id": ObjectId(word_id)})

    return render_template(
        "edit_word.html", word=word, alphabet=alphabetList
    )


@app.route("/delete_word/<word_id>")
def delete_word(word_id):
    """Delete word"""
    username = mongo.db.users.find_one(
        {"username": session["user"]}
        )["username"]
    mongo.db.dictionary.delete_one({"_id": ObjectId(word_id)})
    flash("Word succesfully deleted!")
    return redirect(url_for("profile", username=username))


@app.errorhandler(404)
def page_not_found(error):
    """
    If 404 error occurs, user directed to custom 404 page
    """
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(err):
    """
    If 500 error occurs, user directed to custom 500 page
    """
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=False
        )
