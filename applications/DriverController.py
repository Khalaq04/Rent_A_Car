from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
import psycopg2
from applications.queries import *

@app.route("/driver/1/home", methods=["GET", "POST"])
def driver_home_page():
    if(request.method=='GET'):
        #temp:
        driverInfo = {"did":1, "name":"abc"}
        get_car_details()
        return render_template('DriverHomePage.html', driverInfo = driverInfo)
    