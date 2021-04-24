from app import app
from flask import redirect, render_template, request, session
from db import db


@app.route("/addingredient", methods=["POST"])
def addingredient():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    ingredientname = request.form["ingredientname"]
    ingredientamount = request.form["ingredientamount"]
    recipeid = request.form["id"]

    sql = "INSERT INTO ingredients (ingredientname,ingredientamount,recipe_id) VALUES (:ingredientname,:ingredientamount,:recipeid)"
    db.session.execute(sql, {"ingredientname":ingredientname,"ingredientamount":ingredientamount,"recipeid":recipeid})
    db.session.commit()

    return redirect(f"/recipes/{recipeid}")


@app.route("/deleteingredient/<int:id>", methods=["POST"])
def deleteingredient(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    sql = "SELECT recipe_id FROM ingredients WHERE id=:id"
    current = db.session.execute(sql, {"id":id})
    result = current.fetchone()
    recipeid = result[0]

    sql = "DELETE FROM ingredients WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

    return redirect(f"/recipes/{recipeid}")


@app.route("/updateingredient", methods=["POST"])
def updateingredient():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    ingredientname = request.form["ingredientname"]
    ingredientamount = request.form["ingredientamount"]
    recipeid = request.form["recipeid"]
    ingredientid = request.form["ingredientid"]

    sql = "UPDATE ingredients SET ingredientname=:ingredientname, ingredientamount=:ingredientamount WHERE recipe_id=:recipeid AND id=:ingredientid"
    db.session.execute(sql, {"ingredientname":ingredientname,"ingredientamount":ingredientamount,"recipeid":recipeid,"ingredientid":ingredientid})
    db.session.commit()

    return redirect(f"/recipes/{recipeid}")
