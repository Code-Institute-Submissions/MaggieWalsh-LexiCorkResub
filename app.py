import os
from flask import Flask, render_template
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", page_title="Browse the dictionary", list_of_letters=[1, 2, 3, 4, 5])


@app.route("/about")
def about():
    return render_template("about.html", page_title="About")


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact Us")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )