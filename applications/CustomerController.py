from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries import *
import psycopg2

@app.route("/customer/<int:c_id>/home", methods=["GET", "POST"])
def Customerhome_page(c_id):
    if(request.method=='GET'):
        info={"id":c_id, "name":"abc"}
        return render_template('CustomerHomePage.html', info = info)

@app.route("/booking-portal", methods=["GET", "POST"])
def newbooking():
    if(request.method=='GET'):
        cars = get_car_details()
        return render_template('CustomerNewBooking.html', cars=cars)
    else:
        info={"id":1, "name":"abc"}
        cars = get_car_details()
        print(request.form["to"], request.form["from"], request.form["car"])
        add_booking(request.form["car"], request.form["to"], request.form["from"])
        return redirect("/customer/1/home")