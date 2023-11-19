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
    
    cursor.callproc('get_all_car_details')  # process to call  PL/SQL function

    result = cursor.fetchall()

    cars = []
    for car in result:
        car_dict = {"id": car[0], "v_type": car[1], "v_model": car[2], "v_numberplate": car[3]}
        cars.append(car_dict)

    conn.commit()

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

def show_panalties():

    cursor, conn = connect_to_db()

    query = "SELECT * FROM Penalties"
    cursor.execute(query)

    panal_data = cursor.fetchall()

    penal=[]

    for i in panal_data:
        dict= {"bid":i[0],"desc":i[1],"amt":i[2]}
        penal.append(dict)

    conn.commit()

    conn.close()
    return penal

def employee_action(action,eid,ename,eaddress,edob,esalary,eemail,epassword):
    

    cursor, conn = connect_to_db()

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

    
    set_final = ', '.join(set_det) if set_det else ''

    query = f"UPDATE Employee SET {set_final} WHERE e_id = {eid}"

    cursor.execute(query)
    conn.commit()


    conn.close()
    print(query)


    


def get_emp_details():

    cursor, conn = connect_to_db()
    
    query = "SELECT * FROM Employee"
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


def get_ephone_det():

    cursor, conn = connect_to_db()

    query = "Select e_name,phone from employee natural join employee_phone where employee.e_id = employee_phone.e_id;"

    cursor.execute(query)
    phone = cursor.fetchall()

    nums=[]
    for p in phone:
        pdict = {"e_name":p[0],"phone":p[1]}
        nums.append(pdict)
    
    conn.commit()
    conn.close()
    return nums

def get_driver_details():

    cursor, conn = connect_to_db()
    
    query = "SELECT * FROM Driver"
    cursor.execute(query)
    driver = cursor.fetchall()

    drivers = []
    for dri in driver:
        dri_dict = {"d_id": dri[0], "d_name": dri[1], "d_address": dri[2],"d_salary": dri[3], 
                         "d_dob": dri[4], "d_email": dri[5],"d_password": dri[6],"d_license":dri[7]}
        drivers.append(dri_dict)


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

def dcontact(id,phone):
    cursor, conn = connect_to_db()

    query = "Insert into Driver_Phone Values(%s,%s)"
    values=(id,phone)

    cursor.execute(query,values)
    conn.commit()
    conn.close()
    print(query)

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



