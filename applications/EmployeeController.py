from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app

@app.route("/employee/1/home", methods=["GET", "POST"])
def employee_home_page():
    if request.method == "GET":
        return render_template('EmployeeHomePage.html')