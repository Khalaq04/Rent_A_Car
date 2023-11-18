from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.DriverQueries import *

@app.route("/driver/<int:d_id>/home", methods=["GET", "POST"])
def driver_home_page(d_id):
    if(request.method=='GET'):
        return render_template('DriverTemplates/DriverHomePage.html', d_id=d_id)
    
@app.route("/driver/<int:d_id>/profile", methods=["GET", "POST"])
def driver_profile(d_id):
    if request.method == "GET":
        details, phone = get_driver_details(d_id)
        phones = []
        for i in phone:
            phones.append(i[0])
        return render_template('DriverTemplates/DriverViewProfile.html', d_id=d_id, details=details, phones=phones)

@app.route("/driver/<int:d_id>/upcoming-bookings", methods=["GET", "POST"])
def driver_upcoming_bookings(d_id):
    if request.method == "GET":
        bookings = []
        current_bookings = get_upcoming_bookings(d_id)
        for i in current_bookings:
            dict = {"c_name":i[0]+" "+i[1], "c_email":i[2],"from":i[3], "to":i[4], "type":i[5], "model":i[6], "np":i[7]}
            bookings.append(dict)
        return render_template("DriverTemplates/DriverUpcomingBookings.html", bookings=bookings, d_id=d_id)