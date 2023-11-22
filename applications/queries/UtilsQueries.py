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
    
def get_customer_authentication(c_email, c_password):
    cursor, conn = connect_to_db()
    query = "select get_customer_authentication('" + c_email + "', '" + c_password + "')"

    cursor.execute(query)

    exists = cursor.fetchall()
    conn.close()

    return exists
    
def get_employee_authentication(e_email, e_password):
    cursor, conn = connect_to_db()
    query = "select get_employee_authentication('" + e_email + "', '" + e_password + "')"
    cursor.execute(query)

    exists = cursor.fetchall()
    conn.close()

    return exists

def get_admin_authentication(e_email, e_password):
    cursor, conn = connect_to_db()
    query = "select get_admin_authentication('" + e_email + "', '" + e_password + "')"
    cursor.execute(query)

    exists = cursor.fetchall()
    conn.close()

    return exists
    
def get_driver_authentication(d_email, d_password):
    cursor, conn = connect_to_db()
    query = "select get_driver_authentication('" + d_email + "', '" + d_password + "')"
    cursor.execute(query)

    exists = cursor.fetchall()
    conn.close()

    return exists

def get_customer_id(c_email):
    cursor, conn = connect_to_db()
    query = "select c_id from customer where c_email = '" + c_email + "'"
    cursor.execute(query)

    c_id = cursor.fetchall()
    conn.close()

    return c_id

def get_employee_id(e_email):
    cursor, conn = connect_to_db()
    query = "select e_id from employee where e_email = '" + e_email + "'"
    cursor.execute(query)

    e_id = cursor.fetchall()
    conn.close()

    return e_id[0][0]

def get_driver_id(e_email):
    cursor, conn = connect_to_db()
    query = "select d_id from driver where d_email = '" + e_email + "'"
    cursor.execute(query)

    e_id = cursor.fetchall()
    conn.close()

    return e_id[0][0]

def get_last_customer_id():
    cursor, conn = connect_to_db()
    query = "select max(c_id) from customer"
    cursor.execute(query)

    x = 0
    if cursor.fetchall()[0][0]:
        x = x + int(cursor.fetchall()[0][0])

    c_id = x + 1

    conn.close()
    return c_id

def register_customer(fname, lname, phone, addr, dob, email, psw):
    cursor, conn = connect_to_db()

    cid = get_last_customer_id()

    query = "insert into customer values ("+str(cid)+",'"+fname+"','"+lname+"','"+addr+"','"+dob+"','"+email+"','"+psw+"')"
    cursor.execute(query)

    query = "insert into customer_phone("+str(cid)+", "+phone+")"
    cursor.execute(query)
    
    conn.close()