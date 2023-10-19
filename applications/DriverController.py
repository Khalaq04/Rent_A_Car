from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, relationship
from applications.database import Base, db, engine
from applications.config import LocalDevelopementConfig

@app.route("/driver/1/home", methods=["GET", "POST"])
def homepage():
    if(request.method=='GET'):
        #temp:
        driverInfo = {"did":1, "name":"abc"}
        return render_template('driverHomePage.html', driverInfo = driverInfo)
    