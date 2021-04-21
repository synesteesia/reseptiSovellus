from app import app
from flask import redirect, render_template, request, session
from db import db
from methods import clearallpopups
from werkzeug.security import check_password_hash, generate_password_hash
import os

@app.route("/login",methods=["POST"])
def login():
    form = request.form
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password, id, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None: 
        session["logindanger"] = True
        return redirect("/")
    hash_value = user[0]
    if check_password_hash(hash_value,password):
      clearallpopups()
      session["username"] = username
      session["id"] = user[1]
      session["csrf_token"] = os.urandom(16).hex()
      session["admin"] = user[2]
      return redirect("/")
    else:
      session["logindanger"] = True
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
    clearallpopups()
    del session["username"]
    del session["id"]
    del session["admin"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/createAccount")
def createAccount():
    session["logindanger"] = False
    return render_template("/createAccount.html")