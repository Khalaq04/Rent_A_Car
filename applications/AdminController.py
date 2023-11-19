from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.AdminQueries import *

@app.route("/admin/<int:e_id>/home", methods=["GET", "POST"])
def admin_home_page(e_id):
    if request.method == "GET":
        return render_template('AdminTemplates/AdminHomePage.html', e_id=e_id)
    
@app.route("/admin/view-cars")
def viewcars():
    cars = get_car_details()
    return render_template('AdminTemplates/AdminCarDetails.html', cars=cars)

@app.route("/admin/edit-cars")
def editcars():

    action = request.form['action']

    if action == 'insert':
        insert_car_details(request.form["c_vid"],request.form["c_type"],request.form["c_model"],request.form["c_nplate"])
        return render_template('AdminTemplates/AdminCarDetails.html')
    
    else:
        del_car_detail(request.form["c_vid"])

@app.route("/admin/<int:e_id>/past-bookings", methods=["GET", "POST"])
def admin_past_bookings(e_id):
    if request.method == "GET":
        bookings = []
        past_bookings = get_past_bookings()
        for i in past_bookings:
            dict = {"b_id":i[0], "c_name":i[8]+" "+i[9], "c_email":i[10], "d_name":i[11], "d_email":i[12], "from":i[2], "to":i[3], "type":i[5], "model":i[6], "np":i[7], "amount":i[4], "penalty":i[13], "desc":i[14], "e_name":i[15], "e_email":i[16]}
            bookings.append(dict)
        return render_template("AdminTemplates/AdminBookings.html", bookings=bookings, e_id=e_id, status=0)
    
@app.route("/admin/<int:e_id>/new-bookings", methods=["GET", "POST"])
def admin_new_bookings(e_id):
    if request.method == "GET":
        bookings = []
        past_bookings = get_new_bookings()
        for i in past_bookings:
            dict = {"b_id":i[0], "c_name":i[7]+" "+i[8], "c_email":i[9], "from":i[1], "to":i[2], "type":i[4], "model":i[5], "np":i[6], "amount":i[3]}
            bookings.append(dict)
        return render_template("AdminTemplates/AdminBookings.html", bookings=bookings, e_id=e_id, status=-1)
    
@app.route("/admin/<int:e_id>/current-bookings", methods=["GET", "POST"])
def admin_current_bookings(e_id):
    if request.method == "GET":
        bookings = []
        past_bookings = get_current_bookings()
        for i in past_bookings:
            dict = {"b_id":i[0], "c_name":i[7]+" "+i[8], "c_email":i[9], "from":i[1], "to":i[2], "type":i[4], "model":i[5], "np":i[6], "amount":i[3], "d_name":i[10], "d_email":i[11], "e_name":i[12], "e_email":i[13]}
            bookings.append(dict)
        return render_template("AdminTemplates/AdminBookings.html", bookings=bookings, e_id=e_id, status=1)
    
# @app.route("/admin/<int:e_id>/data-analysis", methods=["GET", "POST"])
# def admin_current_bookings(e_id):
#     if request.method == "GET":
#         e_m_id = get_employee_month()