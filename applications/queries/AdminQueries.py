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


def get_car_details():

    cursor, conn = connect_to_db()

    query = "SELECT * FROM Car"
    cursor.execute(query)
    data = cursor.fetchall()

    cars = []
    for car in data:
        car_dict = {"id": car[0], "v_type": car[1], "v_model": car[2], "v_numberplate": car[3]}
        cars.append(car_dict)

    conn.close()
    return cars

def insert_car_details(cvid,ctype,cmodel,cnplate):
    
    cursor, conn = connect_to_db()

  
    query = "insert into Car values"
    query += "("+cvid+","+ctype+","+cmodel+","+cnplate+")"
    cursor.execute(query)
    conn.commit()

    conn.close()
    print(query)

def del_car_detail(cvid):
    
    cursor, conn = connect_to_db()

    query = "delete from Car where v_id= " + str(cvid)
    cursor.execute(query)
    conn.commit()
    conn.close()
    print(query)

def get_past_bookings():
    cursor, conn = connect_to_db()

    query = "select * from past_bookings "
    query += " order by b_id"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data

def get_current_bookings():
    cursor, conn = connect_to_db()

    query = "select b.b_id, e_id, from_date, to_date, b_amount, v_type, v_model, v_numberplate, c_fname, c_lname, c_email, d_name, d_email, e_name, e_email "
    query += "from booking b natural join car v natural join customer natural join employee natural join driver left outer join penalties p on b.b_id = p.b_id "
    query += "where active=1"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data

def get_new_bookings():
    cursor, conn = connect_to_db()

    query = "select b.b_id, from_date, to_date, b_amount, v_type, v_model, v_numberplate, c_fname, c_lname, c_email "
    query += "from booking b natural join car v natural join customer left outer join penalties p on b.b_id = p.b_id "
    query += "where active=-1"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()
    return data

def get_employee_month():
        cursor, conn = connect_to_db()

        query = "select e_id,count from "
        query += "(select e_id,count(b_id) "
        query += "from booking where extract(month from from_date)=extract(month from current_date) and (active=0 or active=1) "
        query += "group by extract(month from from_date),e_id) as subquery "
        query += "where count>=all("
        query += "select count(b_id) from booking "
        query += "where extract(month from from_date)=extract(month from current_date) and (active=0 or active=1) "
        query += "group by extract(month from from_date),e_id)"

        cursor.execute(query)

        data = cursor.fetchall()

        e_id = data[0][0]
        cnt = data[0][1]

        conn.close()
        return e_id, cnt

def most_car_model():
    cursor, conn = connect_to_db()

    query = "select v_model from "
    query += "(select v_model,count(b_id) from booking natural join car group by v_model) as subquery "
    query += "where count>=all(select count(b_id) from booking natural join car group by v_model)"

    cursor.execute(query)

    data = cursor.fetchall()

    conn.close()
    return data