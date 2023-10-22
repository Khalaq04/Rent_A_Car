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
        dict = {"id":i[0], "name":i[2]}
        cars.append(dict)

    conn.close()
    return cars

def get_last_bid():

    cursor, conn = connect_to_db()

    query="select max(bid) from bookings"
    cursor.execute(query)
    data=cursor.fetchall()
    print(data[0])

    conn.close()
    return str(data[0][0]+1)

def add_booking(vid, to_place, from_place):
    cursor, conn = connect_to_db()

    bid = get_last_bid()

    query="insert into bookings values ("+bid+ ", 1, "+vid+", '"+to_place+"', '"+from_place+"')"
    cursor.execute(query)
    conn.commit()

    conn.close()
    print(query)

@app.route("/customer/1/home", methods=["GET", "POST"])
def Customerhome_page():
    if(request.method=='GET'):
        info={"id":1, "name":"abc"}
        return render_template('CustomerHomePage.html', info = info)

@app.route("/booking-portal", methods=["GET", "POST"])
def newbooking():
    if(request.method=='GET'):
        cars = get_car_details()
        return render_template('CustomerNewBooking.html', cars=cars)
    else:
        info={"id":1, "name":"abc"}
        cars = get_car_details()
        print(request.form["to"], request.form["from"], request.form["car"])
        add_booking(request.form["car"], request.form["to"], request.form["from"])
        return redirect("/customer/1/home")