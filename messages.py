from app import app
from flask import redirect, render_template, request, session
from db import db


@app.route("/addmessage", methods=["POST"])
def addmessage():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    username = request.form["username"]
    userid = request.form["userid"]
    content = request.form["content"]
    recipeid = request.form["id"]

    sql = "INSERT INTO messages (content, recipe_id, user_id, sent_at, edited_at) VALUES (:content,:recipeid,:userid, NOW(), NOW())"
    db.session.execute(sql, {"content":content,"recipeid":recipeid,"userid":userid})
    db.session.commit()

    return redirect(f"/recipes/{recipeid}")


@app.route("/deletemessage/<int:id>", methods=["POST"])
def deletemessage(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    sql = "SELECT recipe_id FROM messages WHERE id=:id"
    current = db.session.execute(sql, {"id":id})
    result = current.fetchone()
    recipeid = result[0]

    content = "(Viesti poistettu)"
    sql = "UPDATE messages SET content =:content WHERE id=:id"
    db.session.execute(sql, {"id":id,"content":content})
    db.session.commit()

    return redirect(f"/recipes/{recipeid}")


@app.route("/updatemessage", methods=["POST"])
def updatemessage():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    content = request.form["content"]
    recipeid = request.form["recipeid"]
    messageid = request.form["messageid"]

    sql = "UPDATE messages SET content=:content, edited_at=NOW() WHERE recipe_id=:recipeid AND id=:messageid"
    db.session.execute(sql, {"content":content,"recipeid":recipeid,"messageid":messageid})
    db.session.commit()

    return redirect(f"/recipes/{recipeid}")
