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


def get_veh_details():

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

def insert_car_details(cvid, ctype, cmodel, cnplate):
    cursor, conn = connect_to_db()

    query = "INSERT INTO Car VALUES (%s, %s, %s, %s)"
    values = (cvid, ctype, cmodel, cnplate)

    cursor.execute(query, values)
    conn.commit()

    conn.close()
    print(query)

def del_car_detail(cvid):
    cursor, conn = connect_to_db()

    query = "DELETE FROM Car WHERE v_id = %s"
    values = (cvid,)

    cursor.execute(query, values)
    conn.commit()
    
    conn.close()
    print(query)





