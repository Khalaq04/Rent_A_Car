from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.AdminQueries import *

@app.route("/admin/101/home", methods=["GET", "POST"])
def Admin_page():
    if request.method == 'GET':
        # Temp:
        AdminPro = {"Id": 101, "name": "Admin1"}
        return render_template('AdminTemplates/AdminHomePage.html', AdminPro=AdminPro)


def editcars():

    if request.method == 'POST':
        action = request.form['action']
        c_vid = request.form['c_vid']

        if action == 'insert':
            c_type = request.form['c_type']
            c_model = request.form['c_model']
            c_nplate = request.form['c_nplate']
            insert_car_details(c_vid, c_type, c_model, c_nplate)
        elif action == 'delete':
            del_car_detail(c_vid)


@app.route("/admin/view-cars", methods=['GET', 'POST'])
def viewcars():
    if request.method == 'POST':
        editcars()

    cars = get_veh_details()

    return render_template('AdminTemplates/AdminCarDetails.html', cars=cars)



@app.route("/admin/panalties")
def viewpenalties():
    
    penal = show_panalties()

    return render_template('AdminTemplates/AdminPenalties.html', penal=penal)


@app.route("/admin/Employee/view", methods=['GET', 'POST'])
def employee_page():
    

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
                ename = request.form['ename']
                eaddress = request.form['eaddress']
                edob = request.form['edob']
                esalary = request.form['esalary']
                eemail = request.form['eemail']
                epassword = request.form['epassword']

                employee_action(action, eid, ename, eaddress, edob, esalary, eemail, epassword)


    emps = get_emp_details()
    return render_template('AdminTemplates/AdminEmployeeDetail.html', emps=emps)

@app.route("/admin/driver/view", methods=['GET', 'POST'])
def driver_page():

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
                dcontact(did,dphone)
                update_driver(did, dname, daddress, dsalary, ddob, demail, dpassword, dlicense)

            
            else:
                
                dname = request.form['dname']
                daddress = request.form['daddress']
                ddob = request.form['ddob']
                dsalary = request.form['dsalary']
                demail = request.form['demail']
                dpassword = request.form['dpassword']
                dlicense = request.form['dlicense']


                driver_action(action, did, dname, daddress, dsalary, ddob, demail, dpassword, dlicense)

    drivers = get_driver_details()
    return render_template('AdminTemplates/AdminDriver.html', drivers=drivers)


@app.route("/admin/customer", methods=['GET', 'POST'])
def customer_page():
    customers = get_customer_details()
    return render_template('AdminTemplates/AdminCustomer.html', customers=customers)



@app.route("/admin/customer/<fname>/phonenum", methods=['GET', 'POST'])
def customer_phonenum(fname):

    phone_numbers = customer_contact(fname)
    return render_template('AdminTemplates/AdminCustomerContact.html', fname=fname, phone_numbers=phone_numbers)

@app.route("/admin/Employee/<e_name>/phonenum", methods=['GET', 'POST'])
def emp_phonenum(e_name):

    ph_num= emp_contact(e_name)
    return render_template('AdminTemplates/AdminEmpContact.html', e_name=e_name, ph_num=ph_num)


@app.route("/admin/driver/<d_name>/phonenum", methods=['GET', 'POST'] )
def driver_phonenum(d_name):

    ph_num= driver_contact(d_name)
    return render_template('AdminTemplates/AdminDriverContact.html', d_name=d_name, ph_num=ph_num)















