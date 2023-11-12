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