from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.CustomerQueries import *
import psycopg2

@app.route("/customer/<int:c_id>/home", methods=["GET", "POST"])
def Customer_home_page(c_id):
    if(request.method=='GET'):       
        return render_template('CustomerTemplates/CustomerHomePage.html', c_id=c_id)

@app.route("/booking-portal/<int:c_id>", methods=["GET", "POST"])
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
    
@app.route("/customer/<int:c_id>/trips", methods=["GET", "POST"])
def Customer_past_bookings(c_id):
    datas = get_past_bookings(c_id)
    info = []
    for i in datas:
        dict = {"from":i[0], "to":i[1], "amount":i[2], "dname":i[4], "demail":i[5], "contact":i[6], "penalties":i[3]}
        info.append(dict)
    return redirect('/CustomerTemplates/CustomerBookings', data=info)

@app.route("/customer/<int:c_id>/profile", methods=["GET","POST"])
def Customer_profile(c_id):
    data = get_customer_details(c_id)
    phone = []
    for i in data:
        phone.append(i[7])
    info = {"fname":data[0][1], "lname":data[0][2], "address":data[0][3], "dob":data[0][4], "email":data[0][5], "phone":phone}
    return render_template('CustomerTemplates/CustomerViewProfile.html', data=info)