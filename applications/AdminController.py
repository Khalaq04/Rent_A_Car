from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.AdminQueries import *

@app.route("/admin/101/home", methods=["GET", "POST"])
def Admin_page():
    if(request.method=='GET'):
        #temp:
        AdminPro = {"Id":101, "name":"Admin1"}
        return render_template('AdminTemplates/AdminHomePage.html', AdminPro = AdminPro)
    
"""@app.route("/admin/view-cars")
def viewcars():
    cars = get_car_details()
    return render_template('AdminTemplates/AdminCarDetails.html', cars=cars)
"""