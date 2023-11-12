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

def get_customer_details(c_id):
    cursor, conn = connect_to_db()

    query = "select * from customer natural join customer_phone where c_id = " + str(c_id)
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    return data
    
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

def add_booking(vid, to_date, from_date):
    cursor, conn = connect_to_db()

    bid = get_last_bid()

    query="insert into bookings values ("+bid+ ", 1, "+vid+", '"+to_date+"', '"+from_date+"')"
    cursor.execute(query)
    conn.commit()

    conn.close()
    print(query)

def get_past_bookings(c_id):
    cursor, conn = connect_to_db()

    query = "select from_date, to_date, b_amount, amount, d_name, d_email, e_email from booking natural join penalties natural join driver natural join employee where c_id=" + str(c_id)
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data