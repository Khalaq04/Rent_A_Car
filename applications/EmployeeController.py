from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="crd",
        user="crd",
        password="crd"
    )
    cursor = conn.cursor()
    return cursor, conn

@app.route("/employee/<int:e_id>/home", methods=["GET", "POST"])
def employee_home_page(e_id):
    if request.method == "GET":
        return render_template('EmployeeHomePage.html')
    
@app.route("/employee/1/all-bookings", methods=["GET", "POST"])
def employee_all_bookings():
    if request.method == "GET":
        cursor, conn = connect_to_db()
        query = "select * from bookings natural join cars"
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)

        bookings=[]
        for i in data:
            dict = {"vid":i[0], "bid":i[1], "cid":i[2], "to":i[3], "from":i[4], "type":i[5], "model":i[6], "np":i[7]}
            bookings.append(dict)

        conn.close()
        return render_template("EmployeeAllBookings.html", bookings=bookings)