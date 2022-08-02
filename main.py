from flask import Flask, render_template, redirect, url_for, request, make_response, session, json, g
from flask_sqlalchemy import SQLAlchemy #For Database stuff later
import pymysql #Database stuff later
from flask_admin import Admin #Maybe needed
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import *
from flask_wtf import FlaskForm #for all forms (if needed)
from wtforms import StringField, SubmitField #for all forms
from wtforms.validators import DataRequired #For all forms
import os #Likely for any secret key stuff needed with Flask
import random
from datetime import datetime
import hashlib

#from requests_html import HTML, HTMLSession #Won't know if we need this yet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mc67964:e4d415c6d3@66.248.199.216/mc67964'
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.secret_key = os.urandom(24)

##DATABASE CODE
class fuelUserCredentials(db.Model):
  username = db.Column(db.String(256),primary_key=True,nullable=False)
  password=db.Column(db.String(512),nullable=False)
  fullname=db.Column(db.String(50),nullable=False)
  address1=db.Column(db.String(100),nullable=False)
  address2=db.Column(db.String(100))
  city=db.Column(db.String(100),nullable=False)
  state=db.Column(db.String(2),nullable=False)
  zipcode=db.Column(db.String(9),nullable=False)

class FuelQuote(db.Model):
  order_id=db.Column(db.Integer,primary_key=True,nullable=False)
  username=db.Column(db.String(256),nullable=False)
  requested=db.Column(db.Integer,nullable=False)
  address=db.Column(db.String(200),nullable=False)
  deliverydate=db.Column(db.DateTime,nullable=False)
  price=db.Column(db.FLOAT,nullable=False)
  total=db.Column(db.FLOAT,nullable=False)

db.create_all()
  
  
##INDEX PAGE
@app.route('/',methods=["POST","GET"])
def index():
  if request.method=="POST":
    session.pop('user',None)
    username=request.form['username']
    password=request.form['password']
    chk=fuelUserCredentials.query.filter_by(username=username).first()
    if(chk):
      if hashlib.sha256(password.encode()).hexdigest()==chk.password:
        session['user']=chk.username
        if chk.state=="XX":
          return redirect("profile")
        else:
          return redirect("quote")
      else:
        return render_template("index.html",error_statement="Wrong password")
    else:
      return render_template("index.html",error_statement="Wrong information")
  else:
    return render_template('index.html')

##PROFILE PAGE
@app.route('/profile',methods=["POST","GET"])
def profile():
  if not g.user:
    return redirect(url_for('index'))
  if request.method=="POST":
    if ((len(request.form["fullname"])<51)and(len(request.form["fullname"])>0)) and ((len(request.form["address1"])<101)and(len(request.form["address1"])>0)) and ((len(request.form["address2"])<101) and (len(request.form["address2"])>=0)) and ((len(request.form["city"])<101) and (len(request.form["city"])>0)) and (len(request.form["zipcode"])<=9) and (len(request.form["zipcode"])>=5) and request.form["zipcode"].isnumeric() and len(request.form["state"])<=2:
      
      print(request.form["zipcode"],request.form["address1"],request.form["address2"],request.form["city"],request.form["state"],request.form["fullname"])
      
      chk = fuelUserCredentials.query.filter_by(username=session['user']).first()
      chk.fullname=request.form["fullname"]
      chk.address1=request.form["address1"]
      chk.address2=request.form["address2"]
      chk.city=request.form["city"]
      chk.state=request.form["state"]
      chk.zipcode=request.form["zipcode"]
      
      try:
        db.session.commit()
        print("Submitted? lol")
        return redirect((url_for('quote')))
      except:
        return render_template('profile.html',error_message="An error occured while updating")
    else:
      username = session['user']
      chk = fuelUserCredentials.query.filter_by(username=session['user']).first()
      if(len(chk.address2)>0):
        address2=chk.address2
      else:
        address2="Address 2"
      return render_template('profile.html',error_message="Please fix errors with your form.",username=username,fullname=chk.fullname,address1=chk.address1,address2=address2,city=chk.city,zipcode=chk.zipcode)
  else:
    username = "Settings for " + session['user']
    chk = fuelUserCredentials.query.filter_by(username=session['user']).first()
    if(len(chk.address2)>0):
      address2=chk.address2
    else:
      address2="Address 2"
    if chk.state=="XX":
      return render_template("profile.html",username=username,fullname="",address1="",address2="",city="",zipcode="",state=chk.state)
    else:
      return render_template("profile.html",username=username,fullname=chk.fullname,address1=chk.address1,address2=address2,city=chk.city,zipcode=chk.zipcode)

##QUOTE PAGE
@app.route('/quote',methods=["POST","GET"])
def quote():
  if not g.user:
    return redirect(url_for('index'))
  if request.method=="POST":
    print("POST")
    chk=fuelUserCredentials.query.filter_by(username=session['user']).first()
    address=chk.address1 + ", " + chk.city + ", "+chk.state+", " +chk.zipcode
    if request.form['quantity'].isnumeric() and int(request.form['quantity'])<100 and int(request.form['quantity'])>0:
      print(request.form["quantity"],address,request.form["DeliveryDate"],request.form["SuggestedPrice"],request.form["TotalAmount"])
    print(request.form["quantity"],address,request.form["DeliveryDate"],request.form["SuggestedPrice"],request.form["TotalAmount"])

    price=1.50
    margin=0
    print("Margin now:",margin)
    if chk.state=="TX":
      print("in state")
      margin+=0.02
    else:
      print("out of state")
      margin+=0.04

    print("Margin now:",margin)
    
    odr = FuelQuote.query.filter_by(username=session['user']).first()
    if(odr):
      print("returning customer")
      margin-=0.01
    else:
      print("New customer")

    print("Margin now POST:",margin)
    
    if int(request.form["quantity"])>1000:
      print("Large order")
      margin+=0.02
    else:
      print("Not large order")
      margin+=0.03

    print("Margin now:",margin)

    print("Adding 10 percent")
    margin+=0.1
    
    suggested=price + (margin*price)
    total=suggested*int(request.form["quantity"])
    print(total)
    
    new_order=FuelQuote(username=session['user'],requested=int(request.form["quantity"]),address=address,deliverydate=request.form["DeliveryDate"],price=suggested,total=total)
    print('session created')
    try:
      db.session.add(new_order)
      db.session.commit()
    except Exception as e:
      print(e)
      return render_template("quote.html",error_message="Unknown Error, try again")
      
    return redirect('history')
  else:
    chk=fuelUserCredentials.query.filter_by(username=session['user']).first()
    address=""
    if(chk):
      if chk.state=="XX":
        return redirect('profile')
      else:
        address=chk.address1+", "+chk.city+", "+chk.state+", "+chk.zipcode
    margin = 0
    suggest = 1.50
    odr = FuelQuote.query.filter_by(username=session['user'])
    if(odr.count()>0):
      margin-=.01
      print(session['user'],"has history",odr.count())
    else:
      margin-=0
    print("Margin now GET:",margin)
    
    if(chk.state=="TX"):
      margin+=.02
    else:
      margin+=.04
    print("margin now GET:",margin)
    margin+=.1
    print("MARGIN NOW GET:",margin)
    suggest = (margin*suggest) + suggest
    orders = []
    for order in odr:
        orders.append([order.order_id,order.requested,order.address,order.deliverydate,order.price,order.total])
    print(orders)
    return render_template("quote.html",suggest=suggest,address=address)


##HISTORY PAGE
@app.route('/history',methods=["POST","GET"])
def history():
  if not g.user:
    return redirect(url_for('index'))
  odr = FuelQuote.query.filter_by(username=session['user'])
  orders = []
  for order in odr:
    orders.append([order.order_id,order.requested,order.address,order.deliverydate,order.price,order.total])
  return render_template("history.html",josh=len(orders),orders=orders)


##REGISTER PAGE
@app.route('/register',methods=["POST","GET"])
def register():
  if request.method=="POST":
    username=request.form["username"]
    password=request.form["password"]
    encrypted_pass=hashlib.sha256(password.encode()).hexdigest()
    print(encrypted_pass)
    chk=fuelUserCredentials.query.filter_by(username=username).first()
    if (chk):
      return render_template("register.html",error_message="Username already exists")

    new_user=fuelUserCredentials(username=username,password=encrypted_pass,fullname="Full Name",address1="Address 1",address2="",city="City",state="XX",zipcode="00000")
    print('session created')
    try:
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for('index'))
    except Exception as e:
      print(e)
      return render_template("register.html",error_message="Unknown Error, try again")
  return render_template("register.html")

@app.before_request
def before_request():
  if 'user' in session:
    g.user=session['user']
    session.permanent=True
  else:
    g.user=None

if __name__=="__main__":
  app.run("0.0.0.0",debug=True)