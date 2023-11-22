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

    query = "select * "
    query += "from customer natural join customer_phone "
    query += "where c_id = " + str(c_id)
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    return data
    
def get_car_types():
    cursor, conn = connect_to_db()

    query = "select distinct v_type, vt_amount "
    query += "from car natural join caramount "
    query += "where v_id in( "
    query += "(select v_id "
    query += "from car) "
    query += "except "
    query += "(select v_id "
    query += "from car "
    query += "where v_id in (select v_id "
    query += "from booking "
    query += "where active=1 or active = -1)))"

    cursor.execute(query)

    data = cursor.fetchall()
    return (data)

def get_car_details(v_type):
    cursor, conn = connect_to_db()

    query = "select distinct v_model "
    query += "from car "
    query += "where v_type='"+ v_type +"' and v_id not in ("
    query += "select v_id "
    query += "from booking "
    query += "where active=1 or active=-1)"

    cursor.execute(query)

    data = cursor.fetchall()
    return (data)

def assign_car(carname):
    cursor, conn = connect_to_db()

    query = "select v_id from booking "
    query += "where v_id in (select v_id from car "
    query += "where v_model='" + carname +"') group by v_id "
    query += "having count(b_id) = (select min(mycount) "
    query += "from (select v_id, count(b_id) mycount "
    query += "from booking where v_id in (select v_id "
    query += "from car where v_model='"+ carname +"') group by v_id))"

    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    return (data)

def get_last_bid():

    cursor, conn = connect_to_db()

    query = "select max(b_id) from booking"
    cursor.execute(query)
    data = cursor.fetchall()

    x = 1
    if data[0][0]:
        x = x + data[0][0]

    conn.close()
    return str(x)

def add_booking(cid, fromdate, todate, did, vmodel):
    cursor, conn = connect_to_db()
    bid = get_last_bid()
    query = "CALL insert_new_booking("+bid+","+str(cid)+",'"+str(fromdate)+"','"+str(todate)+"',"+str(did)+",'"+str(vmodel)+"')"
    print(query)
    cursor.execute(query)
    conn.commit()

    conn.close()

def get_past_bookings(c_id):
    cursor, conn = connect_to_db()

    query = "select from_date, to_date, b_amount, amount, d_name, d_email, e_email "
    query += "from booking b natural join driver natural join employee "
    query += "left outer join penalties p on b.b_id=p.b_id "
    query += "where c_id=" + str(c_id) 
    query += " order by from_date"
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data

def get_amount(fromdate, todate, vtype, driver):
    cursor, conn = connect_to_db()

    query = "select get_amount('"+fromdate+"', '"+todate+"', '"+vtype+"', '"+str(driver)+"')" 
    cursor.execute(query)
    data = cursor.fetchall()[0][0]

    conn.close()
    return data

def add_phone(c_id, phone):
    cursor, conn = connect_to_db()

    query = "insert into customer_phone values ("+str(c_id)+","+str(phone)+")"

    cursor.execute(query)
    query = "commit"
    cursor.execute(query)

    conn.close()

def get_cur_bookings(c_id):
    cursor, conn = connect_to_db()

    query = "select from_date, to_date, b_amount, d_name, d_email, e_email "
    query += "from booking b natural join driver natural join employee "
    query += "where active<>0 and c_id=" + str(c_id) 
    query += " order by from_date"
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data