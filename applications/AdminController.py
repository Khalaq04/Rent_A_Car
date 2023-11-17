from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.AdminQueries import *

@app.route("/admin/101/home", methods=["GET", "POST"])
def Admin_page():
    if request.method == 'GET':
        # Temp:
        AdminPro = {"Id": 101, "name": "Admin1"}
        return render_template('AdminTemplates/AdminHomePage.html', AdminPro=AdminPro)


def editcars():

    if request.method == 'POST':
        action = request.form['action']
        c_vid = request.form['c_vid']

        if action == 'insert':
            c_type = request.form['c_type']
            c_model = request.form['c_model']
            c_nplate = request.form['c_nplate']
            insert_car_details(c_vid, c_type, c_model, c_nplate)
        elif action == 'delete':
            del_car_detail(c_vid)


@app.route("/admin/view-cars", methods=['GET', 'POST'])
def viewcars():
    if request.method == 'POST':
        editcars()

    cars = get_veh_details()

    return render_template('AdminTemplates/AdminCarDetails.html', cars=cars)





