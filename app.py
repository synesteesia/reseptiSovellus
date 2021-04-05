from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    getrecipes = db.session.execute("SELECT id, recipename FROM recipes WHERE visible=1")
    recipes = getrecipes.fetchall()
    return render_template("index.html", recipes=recipes)

@app.route("/login",methods=["POST"])
def login():
    print("hei")
    form = request.form
    print("request toimii")
    username = request.form["username"]
    password = request.form["password"]
    print("request toimii")
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        # TODO: invalid username warning
         print("vaara nimi")
         return redirect("/")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            return redirect("/")
        else:
            # TODO: invalid password warning
            print("vaara passu")
            return redirect("/")

@app.route("/createNewAccount",methods=["POST"])
def createNewAccount():
    # TODO: check if username is used and password length
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/createAccount")
def createAccount():
    return render_template("/createAccount.html")

@app.route("/recipes/<int:id>")
def recipe(id):
    sql = "SELECT id, recipename FROM recipes WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    recipe = result.fetchone()

    sql= "SELECT id, ingredientname, ingredientamount FROM ingredients WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    ingredients = result.fetchall()

    sql= "SELECT id, content FROM recipecontents WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    contents = result.fetchall()

    sql = "SELECT id, content, username FROM messages WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    messages = result.fetchall()

    return render_template("recipe.html", id=id, recipe=recipe,ingredients=ingredients,contents=contents,messages=messages)

@app.route("/createrecipe")
def createrecipe():
    result = db.session.execute("SELECT id, recipename FROM recipes WHERE visible=1")
    recipes = result.fetchall()
    return render_template("/createrecipe.html", recipes=recipes) 

@app.route("/createnewrecipe",methods=["POST"])
def createnewrecipe():
    recipename = request.form["recipename"]
    sql = "INSERT INTO recipes (recipename) VALUES (:recipename) RETURNING id"
    current = db.session.execute(sql, {"recipename":recipename})
    result = current.fetchone()
    id = result[0]
    db.session.commit()
    return redirect(f"/recipes/{id}")

@app.route("/deleterecipe/<int:id>")
def deleterecipe(id):
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
    sql = "SELECT id FROM users WHERE username=:username"
    current = db.session.execute(sql, {"username":username})
    result = current.fetchone()
    userid = result[0]

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





    






