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
    query = "select * from Customer where c_id = " + str(c_id)  

    cursor.execute(query)

    data = cursor.fetchone()
    conn.close()

    customers = []

    if(len(data) == 0):
        return False
    else:
        for i in data:
            dict = {"data":True, "id":data[0], "fname":data[1], "lname":data[2],
               "address":data[3], "dob":data[4], "email":data[5]}
            customers.append(dict)
    
    return customers

def get_customer_authentication(c_email):
    cursor, conn = connect_to_db()
    query = "select c_password from Customer where c_email = " + str(c_email)

    cursor.execute(query)

    password = cursor.fetchone()
    conn.close()

    if(len(password)==0):
        return False
    else:
        return password
    
def get_employee_authentication(e_email):
    cursor, conn = connect_to_db()
    query = "select e_password from Employee where e_email = " + str(e_email)
    cursor.execute(query)

    password = cursor.fetchone()
    conn.close()

    if(len(password)==0):
        return False
    else:
        return password
    
def get_driver_authentication(d_email):
    cursor, conn = connect_to_db()
    query = "select d_password from Driver where d_email = " + str(d_email)
    cursor.execute(query)

    password = cursor.fetchone()
    conn.close()

    if(len(password)==0):
        return False
    else:
        return password
    
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

#def register_customer()