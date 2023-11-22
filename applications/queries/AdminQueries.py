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
    query += "("+cvid+",'"+ctype+"','"+cmodel+"','"+cnplate+"')"
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

def get_veh_details():

    cursor, conn = connect_to_db()
    
    cursor.callproc('get_all_car_details')  # process to call  PL/SQL function

    result = cursor.fetchall()

    cars = []
    for car in result:
        car_dict = {"id": car[0], "v_type": car[1], "v_model": car[2], "v_numberplate": car[3], "nt":car[4]}
        cars.append(car_dict)

    conn.commit()

    conn.close()

    return cars

def employee_action(action,eid,ename,eaddress,edob,esalary,eemail,epassword):
    

    cursor, conn = connect_to_db()

    print(action)

    cursor.callproc('perform_employee_action', (action, eid, ename, eaddress, edob, esalary, eemail, epassword))

    conn.commit()

    conn.close()

def update_emp(eid, ename, eaddress,edob,esalary, eemail, epassword):
    cursor, conn = connect_to_db()

    set_det = []

    if ename:
        set_det.append(f"e_name = '{ename}'")

    if eaddress:
        set_det.append(f"e_address = '{eaddress}'")
    if esalary:
        set_det.append(f"e_salary = '{esalary}'")
    if edob:
        set_det.append(f"e_dob = '{edob}'")
    if eemail:
        set_det.append(f"e_email = '{eemail}'")

    if epassword:
        set_det.append(f"e_password = '{epassword}'")

    
    if set_det:
        set_final = ', '.join(set_det) if set_det else ''

        query = f"UPDATE Employee SET {set_final} WHERE e_id = {eid}"

        cursor.execute(query)
        conn.commit()


    conn.close()

def get_emp_details():

    cursor, conn = connect_to_db()
    
    query = "SELECT * FROM Employee order by e_id"
    cursor.execute(query)
    emp = cursor.fetchall()

    emps = []
    for e in emp:
        emp_dict = {"e_id": e[0], "e_name": e[1], "e_address": e[2],"e_dob": e[3], 
                         "e_salary": e[4], "e_email": e[5],"e_password": e[6]}
        emps.append(emp_dict)


    conn.commit()

    conn.close()
    return emps

def get_driver_details():

    cursor, conn = connect_to_db()
    
    query = "select d.d_id, d_name, d_address, d_salary, d_dob, d_email, d_password, d_license, count(b_id) as number_of_trips from driver d left outer join booking b on d.d_id=b.d_id  where d.d_id <> -1 group by d.d_id order by d.d_id"
    cursor.execute(query)
    driver = cursor.fetchall()

    drivers = []
    for dri in driver:
        dri_dict = {"d_id": dri[0], "d_name": dri[1], "d_address": dri[2],"d_salary": dri[3], 
                         "d_dob": dri[4], "d_email": dri[5],"d_password": dri[6],"d_license":dri[7], "d_cnt":dri[8]}
        drivers.append(dri_dict)

    print(drivers)

    conn.commit()

    conn.close()
    return drivers

def update_driver(did, dname, daddress, dsalary, ddob, demail, dpassword, dlicense):
    cursor, conn = connect_to_db()

    set_dri = []

    if dname:
        set_dri.append(f"d_name = '{dname}'")

    if daddress:
        set_dri.append(f"d_address = '{daddress}'")

    if dsalary:
        set_dri.append(f"d_salary = {dsalary}")

    if ddob:
        set_dri.append(f"d_dob = '{ddob}'")

    if demail:
        set_dri.append(f"d_email = '{demail}'")

    if dpassword:
        set_dri.append(f"d_password = '{dpassword}'")

    if dlicense:
        set_dri.append(f"d_license = '{dlicense}'")


    set_fin = ', '.join(set_dri) if set_dri else ''

    query = f"UPDATE Driver SET {set_fin} WHERE d_id = {did}"

    cursor.execute(query)
    conn.commit()

    conn.close()
    print(query)

def driver_action(action, did, dname, daddress, dsalary, ddob, demail, dpassword, dlicense):
    cursor, conn = connect_to_db()

    cursor.callproc('driver_action', (action, did, dname, daddress, dsalary, ddob, demail, dpassword, dlicense))

    conn.commit()

    conn.close()

def dcontact(id,phone):
    cursor, conn = connect_to_db()

    query = "Insert into Driver_Phone Values(%s,%s)"
    values=(id,phone)

    cursor.execute(query,values)
    conn.commit()
    conn.close()

def customer_contact(fname):

    cursor, conn = connect_to_db()

    query = f"SELECT phone FROM Customer_Phone cp JOIN Customer c ON cp.c_id = c.c_id WHERE c.c_fname = '{fname}'"
    cursor.execute(query)

    phone_numbers = cursor.fetchall()

    phone_numbers_list = []
    for phone in phone_numbers:
        phone_numbers_list.append(phone[0])

    conn.commit()
    conn.close()
    return phone_numbers_list

def emp_contact(e_name):

    cursor, conn = connect_to_db()

    query = f"SELECT phone FROM Employee_Phone ep JOIN Employee e ON ep.e_id = e.e_id WHERE e.e_name = '{e_name}'"
    cursor.execute(query)

    pnums = cursor.fetchall()

    numlist = []
    for ph in pnums :
        numlist.append(ph[0])

    conn.commit()
    conn.close()
    return numlist

def driver_contact(d_name):

    cursor, conn = connect_to_db()

    query = f"SELECT phone FROM Driver_Phone dp JOIN Driver d ON dp.d_id = d.d_id WHERE d.d_name = '{d_name}'"
    cursor.execute(query)

    phone = cursor.fetchall()

    plist = []
    for num in phone:
        plist.append(num[0])

    conn.commit()
    conn.close()
    return plist

def get_customer_details():
    cursor, conn = connect_to_db()

    query = "SELECT * FROM Customer"
    cursor.execute(query)
    customers = cursor.fetchall()

    customer_details = []

    for customer in customers:
        cdict = {"c_id": customer[0],"c_fname": customer[1],"c_lname": customer[2],
            "c_address": customer[3],"c_dob": customer[4],"c_email": customer[5],"c_password": customer[6]}
        
        customer_details.append(cdict)

    conn.commit()
    conn.close()
    return customer_details

def emp_phone_in(eid,ephone):
    cursor, conn = connect_to_db()

    query = "INSERT INTO Employee_Phone VALUES(%s,%s)"
    values = (eid,ephone)

    cursor.execute(query,values)
    conn.commit()

    conn.close()
    print(query)

def del_ephone(ephone):

    cursor, conn = connect_to_db()

    query = "DELETE FROM Employee_Phone WHERE phone=%s"
    values = (ephone,)

    cursor.execute(query,values)
    conn.commit()

    conn.close()
    print(query)

def dri_phone_in(did,dphone):
    cursor, conn = connect_to_db()

    query = "INSERT INTO Driver_Phone VALUES(%s,%s)"
    values = (did,dphone)

    cursor.execute(query,values)
    conn.commit()

    conn.close()
    print(query)

def del_dphone(dphone):

    cursor, conn = connect_to_db()

    query = "DELETE FROM Driver_Phone WHERE phone=%s"
    values = (dphone,)

    cursor.execute(query,values)
    conn.commit()

    conn.close()
    print(query)

def get_car_types():
        cursor, conn = connect_to_db()
        query = "select v_type from caramount"
        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()
        return data

def get_caramount():
    cursor, conn = connect_to_db()
    query = "select * from caramount"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def insert_type(v_type, v_amt):
        cursor, conn = connect_to_db()
        query = "insert into caramount values('" + v_type + "'," + str(v_amt) + ")"
        cursor.execute(query)
        conn.commit()
        conn.close()

def del_type(v_type):
    cursor, conn = connect_to_db()
    query = "delete from caramount where v_type=" + v_type
    cursor.execute(query)
    conn.commit()
    conn.close()