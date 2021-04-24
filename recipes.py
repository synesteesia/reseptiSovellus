from app import app
from flask import redirect, render_template, request, session
from db import db
from methods import clearallpopups


@app.route("/createrecipe")
def createrecipe():
    clearallpopups()
    result = db.session.execute("SELECT id, recipename FROM recipes WHERE visible=1")
    recipes = result.fetchall()

    return render_template("/createrecipe.html", recipes=recipes) 


@app.route("/createnewrecipe",methods=["POST"])
def createnewrecipe():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    recipename = request.form["recipename"]
    content = request.form["content"]

    sql = "INSERT INTO recipes (recipename,owner_id) VALUES (:recipename,:owner_id) RETURNING id"
    current = db.session.execute(sql, {"recipename":recipename,"owner_id":session["id"]})
    result = current.fetchone()
    id = result[0]
    db.session.commit()

    sql = "INSERT INTO recipecontents (content,recipe_id) VALUES (:content,:id)"
    db.session.execute(sql, {"content":content,"id":id})
    db.session.commit()

    return redirect(f"/recipes/{id}")


@app.route("/deleterecipe/<int:id>", methods=["POST"])
def deleterecipe(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    clearallpopups()

    sql = "UPDATE recipes SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

    return redirect("/")


@app.route("/changerecipename", methods=["POST"])
def changerecipename():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    newname = request.form["newname"]
    recipeid = request.form["id"]

    sql = "UPDATE recipes SET recipename=:newname WHERE id=:recipeid"
    db.session.execute(sql, {"newname":newname,"recipeid":recipeid})
    db.session.commit()

    return redirect(f"/recipes/{recipeid}")    


@app.route("/recipes/<int:id>")
def recipe(id):
    clearallpopups()

    sql = "SELECT id, recipename, owner_id FROM recipes WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    recipe = result.fetchone()

    if recipe[2] == session["id"]:
       session["owner"] = True

    else:
       session["owner"] = False

    sql= "SELECT id, ingredientname, ingredientamount FROM ingredients WHERE recipe_id=:id ORDER BY id ASC"
    result = db.session.execute(sql, {"id":id})
    ingredients = result.fetchall()

    sql= "SELECT id, content FROM recipecontents WHERE recipe_id=:id ORDER BY id ASC"
    result = db.session.execute(sql, {"id":id})
    contents = result.fetchall()

    sql = "SELECT m.id, m.content, u.username, m.sent_at, m.edited_at, m.user_id FROM messages m, users u\
      WHERE m.user_id=u.id AND recipe_id=:id ORDER BY sent_at ASC"
    result = db.session.execute(sql, {"id":id})
    messages = result.fetchall()
    messages = [(m[0], m[1], m[2], m[4], m[3] == m[4], m[5]) for m in messages]

    return render_template("recipe.html", id=id, recipe=recipe,ingredients=ingredients,contents=contents,messages=messages)
