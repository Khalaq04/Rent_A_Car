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

def get_car_details():

    cursor, conn = connect_to_db()
    
    query="select * from cars"
    cursor.execute(query)
    data = cursor.fetchall()

    cars=[]
    for i in data:
        dict = {"id":i[0], "type":i[1], "model":i[2], "numberplate":i[3]}
        cars.append(dict)

    return cars

@app.route("/admin/101/home", methods=["GET", "POST"])
def Admin_page():
    if(request.method=='GET'):
        #temp:
        AdminPro = {"Id":101, "name":"Admin1"}
        return render_template('AdminHomePage.html', AdminPro = AdminPro)
    
@app.route("/admin/view-cars")
def viewcars():
    cars = get_car_details()
    return render_template('AdminCarDetails.html', cars=cars)
