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

    query = "select distinct v_type "
    query += "from car "
    query += "where v_model in( "
    query += "(select v_model "
    query += "from car) "
    query += "except "
    query += "(select v_model "
    query += "from car "
    query += "where v_id in (select v_id "
    query += "from booking "
    query += "where active=1 or active = -1)))"

    cursor.execute(query)

    data = cursor.fetchall()
    return (data)

def get_car_details(v_type):
    cursor, conn = connect_to_db()

    query = "select v_model "
    query += "from car "
    query += "where v_type = '" + v_type + "'"

    cursor.execute(query)

    data = cursor.fetchall()
    return (data)

def get_last_bid():

    cursor, conn = connect_to_db()

    query = "select max(bid) from bookings"
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return str(data[0][0]+1)

def add_booking(vid, to_date, from_date):
    cursor, conn = connect_to_db()

    bid = get_last_bid()

    query="insert into bookings values "
    query += "("+bid+ ", 1, "+vid+", '"+to_date+"', '"+from_date+"')"
    cursor.execute(query)
    conn.commit()

    conn.close()
    print(query)

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