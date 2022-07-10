from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy #For Database stuff later
import pymysql #Database stuff later
from flask_admin import Admin #Maybe needed
from flask_wtf import FlaskForm #for all forms (if needed)
from wtforms import StringField, SubmitField #for all forms
from wtforms.validators import DataRequired #For all forms
import os #Likely for any secret key stuff needed with Flask
import random

from requests_html import HTML, HTMLSession #Won't know if we need this yet

app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def index():
  if request.method=="POST":
    if request.form["username"]=="admin" and request.form["password"]=="password":
      return redirect("profile")
    else:
      return render_template("index.html",error_statement="Wrong information")
  else:
    return render_template("index.html")

@app.route('/profile',methods=["POST","GET"])
def profile():
  if request.method=="POST":
    if ((len(request.form["fullname"])<51)and(len(request.form["fullname"])>0)) and ((len(request.form["address1"])<101)and(len(request.form["address1"])>0)) and ((len(request.form["address2"])<101) and (len(request.form["address2"])>=0)) and ((len(request.form["city"])<101) and (len(request.form["city"])>0)) and (len(request.form["zipcode"])<=9) and (len(request.form["zipcode"])>=5) and request.form["zipcode"].isnumeric():
      print(request.form["zipcode"],request.form["address1"],request.form["address2"],request.form["city"],request.form["state"],request.form["fullname"])
      return redirect('quote')
    else:
      return render_template('profile.html',error_message="Please fix errors with your form.")
  else:
    return render_template("profile.html")

@app.route('/quote',methods=["POST","GET"])
def quote():
  if request.method=="POST":
    print("POST")
    if request.form['quantity'].isnumeric() and int(request.form['quantity'])<100 and int(request.form['quantity'])>0:
      print(request.form["quantity"])
    return redirect('history')
  return render_template("quote.html")

@app.route('/history',methods=["POST","GET"])
def history():
  josh = random.randint(0,50)
  orders = []
  for i in range(0,josh):
    price=random.randint(1,101)
    requested=random.randint(1,10000)
    orders.append([i,requested,"Address",str(random.randint(1,12))+"-"+str(random.randint(1,31))+"-"+str(random.randint(1990,2023)),price,price*requested])
  return render_template("history.html",josh=josh,orders=orders)

@app.route('/register',methods=["POST","GET"])
def register():
  if request.method=="POST":
    return render_template("index.html")
  return render_template("register.html")

if __name__=="__main__":
  app.run("0.0.0.0",debug=True)