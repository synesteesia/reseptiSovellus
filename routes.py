from app import app
from flask import redirect, render_template, request, session
from db import db
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    session["usednamedanger"] = False
    getrecipes = db.session.execute("SELECT id, recipename, popularity FROM recipes WHERE visible=1 ORDER BY popularity DESC")
    recipes = getrecipes.fetchall()
    return render_template("index.html", recipes=recipes)

@app.route("/login",methods=["POST"])
def login():
    form = request.form
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    hash_value = user[0]
    if check_password_hash(hash_value,password):
      session["passworddanger"] = False
      session["registersuccess"] = False
      session["username"] = username
      session["id"] = user[1]
      return redirect("/")
    else:
      session["passworddanger"] = True
      print("vaara passu")
      return redirect("/")

@app.route("/createNewAccount",methods=["POST"])
def createNewAccount():
    username = request.form["username"]
    sql = "SELECT username FROM users WHERE username=:username"
    getname = db.session.execute(sql, {"username":username})
    result = getname.fetchone()
    if result == None:
      password = request.form["password"]
      hash_value = generate_password_hash(password)
      sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
      db.session.execute(sql, {"username":username,"password":hash_value})
      db.session.commit()
      session["registersuccess"] = True
      return redirect("/")
    else:
      session["usednamedanger"] = True
      return redirect("/createAccount")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/createAccount")
def createAccount():
    session["passworddanger"] = False
    return render_template("/createAccount.html")

    
    return render_template("/createAccount.html")

@app.route("/recipes/<int:id>")
def recipe(id):
    session["alreadyonuserlist"] = False
    sql = "SELECT id, recipename FROM recipes WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    recipe = result.fetchone()

    sql= "SELECT id, ingredientname, ingredientamount FROM ingredients WHERE recipe_id=:id ORDER BY id ASC"
    result = db.session.execute(sql, {"id":id})
    ingredients = result.fetchall()

    sql= "SELECT id, content FROM recipecontents WHERE recipe_id=:id ORDER BY id ASC"
    result = db.session.execute(sql, {"id":id})
    contents = result.fetchall()

    sql = "SELECT id, content, username FROM messages WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    messages = result.fetchall()

    return render_template("recipe.html", id=id, recipe=recipe,ingredients=ingredients,contents=contents,messages=messages)

@app.route("/createrecipe")
def createrecipe():
    session["alreadyonuserlist"] = False
    result = db.session.execute("SELECT id, recipename FROM recipes WHERE visible=1")
    recipes = result.fetchall()
    return render_template("/createrecipe.html", recipes=recipes) 

@app.route("/createnewrecipe",methods=["POST"])
def createnewrecipe():
    recipename = request.form["recipename"]
    content = request.form["content"]
    sql = "INSERT INTO recipes (recipename) VALUES (:recipename) RETURNING id"
    current = db.session.execute(sql, {"recipename":recipename})
    result = current.fetchone()
    id = result[0]
    db.session.commit()
    sql = "INSERT INTO recipecontents (content,recipe_id) VALUES (:content,:id)"
    db.session.execute(sql, {"content":content,"id":id})
    db.session.commit()
    return redirect(f"/recipes/{id}")

@app.route("/deleterecipe/<int:id>")
def deleterecipe(id):
    session["alreadyonuserlist"] = False
    sql = "UPDATE recipes SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect("/")

@app.route("/addingredient",methods=["POST"])
def addIngredient():
    ingredientname = request.form["ingredientname"]
    ingredientamount = request.form["ingredientamount"]
    recipeid = request.form["id"]
    sql = "INSERT INTO ingredients (ingredientname,ingredientamount,recipe_id) VALUES (:ingredientname,:ingredientamount,:recipeid)"
    db.session.execute(sql, {"ingredientname":ingredientname,"ingredientamount":ingredientamount,"recipeid":recipeid})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/deleteingredient/<int:id>")
def deleteingredient(id):
    sql = "SELECT recipe_id FROM ingredients WHERE id=:id"
    current = db.session.execute(sql, {"id":id})
    result = current.fetchone()
    recipeid = result[0]
    sql = "DELETE FROM ingredients WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/addmessage",methods=["POST"])
def addmessage():
    username = request.form["username"]
    userid = request.form["userid"]
    content = request.form["content"]
    recipeid = request.form["id"]
    sql = "INSERT INTO messages (content, username, recipe_id, user_id) VALUES (:content,:username,:recipeid,:userid)"
    db.session.execute(sql, {"content":content,"username":username,"recipeid":recipeid,"userid":userid})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/deletemessage/<int:id>")
def deletemessage(id):
    sql = "SELECT recipe_id FROM messages WHERE id=:id"
    current = db.session.execute(sql, {"id":id})
    result = current.fetchone()
    recipeid = result[0]
    sql = "DELETE FROM messages WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/addcontent",methods=["POST"])
def addcontent():
    content = request.form["content"]
    recipeid = request.form["id"]
    sql = "INSERT INTO recipecontents (content,recipe_id) VALUES (:content,:recipeid)"
    db.session.execute(sql, {"content":content,"recipeid":recipeid})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/deletecontent/<int:id>")
def deletecontent(id):
    sql = "SELECT recipe_id FROM recipecontents WHERE id=:id"
    current = db.session.execute(sql, {"id":id})
    result = current.fetchone()
    recipeid = result[0]
    sql = "DELETE FROM recipecontents WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/changerecipename",methods=["POST"])
def changerecipename():
    newname = request.form["newname"]
    recipeid = request.form["id"]
    sql = "UPDATE recipes SET recipename=:newname WHERE id=:recipeid"
    db.session.execute(sql, {"newname":newname,"recipeid":recipeid})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/updaterecipecontent",methods=["POST"])
def updaterecipecontent():
    content = request.form["content"]
    recipeid = request.form["recipeid"]
    contentid = request.form["contentid"]
    sql = "UPDATE recipecontents SET content=:content WHERE recipe_id=:recipeid AND id=:contentid"
    db.session.execute(sql, {"content":content,"recipeid":recipeid,"contentid":contentid})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/updateingredient",methods=["POST"])
def updateingredient():
    ingredientname = request.form["ingredientname"]
    ingredientamount = request.form["ingredientamount"]
    recipeid = request.form["recipeid"]
    ingredientid = request.form["ingredientid"]
    sql = "UPDATE ingredients SET ingredientname=:ingredientname, ingredientamount=:ingredientamount WHERE recipe_id=:recipeid AND id=:ingredientid"
    db.session.execute(sql, {"ingredientname":ingredientname,"ingredientamount":ingredientamount,"recipeid":recipeid,"ingredientid":ingredientid})
    db.session.commit()
    return redirect(f"/recipes/{recipeid}")

@app.route("/userrecipes/<int:id>")
def userrecipes(id):
    session["alreadyonuserlist"] = False
    sql = "FROM recipes, users, userrecipes WHERE "
    findrecipes =  db.session.execute(sql, {"id":id})
    recipeid = findrecipes.fetchall()
    sql = "SELECT id, recipename FROM recipes WHERE id=:recipeid"
    getrecipes = db.session.execute(sql, {"recipeid":recipeid})
    recipes = getrecipes.fetchall()
    return render_template("userrecipes.html", recipes=recipes)

@app.route("/linkrecipeanduser/<int:rid>/<int:uid>",methods=["GET"])
def linkrecipeanduser(rid, uid):
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





    






