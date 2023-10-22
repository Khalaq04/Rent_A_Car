from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app

@app.route("/", methods=["GET", "POST"])
def landing_page():
    if (request.method=="GET"):
        return render_template("LandingPage.html")
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
    return render_template("LoginPage.html", reg=0)

@app.route("/login-admin", methods=["GET", "POST"])
def login_admin():
    return render_template("LoginPage.html", reg=0)

@app.route("/login-driver", methods=["GET", "POST"])
def login_driver():
    return render_template("LoginPage.html", reg=0)

@app.route("/login-customer", methods=["GET", "POST"])
def login_customer():
    return render_template("LoginPage.html", reg=1)

@app.route("/register-customer", methods=["GET", "POST"])
def register_customer():
    return render_template("RegisterPage.html")