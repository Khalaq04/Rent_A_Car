from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.EmployeeQueries import *

@app.route("/employee/<int:e_id>/home", methods=["GET", "POST"])
def employee_home_page(e_id):
    if request.method == "GET":
        return render_template('EmployeeTemplates/EmployeeHomePage.html', e_id=e_id)
    
@app.route("/employee/<int:e_id>/profile", methods=["GET", "POST"])
def employee_profile(e_id):
    if request.method == "GET":
        details, phone = get_employee_details(e_id)
        phones = []
        for i in phone:
            phones.append(i[0])
        return render_template('EmployeeTemplates/EmployeeViewProfile.html', e_id=e_id, details=details, phones=phones)
    
@app.route("/employee/<int:e_id>/past-bookings", methods=["GET", "POST"])
def employee_past_bookings(e_id):
    if request.method == "GET":
        bookings = []
        past_bookings = get_employee_past_bookings(e_id)
        for i in past_bookings:
            if i[13]:
                penalty, desc = i[13], i[14]
            else:
                penalty = 0
                desc = "No Penalty"
            dict = {"b_id":i[0], "c_name":i[8]+" "+i[9], "c_email":i[10], "d_name":i[11], "d_email":i[12], "from":i[2], "to":i[3], "type":i[5], "model":i[6], "np":i[7], "amount":i[4], "penalty":penalty, "desc":desc}
            bookings.append(dict)
        return render_template("EmployeeTemplates/EmployeePastBookings.html", bookings=bookings, e_id=e_id)
    
@app.route("/employee/<int:e_id>/current-bookings", methods=["GET", "POST"])
def employee_current_bookings(e_id):
    if request.method == "GET":
        bookings = []
        current_bookings = get_employee_current_bookings(e_id)
        for i in current_bookings:
            dict = {"b_id":i[0], "c_name":i[8]+" "+i[9], "c_email":i[10], "d_name":i[11], "d_email":i[12], "from":i[2], "to":i[3], "type":i[5], "model":i[6], "np":i[7], "amount":i[4]}
            bookings.append(dict)
        return render_template("EmployeeTemplates/EmployeeCurrentBookings.html", bookings=bookings, e_id=e_id)
    
    else:
        b_id = request.form["bid"]
        penalty = request.form["penalty"]
        desc = request.form["description"]

        if penalty>0:
            close_booking(b_id, penalty, desc)

        bookings = []
        current_bookings = get_employee_current_bookings(e_id)
        for i in current_bookings:
            dict = {"b_id":i[0], "c_name":i[8]+" "+i[9], "c_email":i[10], "d_name":i[11], "d_email":i[12], "from":i[2], "to":i[3], "type":i[5], "model":i[6], "np":i[7], "amount":i[4]}
            bookings.append(dict)
        return render_template("EmployeeTemplates/EmployeeCurrentBookings.html", bookings=bookings, e_id=e_id)
    
@app.route("/employee/<int:e_id>/new-bookings", methods=["GET", "POST"])
def employee_new_bookings(e_id):
    if request.method == "GET":
        bookings = []
        new_bookings = get_employee_new_bookings()
        for i in new_bookings:
            if not i[1]:
                d_id = 0
            else:
                d_id = i[1]
            dict = {"b_id":i[0], "d_id":d_id, "c_name":i[4]+" "+i[5], "c_email":i[6], "from":i[2], "to":i[3], "amount":i[7], "type":i[8], "model":i[9], "np":i[10]}
            bookings.append(dict)

        drivers = []
        for i in get_drivers():
            if not i[0] == -1:
                drivers.append({"d_id":i[0], "d_name":i[1]})

        return render_template("EmployeeTemplates/EmployeeNewBookings.html", bookings=bookings, e_id=e_id, drivers=drivers)
    
    else:
        b_id = request.form["bid"]
        d_id = request.form["did"]
        e_id = request.form["eid"]

        confirm_booking(b_id, e_id, d_id)

        bookings = []
        new_bookings = get_employee_new_bookings()
        for i in new_bookings:
            if not i[1]:
                d_id = 0
            else:
                d_id = i[1]
            dict = {"b_id":i[0], "d_id":d_id, "c_name":i[4]+" "+i[5], "c_email":i[6], "from":i[2], "to":i[3], "amount":i[7], "type":i[8], "model":i[9], "np":i[10]}
            bookings.append(dict)

        drivers = []
        for i in get_drivers():
            if not i[0] == -1:
                drivers.append({"d_id":i[0], "d_name":i[1]})

        return render_template("EmployeeTemplates/EmployeeNewBookings.html", bookings=bookings, e_id=e_id, drivers=drivers)