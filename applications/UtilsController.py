from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, relationship
from applications.database import Base, db, engine
from applications.config import LocalDevelopementConfig

@app.route("/", methods=["GET", "POST"])
def landing_page():
    if (request.method=="GET"):
        return render_template("LandingPage.html")
    else:
        try:
            if(request.form["input"]=="manager"):
                return redirect("/login/manager")
            elif(request.form["input"]=="admin"):
                return redirect("/login/admin")
            elif(request.form["input"]=="driver"):
                return redirect("/login/driver")
            else:
                return redirect("/login/customer")
        except:
            print("in except")
            return redirect("/")

@app.route("/login/manager", methods=["GET", "POST"])
def login_pagem():
    return render_template("LoginPage.html")

@app.route("/login/admin", methods=["GET", "POST"])
def login_pagea():
    return render_template("LoginPage.html")

@app.route("/login/driver", methods=["GET", "POST"])
def login_paged():
    return render_template("LoginPage.html")

@app.route("/login/customer", methods=["GET", "POST"])
def login_pagec():
    #get
    return render_template("LoginPage.html")
#post: search cust db, return acc, redirect to url in cust contrlr