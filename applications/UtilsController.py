from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from applications.queries.UtilsQueries import *

@app.route("/", methods=["GET", "POST"])
def landing_page():
    if (request.method=="GET"):
        return render_template("UtilsTemplates/LandingPage.html")
    else:
        try:
            if(request.form["input"]=="employee"):
                return redirect("/login-employee")
            elif(request.form["input"]=="admin"):
                return redirect("/login-admin")
            elif(request.form["input"]=="driver"):
                return redirect("/login-driver")
            else:
                return redirect("/login-customer")
        except:
            print("in except")
            return redirect("/")

@app.route("/login-employee", methods=["GET", "POST"])
def login_employee():
    if request.method == "GET":
        return render_template("UtilsTemplates/LoginPage.html", reg=0)
    
    else:
        email = request.form["email"]
        psw = request.form["psw"]

        if get_employee_authentication(email, psw)[0][0] == 1:
            e_id = get_employee_id(email)
            return redirect(url_for("employee_home_page", e_id=e_id))
        else:
            return render_template("UtilsTemplates/LoginPage.html", reg=0)

@app.route("/login-admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "GET":
        return render_template("UtilsTemplates/LoginPage.html", reg=0)
    
    else:
        email = request.form["email"]
        psw = request.form["psw"]

        if get_admin_authentication(email, psw)[0][0] == 1:
            e_id = get_employee_id(email)
            return redirect(url_for("admin_home_page", e_id=e_id))
        else:
            return render_template("UtilsTemplates/LoginPage.html", reg=0)
        
@app.route("/login-driver", methods=["GET", "POST"])
def login_driver():
    if request.method == "GET":
        return render_template("UtilsTemplates/LoginPage.html", reg=0)
    
    else:
        email = request.form["email"]
        psw = request.form["psw"]

        if get_driver_authentication(email, psw)[0][0] == 1:
            d_id = get_driver_id(email)
            return redirect(url_for("driver_home_page", d_id=d_id))
        else:
            return render_template("UtilsTemplates/LoginPage.html", reg=0)

@app.route("/login-customer", methods=["GET", "POST"])
def login_customer():
    if(request.method == 'GET'):
        return render_template("UtilsTemplates/LoginPage.html", reg=1)
    else:
        result = get_customer_authentication(request.form["email"], request.form["psw"])
        if(result[0][0]==0):
            return redirect("/login-customer")
        elif(result[0][0]==-1):
            return redirect("/register-customer")
        else:
            c_id = get_customer_id(request.form["email"])
            c_id = c_id[0][0]
            return redirect(url_for("Customer_home_page", c_id=c_id))

@app.route("/register-customer", methods=["GET", "POST"])
def register_customer():
    if(request.method == 'GET'):
        return render_template("UtilsTemplates/RegisterPage.html")
    else:
        return redirect("/register-customer")