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
        return render_template('/CustomerTemplates/CustomerNewBooking.html', cars=cars, carselect=True, c_id=c_id)
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

        return render_template('/CustomerTemplates/CustomerNewBooking.html', cars=cars, carselect=False, c_id=c_id)
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

        return redirect(url_for("confirm_booking", c_id=c_id, carname=carname, amt=amt, fromdate=fromdate, todate=todate, driver=driver, assign=assign, v_type=v_type))
    
@app.route("/customer/<int:c_id>/confirm-booking/<string:carname>/<int:amt>/<string:fromdate>/<string:todate>/<string:driver>/<string:assign>/<string:v_type>", methods=["GET","POST"])
def confirm_booking(c_id, carname, amt, fromdate, todate, driver, assign,v_type):
    if(request.method=='GET'):
        details = {"car":carname, "from":fromdate, "to":todate, "driver":assign, "amt":amt}
        return render_template('/CustomerTemplates/CustomerConfirmBooking.html', details = details, c_id=c_id, cartype=v_type)
    
    else:
        add_booking(c_id, fromdate, todate, driver, carname)
        return redirect(url_for("Customer_home_page", c_id=c_id))

@app.route("/customer/<int:c_id>/trips", methods=["GET", "POST"])
def Customer_past_bookings(c_id):
    data = get_past_bookings(c_id)
    info = []
    for i in data:
        dname = "not aplicable"
        demail = "not aplicable"
        if(i[6] != "none"):
            dname = i[6]
            demail = i[7]
        dict = {"bid":i[0], "vtype":i[1], "vname":i[2], "from":i[3], "to":i[4], "chandler":i[5], "dname":dname, "demail":demail, "amt":i[8], "pen":i[9]}
        info.append(dict)
    return render_template('/CustomerTemplates/CustomerBookings.html', data=info, c_id=c_id)

@app.route("/customer/<int:c_id>/curtrips", methods=["GET", "POST"])
def Customer_current_bookings(c_id):
    data = get_cur_bookings(c_id)
    info = []
    print(data)
    for i in data:
        handler = "not assigned yet, please check again later"
        driver = "not assigned yet, please check again later"
        demail = "not aplicable"
        if(i[5]):
            handler = i[5]
        if(i[6] == "none"):
            driver = "not requested"
            demail = "not aplicable"
        elif(i[6]):
            driver = i[6]
            demail = i[7]
        else:
            
            demail = i[7]
        
        dict = {"b_id":i[0], "from":i[3], "to":i[4], "vtype":i[1], "vname":i[2], "amt":i[8], "chandler":handler,"dname":driver, "cdriver":demail}
        print(dict)
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
        try:
            phone = request.form["phone"]
            add_phone(c_id, phone)
        finally:
            return redirect(url_for("Customer_profile", c_id=c_id))