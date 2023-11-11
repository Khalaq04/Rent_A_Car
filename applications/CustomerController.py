from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.CustomerQueries import *

@app.route("/customer/<int:c_id>/home", methods=["GET", "POST"])
def Customer_home_page(c_id):
    if(request.method=='GET'):
        data = get_customer_details(c_id)
        phone = []
        for i in data:
            phone.append(i[7])
        info = {"fname":data[0][1], "lname":data[0][2], "address":data[0][3], "dob":data[0][4], "email":data[0][5], "phone":phone}
        print(info)
        return render_template('CustomerTemplates/CustomerHomePage.html', data = info)

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
    
@app.route("/customer<int:c_id>/tripe", methods=["GET", "POST"])
def Customer_past_bookings(c_id):
    data = get_past_bookings(c_id)
    return redirect('/CustomerTemplates/CustomerBookings')