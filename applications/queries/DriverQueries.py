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

def get_driver_details(d_id):
    cursor, conn = connect_to_db()
    query = "select * from Driver where d_id=" + str(d_id)

    cursor.execute(query)
    data = cursor.fetchall()

    query = "select phone from Driver_Phone where d_id=" + str(d_id)
    cursor.execute(query)
    phone = cursor.fetchall()

    detials = {"name":data[0][1], "addr":data[0][2], "dob":data[0][4], "sal":data[0][3], "email":data[0][5]}
    conn.close()
    return detials, phone

def get_upcoming_bookings(d_id):
    cursor, conn = connect_to_db()

    query = "select c_fname, c_lname, c_email, from_date, to_date, v_type, v_model, v_numberplate "
    query += "from booking natural join customer natural join car "
    query += "where d_id=" + str(d_id) + " and active=1"

    cursor.execute(query)

    data = cursor.fetchall()

    conn.close
    return data