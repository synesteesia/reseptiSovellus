from app import app
from flask import redirect, render_template, request, session
from db import db
from methods import clearallpopups

@app.route("/userrecipes/<int:uid>")
def userrecipes(uid):
    clearallpopups()
    session["alreadyonuserlist"] = False
    sql = "SELECT id, recipename, popularity FROM recipes r \
      INNER JOIN userrecipes u ON r.id = u.recipe_id \
      WHERE r.visible=1 AND u.user_id = :uid"
    findrecipes =  db.session.execute(sql, {"uid":uid})
    recipes = findrecipes.fetchall()
    return render_template("userrecipes.html", recipes=recipes)

@app.route("/linkrecipeanduser",methods=["POST"])
def llinkrecipeanduser():
    if session["csrf_token"] != request.form["csrf_token"]:
      abort(403)
    uid = request.form["userid"]
    rid = request.form["recipeid"]
    sql = "SELECT user_id, recipe_id FROM userrecipes WHERE user_id=:uid AND recipe_id=:rid"
    getresult = db.session.execute(sql, {"uid":uid,"rid":rid})
    result = getresult.fetchone()
    if result == None:
      session["alreadyonuserlist"] = False
      sql = "INSERT INTO userrecipes (recipe_id, user_id) VALUES (:rid,:uid)"
      db.session.execute(sql, {"rid":rid,"uid":uid})
      db.session.commit()
      sql = "UPDATE recipes SET popularity = popularity + 1 WHERE id=:rid"
      db.session.execute(sql, {"rid":rid})
      db.session.commit()
      return redirect("/")
    else:
      session["alreadyonuserlist"] = True
      return redirect("/")

@app.route("/deleteuserrecipe/<int:rid>//<int:uid>",methods=["POST"])
def deleteuserrecipe(rid, uid):
    if session["csrf_token"] != request.form["csrf_token"]:
      abort(403)
    sql = "DELETE FROM userrecipes WHERE user_id=:uid AND recipe_id=:rid"
    db.session.execute(sql, {"rid":rid,"uid":uid})
    db.session.commit()
    sql = "UPDATE recipes SET popularity = popularity - 1 WHERE id=:rid"
    db.session.execute(sql, {"rid":rid})
    db.session.commit()
    return redirect(f"/userrecipes/{uid}")