from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.CustomerQueries import *

@app.route("/customer/<int:c_id>/home", methods=["GET", "POST"])
def Customer_home_page(c_id):
    if(request.method=='GET'):       
        return render_template('CustomerTemplates/CustomerHomePage.html', c_id=c_id)

@app.route("/customer/<int:c_id>/booking-portal/select-car-type", methods=["GET", "POST"])
def select_type(c_id):
    if(request.method=='GET'):
        data = get_car_types()
        cars = []
        for i in data:
            cars.append(i[0])
        return render_template('/CustomerTemplates/CustomerNewBooking.html', cars=cars, carselect=True)
    else:
        cartype = request.form["cartype"]
        return redirect(url_for('newbooking', c_id=c_id, v_type=cartype))
    
@app.route("/customer/<int:c_id>/book-a-trip/<string:v_type>", methods=["GET", "POST"])
def newbooking(c_id, v_type):
    if(request.method=='GET'):
        data = get_car_details(v_type)
        cars = []
        for i in data:
            cars.append(i[0])

        return render_template('/CustomerTemplates/CustomerNewBooking.html', cars=cars, carselect=False)
    else:
        carname = request.form["car"]
        fromdate = request.form["from"]
        todate = request.form["to"]
        driver = request.form["driver"]
        if(driver == "n"):
            driver = "NULL"
        else:
            driver = -1
        add_booking(c_id, fromdate, todate, driver, carname)

        return redirect(url_for('Customer_home_page',c_id))

@app.route("/customer/<int:c_id>/trips", methods=["GET", "POST"])
def Customer_past_bookings(c_id):
    data = get_past_bookings(c_id)
    info = []
    for i in data:
        dict = {"from":i[0], "to":i[1], "amount":i[2], "dname":i[4], "demail":i[5], "contact":i[6], "penalties":i[3]}
        info.append(dict)
    return render_template('/CustomerTemplates/CustomerBookings.html', data=info)

@app.route("/customer/<int:c_id>/profile", methods=["GET","POST"])
def Customer_profile(c_id):
    data = get_customer_details(c_id)
    phone = []
    for i in data:
        phone.append(i[7])
    info = {"fname":data[0][1], "lname":data[0][2], "address":data[0][3], "dob":data[0][4], "email":data[0][5], "phone":phone}
    return render_template('CustomerTemplates/CustomerViewProfile.html', data=info)