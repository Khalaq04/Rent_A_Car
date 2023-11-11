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
def employee_all_bookings(e_id):
    if request.method == "GET":
        dict = {"b_id":"1", "c_id":"1", "d_id":"3", "v_id":"2", "from":"2023-10-20", "to":"2023-10-21", "type":"Sedan", "model":"Swift", "np":"UP-32-AA-1234", "amount":"2000"}
        bookings = []
        bookings.append(dict)
        return render_template("EmployeeTemplates/EmployeePastBookings.html", bookings=bookings)