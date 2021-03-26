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
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
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
    # TODO: check username and password length
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

@app.route("/recipes")
def recipes():
    result = db.session.execute("SELECT id, recipename FROM recipes")
    recipes = result.fetchall()
    return render_template("/recipes.html", recipes=recipes)

@app.route("/recipes/<int:id>")
def recipe(id):
    sql = "SELECT recipename FROM recipes WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    recipe = result.fetchone()[0]
    return render_template("recipe.html", id=id, recipe=recipe)



    






