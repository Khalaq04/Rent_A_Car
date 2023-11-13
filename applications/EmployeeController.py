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
            dict = {"b_id":i[0], "c_name":i[8]+i[9], "c_email":i[10], "d_name":i[11], "d_email":i[12], "from":i[2], "to":i[3], "type":i[5], "model":i[6], "np":i[7], "amount":i[4], "penalty":i[13], "desc":i[14]}
            bookings.append(dict)
        return render_template("EmployeeTemplates/EmployeePastBookings.html", bookings=bookings, e_id=e_id)