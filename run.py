import os
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", page_title="Browse the dictionary", list_of_letters=[a, b, c, d, e, f, g, h, i, j,k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z])


@app.route("/about")
def about():
    return render_template("about.html", page_title="About")


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact Us")


@app.route("/a")
def a():
    return render_template("a.html", page_title="A")


@app.route("/b")
def b():
    return render_template("b.html", page_title="b")


@app.route("/c")
def c():
    return render_template("c.html", page_title="c")


@app.route("/d")
def d():
    return render_template("d.html", page_title="d")


@app.route("/e")
def e():
    return render_template("e.html", page_title="e")


@app.route("/f")
def f():
    return render_template("f.html", page_title="f")


@app.route("/g")
def g():
    return render_template("g.html", page_title="g")


@app.route("/h")
def h():
    return render_template("h.html", page_title="h")


@app.route("/i")
def i():
    return render_template("i.html", page_title="i")


@app.route("/j")
def j():
    return render_template("j.html", page_title="j")


@app.route("/k")
def k():
    return render_template("k.html", page_title="k")


@app.route("/l")
def l():
    return render_template("l.html", page_title="l")


@app.route("/m")
def m():
    return render_template("m.html", page_title="m")


@app.route("/n")
def n():
    return render_template("n.html", page_title="n")


@app.route("/o")
def o():
    return render_template("o.html", page_title="o")


@app.route("/p")
def p():
    return render_template("p.html", page_title="p")


@app.route("/q")
def q():
    return render_template("q.html", page_title="q")


@app.route("/r")
def r():
    return render_template("r.html", page_title="r")


@app.route("/s")
def s():
    return render_template("s.html", page_title="s")


@app.route("/t")
def t():
    return render_template("t.html", page_title="t")


@app.route("/u")
def u():
    return render_template("u.html", page_title="u")


@app.route("/v")
def v():
    return render_template("v.html", page_title="v")


@app.route("/w")
def w():
    return render_template("w.html", page_title="w")


@app.route("/x")
def x():
    return render_template("x.html", page_title="x")


@app.route("/y")
def y():
    return render_template("y.html", page_title="y")


@app.route("/z")
def z():
    return render_template("z.html", page_title="z")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True
    )
