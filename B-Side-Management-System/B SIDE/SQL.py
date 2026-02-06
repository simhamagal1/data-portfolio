import sqlite3 as sql
import datetime

def connect_to_db(db_name='bside.db'):
    conn = sql.connect(db_name)  
    cur = conn.cursor()          
    return conn, cur             



def create_table_employees(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS employees(
        employee_num INTEGER PRIMARY KEY,
        full_name TEXT,
        role TEXT,
        branch TEXT,
        starting_date TEXT,
        hourly_wage REAL,
        phone_number TEXT,
        email_address TEXT, 
        birth_date TEXT, 
        image BLOB 
    );""") # Image will not be implemented on MPV

def create_table_stores(cur):
    query = """
    CREATE TABLE IF NOT EXISTS stores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch TEXT NOT NULL,
        manager TEXT NOT NULL,
        stock INTEGER,
        opening_hours TEXT
    )
    """
    cur.execute(query)


def get_employees_in_branch(cur, branch_name):
    query = "SELECT * FROM employees WHERE LOWER(branch) = LOWER(?)"
    cur.execute(query, (branch_name,))
    return cur.fetchall()  # List of employees in the specified branch




def get_all_employees(cur):
    res = cur.execute("SELECT * FROM employees ORDER BY employee_num DESC;")
    rows = res.fetchall()
    return rows


def get_employee_by_name(cur, employee_name):
    values = (employee_name.lower(),)
    res = cur.execute("SELECT * FROM employees WHERE LOWER(full_name) = ?;", values)  # "WHERE LOWER" is for case-insensitive search
    rows = res.fetchall()
    return rows  



def add_employee(cur, conn, full_name, role="Worker", branch="branch", starting_day=None, hourly_wage=0, phone_number="phone_number", email_address="email_address", birth_date="birth_date", image=None, employees_under_manager=None):
    if starting_day is None:
        starting_day = datetime.date.today()  

    # Automatically populate employees under the manager if role is 'Manager'
    if role == "Manager":
        employees_in_branch = get_employees_in_branch(cur, branch)
        employees_under_manager = employees_in_branch if employees_in_branch else []

    stat = """
        INSERT INTO employees (full_name, role, branch, starting_date, hourly_wage, phone_number, email_address, birth_date, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    values = (full_name, role, branch, starting_day, hourly_wage, phone_number, email_address, birth_date, image)
    cur.execute(stat, values)
    conn.commit()


def get_employee_status(cur, full_name): #Checks if an employee exists by full name, Returns their role (Manager \ Worker), if they exist
    query = """
        SELECT role FROM employees 
        WHERE LOWER(full_name) = ?;
    """
    cur.execute(query, (full_name.lower(),))
    result = cur.fetchone()
    if result:
        return True, result[0]  # (Employee exists, Role)
    else:
        return False, None      # (Employee does not exist, No role)




def create_table_vinyls(cur):
    cur.execute("""CREATE TABLE vinyls(
        lp_name TEXT ,
        artist TEXT,
        size TEXT,
        price TEXT,
        on_sale BOOL,
        limited_edition BOOL,   
        image BLOB, 
        rating TEXT,
        year_published TEXT, 
        genre TEXT  
    );""") #to examine if genre could be list


def get_all_vinyls(cur):
    res = cur.execute("SELECT * FROM vinyls ORDER BY lp_name DESC;")
    rows = res.fetchall()
    return rows






def add_store_to_db(cur, branch, manager, stock, opening_hours):
    query = """
    INSERT INTO stores (branch, manager, stock, opening_hours) 
    VALUES (?, ?, ?, ?)
    """
    values = (branch, manager, stock, opening_hours)
    cur.execute(query, values)



def delete_store_from_db(cur, branch_name):
    query = "DELETE FROM stores WHERE LOWER(branch) = LOWER(?)"
    cur.execute(query, (branch_name,))


def delete_employee_from_db(cur, employee_name):
    query = "DELETE FROM employees WHERE LOWER(full_name) = LOWER(?)"
    cur.execute(query, (employee_name,))



def get_all_stores(cur):
    query = "SELECT branch, manager, stock, opening_hours FROM stores"
    cur.execute(query)
    stores = cur.fetchall()
    return stores



def load_stores_from_db(cur):
    from b_side_classes import Store  
    stores_data = get_all_stores(cur)
    stores = []
    for store_data in stores_data:
        branch, manager, stock, opening_hours = store_data
        store = Store(branch, manager, stock, opening_hours) 
        stores.append(store)
    return stores






def get_all_employees(cur):
    query = """
    SELECT employee_num, full_name, role, branch, starting_date, hourly_wage, 
           phone_number, email_address, birth_date, image 
    FROM employees
    """
    cur.execute(query)
    return cur.fetchall()




def load_employees_from_db(cur):
    from b_side_classes import Employee, Manager  # Moved inside the function to avoid circular import
    employees_data = get_all_employees(cur)
    employees_dict = {}
    for emp in employees_data:
        (employee_num, full_name, role, branch, starting_date, hourly_wage,
         phone_number, email_address, birth_date, image) = emp
        
        employee_instance = (Manager if role == "Manager" else Employee)(
            full_name, branch, starting_date, hourly_wage, 
            phone_number, email_address, birth_date, image, employee_num)
        
        employees_dict[full_name.lower()] = employee_instance
    
    return employees_dict

