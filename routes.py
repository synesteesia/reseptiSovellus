from app import app
from flask import redirect, render_template, request, session
from db import db
from methods import clearallpopups

@app.route("/")
def index():
    session["usednamedanger"] = False
    getrecipes = db.session.execute("SELECT id, recipename, popularity, owner_id FROM recipes WHERE visible=1 ORDER BY popularity DESC")
    recipes = getrecipes.fetchall()
    return render_template("index.html", recipes=recipes)


@app.route("/clearpopup")
def clearpopup():
    clearallpopups()
    return redirect(request.referrer)










    






