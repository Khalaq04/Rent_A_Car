from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="CarRental",
        user="CarRental",
        password="CarRental"
    )
    cursor = conn.cursor()
    return cursor, conn

def get_employee(e_email, e_password):
    cursor, conn = connect_to_db()
    query = "select e_id from Employee where e_email='"+e_email+"' and e_password='"+e_password+"'"
    cursor.execute(query)
    id = cursor.fetchall()
    print(id)

    if not id:
        return -1

    return id[0][0]

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
    e_email = ''
    e_password = ''
    if request.method == "GET":
        return render_template("LoginPage.html", reg=0)
    else:
        e_email = request.form["email"]
        e_password = request.form["psw"]
        e_id = get_employee(e_email, e_password)

        if e_id == -1:
            return redirect("/login-employee")

        return redirect(url_for("employee_home_page", e_id=e_id))

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