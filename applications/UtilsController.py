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
            if(request.form["input"]=="employee"):
                return redirect("/login-employee")
            elif(request.form["input"]=="admin"):
                return redirect("/login-admin")
            elif(request.form["input"]=="driver"):
                return redirect("/login-driver")
            else:
                return redirect("/login-customer")
        except:
            print("in except")
            return redirect("/")

@app.route("/login-employee", methods=["GET", "POST"])
def login_page_employee():
    return render_template("LoginPage.html")

@app.route("/login-admin", methods=["GET", "POST"])
def login_page_admin():
    return render_template("LoginPage.html")

@app.route("/login-driver", methods=["GET", "POST"])
def login_paged():
    return render_template("LoginPage.html")

@app.route("/login-customer", methods=["GET", "POST"])
def login_pagec():
    return render_template("LoginPage.html")