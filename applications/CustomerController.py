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
            dict = {"type": i[0], "amt": i[1]}
            cars.append(dict)
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
        assign='Yes'
        if(driver == "y"):
            driver = "NULL"
        else:
            driver = -1
            assign = 'No'
        amt = get_amount(fromdate, todate, v_type, driver)

        return redirect(url_for("confirm_booking", c_id=c_id, carname=carname, amt=amt, fromdate=fromdate, todate=todate, driver=driver, assign=assign))
    
@app.route("/customer/<int:c_id>/confirm-booking/<string:carname>/<int:amt>/<string:fromdate>/<string:todate>/<string:driver>/<string:assign>", methods=["GET","POST"])
def confirm_booking(c_id, carname, amt, fromdate, todate, driver, assign):
    if(request.method=='GET'):
        details = {"car":carname, "from":fromdate, "to":todate, "driver":assign, "amt":amt}
        return render_template('/CustomerTemplates/CustomerConfirmBooking.html', details = details)
    
    else:
        add_booking(c_id, fromdate, todate, driver, carname)
        return redirect(url_for("Customer_home_page", c_id=c_id))

@app.route("/customer/<int:c_id>/trips", methods=["GET", "POST"])
def Customer_past_bookings(c_id):
    data = get_past_bookings(c_id)
    info = []
    for i in data:
        dict = {"from":i[0], "to":i[1], "amount":i[2], "dname":i[4], "demail":i[5], "contact":i[6], "penalties":i[3]}
        info.append(dict)
    return render_template('/CustomerTemplates/CustomerBookings.html', data=info, c_id=c_id)

@app.route("/customer/<int:c_id>/curtrips", methods=["GET", "POST"])
def Customer_current_bookings(c_id):
    data = get_cur_bookings(c_id)
    info = []
    for i in data:
        dict = {"from":i[0], "to":i[1], "amount":i[2], "dname":i[3], "demail":i[4], "contact":i[5]}
        info.append(dict)
    return render_template('/CustomerTemplates/CustomerCurBookings.html', data=info, c_id=c_id)

@app.route("/customer/<int:c_id>/profile", methods=["GET","POST"])
def Customer_profile(c_id):
    if(request.method=='GET'):
        data = get_customer_details(c_id)
        phone = []
        for i in data:
            phone.append(i[7])
        info = {"fname":data[0][1], "lname":data[0][2], "address":data[0][3], "dob":data[0][4], "email":data[0][5], "phone":phone}
        return render_template('CustomerTemplates/CustomerViewProfile.html', data=info, c_id=c_id)
    else:
        phone = request.form["phone"]
        add_phone(c_id, phone)

        return redirect(url_for("Customer_profile", c_id=c_id))