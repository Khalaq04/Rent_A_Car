from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.AdminQueries import *
from applications.queries.EmployeeQueries import *

@app.route("/admin/<int:e_id>/home", methods=["GET", "POST"])
def admin_home_page(e_id):
    if request.method == "GET":
        return render_template('AdminTemplates/AdminHomePage.html', e_id=e_id)
    
def editcars():

    if request.method == 'POST':
        action = request.form['action']
        c_vid = request.form['c_vid']

        if action == 'insert':
            c_type = request.form['c_type']
            c_model = request.form['c_model']
            c_nplate = request.form['c_nplate']
            if c_model and c_nplate and c_type:
                insert_car_details(c_vid, c_type, c_model, c_nplate)
        elif action == 'delete':
            del_car_detail(c_vid)


@app.route("/admin/<int:e_id>/view-cars", methods=['GET', 'POST'])
def viewcars(e_id):
    if request.method == 'POST':
        try:
            editcars()
        except:
            return redirect(url_for('viewcars', e_id=e_id))

    cars = get_veh_details()
    ctype = get_car_types()
    types = []
    for i in ctype:
        types.append(i[0])

    return render_template('AdminTemplates/AdminCarDetails.html', cars=cars, e_id=e_id, types=types)

@app.route("/admin/<int:e_id>/past-bookings", methods=["GET", "POST"])
def admin_past_bookings(e_id):
    if request.method == "GET":
        bookings = []
        past_bookings = get_past_bookings()
        for i in past_bookings:
            if i[13]:
                penalty, desc = i[13], i[14]
            else:
                penalty = 0
                desc = "No Penalty"
            dict = {"b_id":i[0], "c_name":i[8]+" "+i[9], "c_email":i[10], "d_name":i[11], "d_email":i[12], "from":i[2], "to":i[3], "type":i[5], "model":i[6], "np":i[7], "amount":i[4], "penalty":penalty, "desc":desc, "e_name":i[15], "e_email":i[16]}
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
            dict = {"b_id":i[0], "c_name":i[8]+" "+i[9], "c_email":i[10], "from":i[2], "to":i[3], "type":i[5], "model":i[6], "np":i[7], "amount":i[4], "d_name":i[11], "d_email":i[12], "e_name":i[13], "e_email":i[14]}
            bookings.append(dict)
        return render_template("AdminTemplates/AdminBookings.html", bookings=bookings, e_id=e_id, status=1)
    
@app.route("/admin/<int:e_id>/data-analysis", methods=["GET", "POST"])
def data_analysis(e_id):
    if request.method == "GET":
        e_m_id,cnt = get_employee_month()
        phones = []
        details = {}

        if e_m_id>0:
            details,phone = get_employee_details(e_m_id)
            for i in phone:
                phones.append(i[0])

        car = most_car_model()
        cars = []
        for i in car:
            cars.append(i[0])

        return render_template('AdminTemplates/DataAnalysis.html', e_id=e_id, details=details, phones=phones, cnt=cnt, cars=cars)
    
@app.route("/admin/<int:e_id>/employee/view", methods=['GET', 'POST'])
def employee_page(e_id):
    

    if request.method == 'POST':
            action = request.form['action']
            eid = request.form['eid']
            if action == 'delete':
                employee_action(action, eid, None, None, None, None, None, None)


            elif action == 'update':
                ename = request.form['ename']
                eaddress = request.form['eaddress']
                esalary = request.form['esalary']
                edob = request.form['edob']
                eemail = request.form['eemail']
                epassword = request.form['epassword']
                
                update_emp(eid, ename, eaddress,edob,esalary, eemail, epassword)

            
            else:
                try:
                    ename = request.form['ename']
                    eaddress = request.form['eaddress']
                    edob = request.form['edob']
                    esalary = request.form['esalary']
                    eemail = request.form['eemail']
                    epassword = request.form['epassword']
                    ephone = request.form['ephone']

                    if ename and eaddress and edob and esalary and eemail and epassword and ephone:
                        employee_action(action, eid, ename, eaddress, edob, esalary, eemail, epassword)
                        emp_phone_in(eid,ephone)
                except:
                    return redirect(url_for('employee_page', e_id=e_id))

    emps = get_emp_details()
    return render_template('AdminTemplates/AdminEmployeeDetail.html', emps=emps, e_id=e_id)

@app.route("/admin/<int:e_id>/driver/view", methods=['GET', 'POST'])
def driver_page(e_id):

    if request.method == 'POST':
            
            action = request.form['action']
            did = request.form['did']
            if action == 'delete':
                driver_action(action, did, None, None, None, None, None, None,None)


            elif action == 'update':

                dname = request.form['dname']
                daddress = request.form['daddress']
                dsalary = request.form['dsalary']
                demail = request.form['demail']
                dpassword = request.form['dpassword']
                ddob = request.form['ddob']
                dlicense = request.form['dlicense']
                dphone = request.form['dphone']
                update_driver(did, dname, daddress, dsalary, ddob, demail, dpassword, dlicense)

            
            else:
                try:
                    dname = request.form['dname']
                    daddress = request.form['daddress']
                    ddob = request.form['ddob']
                    dsalary = request.form['dsalary']
                    demail = request.form['demail']
                    dpassword = request.form['dpassword']
                    dlicense = request.form['dlicense']
                    dphone = request.form['dphone']

                    if dname and daddress and ddob and dsalary and demail and dpassword and dlicense and dphone:
                        driver_action(action, did, dname, daddress, dsalary, ddob, demail, dpassword, dlicense)
                        dcontact(did,dphone)
                except:
                    return redirect(url_for('driver_page', e_id=e_id))

    drivers = get_driver_details()
    return render_template('AdminTemplates/AdminDriver.html', drivers=drivers, e_id=e_id)

@app.route("/admin/<int:e_id>/customer", methods=['GET', 'POST'])
def customer_page(e_id):
    customers = get_customer_details()
    return render_template('AdminTemplates/AdminCustomer.html', customers=customers, e_id=e_id)

@app.route("/admin/<int:e_id>/customer/<string:fname>/phonenum", methods=['GET', 'POST'])
def customer_phonenum(e_id, fname):

    phone_numbers = customer_contact(fname)
    return render_template('AdminTemplates/AdminCustomerContact.html', fname=fname, phone_numbers=phone_numbers, e_id=e_id)

@app.route("/admin/<int:e_id>/employee/<int:e_id1>/<string:e_name>/phonenum", methods=['GET', 'POST'])
def emp_phonenum(e_id, e_name, e_id1):
    if request.method == 'POST':
        action = request.form['action']
        try:
            if action=='insert':
                ephone = request.form['e_phone']
                emp_phone_in(e_id1,ephone)
            else:
                ephone = request.form['e_phone']
                del_ephone(ephone)
        except:
            return redirect(url_for('emp_phonenum', e_id=e_id, e_name=e_name, e_id1=e_id1))

    ph_num= emp_contact(e_name)
    return render_template('AdminTemplates/AdminEmpContact.html', e_name=e_name, ph_num=ph_num, e_id=e_id, e_id1=e_id1)


@app.route("/admin/<int:e_id>/driver/<int:d_id>/<string:d_name>/phonenum", methods=['GET', 'POST'] )
def driver_phonenum(e_id, d_name, d_id):
    if request.method == 'POST':
        try:
            action = request.form['action']
            if action=='insert':
                dphone = request.form['d_phone']
                dri_phone_in(d_id,dphone)
            else:
                dphone = request.form['d_phone']
                del_dphone(dphone)
        except:
            return redirect(url_for('driver_phonenum', e_id=e_id, d_name=d_name, d_id=d_id))

    ph_num= driver_contact(d_name)
    return render_template('AdminTemplates/AdminDriverContact.html', d_name=d_name, ph_num=ph_num, e_id=e_id, d_id=d_id)

@app.route("/admin/<int:e_id>/view-types", methods=['GET', 'POST'])
def viewtypes(e_id):
    if request.method == 'POST':
        action = request.form['action']
        try:
            if action == 'insert':
                v_type = request.form['vtype']
                v_amt = request.form['vamt']
                if v_amt and v_type:
                    insert_type(v_type, v_amt)
            elif action == 'delete':
                del_type(v_type)
            elif action == 'update':
                v_type = request.form['vtype']
                v_amt = request.form['vamt']
                if v_amt and v_type:
                    update_type(v_type, v_amt)
        except:
            return redirect(url_for('viewtypes', e_id=e_id))

    caramt = []
    camt = get_caramount()
    for i in camt:
        dict = {"type":i[0], "amt":i[1]}
        caramt.append(dict)

    return render_template('AdminTemplates/AdminTypes.html', e_id=e_id, caramt=caramt)