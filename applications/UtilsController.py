from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, relationship
from applications.database import Base, db, engine
from applications.config import LocalDevelopementConfig

@app.route("/", methods=["GET", "POST"])
def landing_page():
    return render_template("LandingPage.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    return render_template("LoginPage.html")