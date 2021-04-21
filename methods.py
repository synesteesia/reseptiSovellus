from flask import session

def clearallpopups():
  session["usednamedanger"] = False
  session["logindanger"] = False
  session["registersuccess"] = False
  session["alreadyonuserlist"] = False