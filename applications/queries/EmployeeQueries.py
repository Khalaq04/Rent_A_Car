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
    query += " order by b_id"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data

def close_booking(b_id, penalty, desc):
    cursor, conn = connect_to_db()

    query = "CALL insert_penalty(" + str(b_id) + "," + str(penalty) + ",'" + str(desc) + "')" 
    cursor.execute(query)
    
    conn.commit()
    conn.close()

def get_employee_new_bookings():
    cursor, conn = connect_to_db()

    query = "select b.b_id, d_id, from_date, to_date, c_fname, c_lname, c_email, b_amount, v_type, v_model, v_numberplate "
    query += "from booking b natural join customer natural join car where active=-1 order by b_id"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data

def get_cars():
    cursor, conn = connect_to_db()

    query = "select v_model from car"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data

def get_drivers():
    cursor, conn = connect_to_db()

    query = "(select d_id, d_name from driver) except (select d_id, d_name from driver where d_id in (select d_id from booking where active=1))"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data

def confirm_booking(b_id, e_id, d_id):
    cursor, conn = connect_to_db()

    if d_id == -1:
        query = "update booking "
        query += "set e_id=" + str(e_id) + ", "
        query += "active=1 "
        query += "where b_id=" + str(b_id)
    else:
        query = "update booking "
        query += "set e_id=" + str(e_id) + ", "
        query += "d_id=" + str(d_id) + ", "
        query += "active=1 "
        query += "where b_id=" + str(b_id)

    cursor.execute(query)

    conn.commit()
    conn.close()

def get_maintainance():
    cursor, conn = connect_to_db()

    query = "select * from car natural join maintainance"
    cursor.execute(query)

    data = cursor.fetchall()
    
    conn.close()
    return data