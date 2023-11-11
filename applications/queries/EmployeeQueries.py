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

def get_employee_details(e_id):
    cursor, conn = connect_to_db()
    query = "select * from Employee where e_id=" + str(e_id)

    cursor.execute(query)
    data = cursor.fetchall()

    query = "select phone from Employee_Phone where e_id=" + str(e_id)
    cursor.execute(query)
    phone = cursor.fetchall()

    detials = {"name":data[0][1], "addr":data[0][2], "dob":data[0][3], "sal":data[0][4], "email":data[0][5]}
    conn.close()
    return detials, phone

# def get_employee_bookings(e_id):
#     cursor, conn = connect_to_db()

#     query = ""