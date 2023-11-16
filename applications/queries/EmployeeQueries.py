import psycopg2

# new = -1
# current = 1
# past = 0

def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="CarRental",
        user="CarRental",
        password="CarRental"
    )
    cursor = conn.cursor()
    conn.autocommit = True
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

def get_employee_past_bookings(e_id):
    cursor, conn = connect_to_db()

    query = "select * from e_past_bookings "
    query += "where e_id="+str(e_id)
    query += " order by b_id"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data

def get_employee_current_bookings(e_id):
    cursor, conn = connect_to_db()

    query = "select b.b_id, e_id, from_date, to_date, b_amount, v_type, v_model, v_numberplate, c_fname, c_lname, c_email, d_name, d_email "
    query += "from booking b natural join car v natural join customer natural join driver where active=1 and e_id=" + str(e_id)
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data

def close_booking(b_id, penalty, desc):
    cursor, conn = connect_to_db()

    query = "insert into penalties values(" + str(b_id) + ",'" + str(desc) + "'," + str(penalty) + ")" 
    cursor.execute(query)

    conn.commit()
    conn.close()