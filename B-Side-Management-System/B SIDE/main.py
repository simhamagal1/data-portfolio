from b_side_classes import Employee, Manager, Store, Company
import datetime
import SQL; conn, cur = SQL.connect_to_db()

SQL.create_table_employees(cur); SQL.create_table_stores(cur)

# constant values
STOCK_DEFAULT = 50
COMMAND_ADD_WORKER = "add worker"
COMMAND_ADD_STORE = "add store"
COMMAND_PRESENT_STORE = "present store"
COMMAND_PRESENT_EMPLOYEE = "present employee"
COMMAND_PRESENT__ALL_EMPLOYEES = "present all employees"
COMMAND_DEL_EMPLOYEE = "delete employee"
COMMAND_DEL_STORE = "delete store"
COMMAND_ADD_MANAGER = "add manager"







class UserInterface:
    def __init__(self, company):
        self.company = company

    def welcome_print(self):
        print("\nWelcome to B-side BE user helper!\n\n")
        print("Commands:\n")
        ## Note: the "{:<40}{}".format addition is for equal margin\padding 
        print("{:<40}{}".format("Add Store", "To create a new store of B-Side"))   
        print("{:<40}{}".format("Update Store - NOT IN MVP", "To update information about a B-Side store")) ## NOT COMPLETED
        print("{:<40}{}".format("Present Store =?", "To present a store named '?'"))   
        print("{:<40}{}".format("Present all Stores", "To present all of B-Side stores"))       
        print("{:<40}{}".format("Add Worker", "To add a non-manager employee to B-Side team"))    
        print("{:<40}{}".format("Add Manager", "To add a manager to B-Side team"))
        print("{:<40}{}".format("Update Employee - NOT IN MVP", "To update information about an employee")) ## NOT COMPLETED
        print("{:<40}{}".format("Present Employee = ? (Full name)", "To present information about an employee"))    
        print("{:<40}{}".format("Present all Employees", "To present all employees of B-Side"))    
        print("{:<40}{}".format("Delete store = ? (branch name)", "PERMANENTLY deletes a store from the data"))   
        print("{:<40}{}".format("Delete employee = ? (full name)", "PERMANENTLY deletes an employee from the data"))   



    def main_loop(self):
        self.welcome_print()


        while True:
                print()
                command = input("> ").strip().lower()

                if command.startswith(COMMAND_PRESENT_STORE): ## SQL INCLUDED 
                    params = command.split("=")
                    name_of_store = params[1].strip()
                    for store in self.company.list_of_stores:
                        if name_of_store == store.branch.lower():
                            print(store.present_store(cur))
                            break
                    print("Store not found in our company")

                elif command == "present all stores":
                    all_stores = SQL.get_all_stores(cur)
                    if all_stores:
                        for store_data in all_stores:
                            branch, manager_name, stock, opening_hours = store_data
                            store = Store(branch, manager_name, stock, opening_hours)
                            print(store.present_store(cur))  # Print each store’s details
                            print()  # Add a blank line after each store
                    else:
                        print("No stores found.")


                elif command.startswith(COMMAND_PRESENT_EMPLOYEE): ## SQL INCLUDED
                    params = command.split("=")
                    if len(params) > 1:
                        name_of_emp = params[1].strip().lower()
                        employee_list = SQL.get_employee_by_name(cur, name_of_emp)  

                        if employee_list:  
                            for emp in employee_list:
                                employee_num, full_name, role, branch, starting_date, hourly_wage, phone_number, email_address, birth_date, image = emp #SQL methods returns list of tuples (fetchall returns list of tuples) - therefore here we unpack it
                
                                print(f"Employee number {employee_num} is {full_name} from branch {branch} as {role}.")
                                print(f"Phone number is {phone_number} and Email is {email_address}.")
                                print(f"Additional Information: \nHourly Wage: {hourly_wage}\nStarting date: {starting_date}\nBirthday: {birth_date}\n")
                        else:
                            print(f"No employee found with the name {name_of_emp}")
                    else:
                        print("Invalid command format. Use 'present employee = Full Name'.")





                elif command.startswith(COMMAND_PRESENT__ALL_EMPLOYEES):  ## SQL INCLUDED
                    print()
                    employees_to_present = SQL.get_all_employees(cur)  
                    print("\nAll Employees in B-Side:")
                    for emp in employees_to_present:
                        print(f"{emp[1]}     {emp[2]}")  # for name and role






                elif command.startswith(COMMAND_ADD_STORE):
                    name_of_branch = input("Insert the name of the branch: ")
                    name_of_manager = input("Insert the name of the branch manager: ")

                    # Check if the manager exists in the database and get their role
                    employee_exists, role = SQL.get_employee_status(cur, name_of_manager)

                    if employee_exists and role == "Manager":
                        emp_under_manager = [emp for emp in SQL.get_employees_in_branch(cur, name_of_branch) if emp[2] == "Worker"]

                        stock = STOCK_DEFAULT
                        opening_hours = "08:00-18:00, Sunday to Thursday"
                        branch = Store(name_of_branch, name_of_manager, stock, opening_hours)
                        print(f"The store {name_of_branch} is added to B-Side family!")

                        # Insert the store into the database
                        SQL.add_store_to_db(cur, name_of_branch, name_of_manager, stock, opening_hours)
                        conn.commit()  # Commit to save changes permanently

                        self.company.list_of_stores.append(branch)  # Keep this if you also want in-memory tracking
                    elif employee_exists:
                        print(f"The employee '{name_of_manager}' exists but is not a manager.")
                    else:
                        print(f"The manager '{name_of_manager}' does not exist.")











                elif command.startswith(COMMAND_ADD_WORKER): #SQL included -> check "add_employee" in sql.py file
                    name_of_emp = input("Insert the name of the employee: ").lower()
                    name_of_branch = input("Insert the name of the branch: ")
                    starting_day = datetime.date.today()  
                    emp_wage = float(input("Insert the hourly wage of the employee: "))
                    emp_phone = input("Insert the phone number of the employee: ")
                    emp_email = input("Insert the email of the employee: ")
                    emp_bday = input("Insert the birthday of the employee (YYYY-MM-DD): ")
                    emp_image = "image placeholder" #employee pic not for mvp

                    # FOR MVP we assume that 2 employees with the same name is not possible, making the name of the employee as a unique value. In later versions this method is ought to be changed, as irl 2 employees with the same name exactly is actaully resonable 

                    existing_employee = company.dict_of_employees.get(name_of_emp.lower()) #this will get 'None' in case that the new employee has a unique name
                    if existing_employee:
                        print(f"Error: '{name_of_emp}' is already a in the db. and cannot be readded as a worker.")

                    else:

                        employee_data = {
                            "cur": cur,
                            "conn": conn,
                            "full_name": name_of_emp,
                            "role": "Worker",  
                            "branch": name_of_branch,
                            "starting_day": starting_day,
                            "hourly_wage": emp_wage,
                            "phone_number": emp_phone,
                            "email_address": emp_email,
                            "birth_date": emp_bday,
                            "image": emp_image
                        }

                    
                        SQL.add_employee(
                            employee_data["cur"], 
                            employee_data["conn"], 
                            employee_data["full_name"], 
                            role=employee_data["role"], 
                            branch=employee_data["branch"], 
                            starting_day=employee_data["starting_day"], 
                            hourly_wage=employee_data["hourly_wage"], 
                            phone_number=employee_data["phone_number"], 
                            email_address=employee_data["email_address"], 
                            birth_date=employee_data["birth_date"], 
                            image=employee_data["image"]
                        )
                        company.dict_of_employees[name_of_emp.lower()] = employee_data
                        print(f"The worker {name_of_emp} is added to B-Side family!")
                  

                elif command.startswith(COMMAND_ADD_MANAGER): 
                    name_of_emp = input("Insert the name of the manager: ")
                    name_of_branch = input("Insert the name of the branch: ")
                    starting_day = datetime.date.today()
                    emp_wage = float(input("Insert the hourly wage of the manager: "))
                    emp_phone = input("Insert the phone number of the manager: ")
                    emp_email = input("Insert the email of the manager: ")
                    emp_bday = input("Insert the birthday of the manager (YYYY-MM-DD): ")
                    emp_image = "image placeholder"  # Image not needed for MVP

                    manager_data = {
                            "cur": cur,
                            "conn": conn,
                            "full_name": name_of_emp,
                            "role": "Manager",
                            "branch": name_of_branch,
                            "starting_day": starting_day,
                            "hourly_wage": emp_wage,
                            "phone_number": emp_phone,
                            "email_address": emp_email,
                            "birth_date": emp_bday,
                            "image": emp_image
                        }

                    # Adding the manager to the database using SQL.add_employee
                    SQL.add_employee(
                        manager_data["cur"],
                        manager_data["conn"],
                        manager_data["full_name"],
                        role=manager_data["role"],
                        branch=manager_data["branch"],
                        starting_day=manager_data["starting_day"],
                        hourly_wage=manager_data["hourly_wage"],
                        phone_number=manager_data["phone_number"],
                        email_address=manager_data["email_address"],
                        birth_date=manager_data["birth_date"],
                        image=manager_data["image"]
                    )

                    print(f"The manager {name_of_emp} has been added to B-Side.")


                elif command.startswith(COMMAND_DEL_STORE):
                    params = command.split("=")
                    if len(params) > 1:
                        branch_name = params[1].strip()
                        
                        # Confirm deletion
                        confirm = input(f"Are you sure you want to permanently delete the store '{branch_name}'? Type 'yes' to confirm: ").lower()
                        if confirm == 'yes':
                            SQL.delete_store_from_db(cur, branch_name)
                            conn.commit()  # Commit the deletion
                            print(f"The store '{branch_name}' has been deleted from the data.")
                        else:
                            print("Deletion canceled.")
                    else:
                        print("Please specify the branch name to delete. Example: delete store = Branch Name")


                elif command.startswith(COMMAND_DEL_EMPLOYEE):
                    params = command.split("=")
                    if len(params) > 1:
                        employee_name = params[1].strip()
                        
                        # Confirm deletion
                        confirm = input(f"Are you sure you want to permanently delete the employee '{employee_name}'? Type 'yes' to confirm: ").lower()
                        if confirm == 'yes':
                            SQL.delete_employee_from_db(cur, employee_name)
                            conn.commit()  # Commit the deletion
                            print(f"The employee '{employee_name}' has been deleted from the data.")
                        else:
                            print("Deletion canceled.")
                    else:
                        print("Please specify the full name of the employee to delete. Example: delete employee = Full Name")




if __name__ == '__main__':
    conn, cur = SQL.connect_to_db()  # Connect to the database
    SQL.create_table_employees(cur)  # employees table is created

    company = Company()

    # Load stores, employees, and vinyls from the database
    company.list_of_stores = SQL.load_stores_from_db(cur)
    company.dict_of_employees = SQL.load_employees_from_db(cur)
    #company.list_of_vinyls = SQL.load_vinyls_from_db(cur)  NOT FOR MVP

    ui = UserInterface(company)
    ui.main_loop()













