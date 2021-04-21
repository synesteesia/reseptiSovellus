from app import app
from flask import redirect, render_template, request, session
from db import db

@app.route("/addcontent",methods=["POST"])
def addcontent():
    if session["csrf_token"] != request.form["csrf_token"]:
      abort(403)
    content = request.form["content"]
    recipeid = request.form["id"]
    sql = "INSERT INTO recipecontents (content,recipe_id) VALUES (:content,:recipeid)"
    db.session.execute(sql, {"content":content,"recipeid":recipeid})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/deletecontent/<int:id>",methods=["POST"])
def deletecontent(id):
    if session["csrf_token"] != request.form["csrf_token"]:
      abort(403)
    sql = "SELECT recipe_id FROM recipecontents WHERE id=:id"
    current = db.session.execute(sql, {"id":id})
    result = current.fetchone()
    recipeid = result[0]
    sql = "DELETE FROM recipecontents WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/updaterecipecontent",methods=["POST"])
def updaterecipecontent():
    if session["csrf_token"] != request.form["csrf_token"]:
      abort(403)
    content = request.form["content"]
    recipeid = request.form["recipeid"]
    contentid = request.form["contentid"]
    sql = "UPDATE recipecontents SET content=:content WHERE recipe_id=:recipeid AND id=:contentid"
    db.session.execute(sql, {"content":content,"recipeid":recipeid,"contentid":contentid})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")