import datetime
import SQL

# Company and Store
########################################################################################

class Company:
    def __init__(self):
        self.list_of_stores = []
        self.dict_of_employees = {}
        self.num_of_employees = 0

    def add_store_to_company(self, store):
        self.list_of_stores.append(store)
        # Replace the in-memory(list_of_stores.append(store)) with an SQL INSERT 

    def add_employee_to_company(self, emp):
        self.dict_of_employees[emp.full_name.lower()] = emp
        self.num_of_employees += 1
        # Replace the in-memory(dict_of_employees[emp.full_name.lower()] = emp) with an SQL INSERT 

class Store:
    def __init__(self, branch, manager, stock, opening_hours):
        self.branch = branch
        self.manager = str(manager)  # Explicitly convert to string to ensure it's a name
        self.stock = stock
        self.opening_hours = opening_hours



    def present_store(self, cur):
        # Fetch the manager’s information
        manager_data = SQL.get_employee_by_name(cur, self.manager)
        if manager_data:
            employee_num, full_name, role, branch, starting_date, hourly_wage, phone_number, email_address, birth_date, image = manager_data[0]
            manager_info = f"{full_name} (Phone: {phone_number}, Email: {email_address})"
        else:
            manager_info = "Manager information not found"

        # Fetch employees specific to this store branch
        employees_in_store = [emp[1] for emp in SQL.get_employees_in_branch(cur, self.branch) if emp[2] == "Worker"]
        store_employees = ", ".join(employees_in_store) if employees_in_store else "No employees"

        # Construct the output string
        print_line = f"B-Side {self.branch} is open at {self.opening_hours}. Branch manager is {manager_info} and the {len(employees_in_store)} employees of this store are:\n{store_employees}"
        return print_line






    def calc_salaries(self):
        all_store_salaries = 0
        for emp in self.manager.employees_under_manager:
            emp_monthly_hours = float(input(f"insert the amount of hours that {emp.full_name} has worked this month: "))
            all_store_salaries += emp.get_salary(emp_monthly_hours)
        manager_monthly_hours = float(input(f"insert the amount of hours that {self.manager.full_name} has worked this month: "))
        all_store_salaries += self.manager.get_salary(manager_monthly_hours)
        return "{:,}".format(all_store_salaries) + " new shekels"

    def change_opening_hours(self, new_opening_hours):
        self.opening_hours = new_opening_hours



# Employee and Manager
########################################################################################


class Employee:
    role = "Worker"

    def __init__(self, full_name, branch, starting_date, hourly_wage, phone_number, email_address, birth_date, image, employee_num):
        self.employee_num = employee_num
        self.full_name = full_name
        self.branch = branch
        self.starting_date = starting_date
        self.hourly_wage = hourly_wage
        self.phone_number = phone_number
        self.email_address = email_address
        self.birth_date = birth_date
        self.image = image


    def present_employee(self):
        print_line = f"Employee number {self.employee_num} is {self.full_name} from branch {self.branch} as {self.role}.\nPhone number is {self.phone_number} and Email is {self.email_address}. \nAdditional Information: \nHourly Wage: {self.hourly_wage} \nStarting date: {self.starting_date} \nBirthday: {self.birth_date} \n \n"
        return print_line




    def get_salary(self, monthly_hours):
        monthly_wage = self.hourly_wage * monthly_hours
        return monthly_wage


    def update_emp(self, new_branch=None, new_hourly_wage=None, new_phone_number=None, new_email_address=None):
        if new_branch is not None:
            self.branch = new_branch
        if new_hourly_wage is not None:
            self.hourly_wage = new_hourly_wage
        if new_phone_number is not None:
            self.phone_number = new_phone_number
        if new_email_address is not None:
            self.email_address = new_email_address
        return("Emp is updated. \n" + self.present_employee())



    def birthday_gift(self): ### HAS BUGS - not finished yet
        pass
        #TBD
        today = datetime.date.today().strftime("%d/%m")
        
        if str(self.birth_date) == str(today):
            print(f"Happy Birthday, {self.full_name}! You get a gift! Choose a vinyl: ")
            emp_bday_choice = input("> ")
            # if emp_bday_choice == in_stock:
            #   print congratz + update stock
            # else -> suggest a different vinyl.
        



    def delete_emp(self, cur, conn): 
        print(f"Are you sure you want to delete {self.full_name} from the data? Reply with yes/no")
        user_answer = input("> ").strip().lower()
        
        if user_answer == "yes":
            SQL.delete_employee_from_db(cur, self.full_name)
            conn.commit() 
            print(f"{self.full_name} has been successfully deleted from the database.")
        else:
            print(f"{self.full_name} was not deleted.")






class Manager(Employee):
    role = "Manager"
    def __init__(self, full_name, branch, starting_date, hourly_wage, phone_number, email_address, birth_date, image, employee_num, employees_under_manager=None):
        super().__init__(full_name, branch, starting_date, hourly_wage, phone_number, email_address, birth_date, image, employee_num)
        if employees_under_manager is None:
            employees_under_manager = []
        self.employees_under_manager = employees_under_manager
        
    def present_employee(self):
        base_info = super().present_employee()
        employees_info = "\n".join([f"- {emp.full_name} ({emp.role})" for emp in self.employees_under_manager])
        return f"{base_info}Employees under management:\n{employees_info}\n"





# Vinyl
########################################################################################


# class Vinyl: #NOT IN MVP
#     def __init__(self, lp_name, artist , size, price, on_sale, limited_edition):
#         self.lp_name = lp_name
#         self.artist = artist
#         self.genre = None
#         self.size = size
#         self.price = price
#         self.on_sale = False
#         self.limited_edition = False
#         self.year_published = None
#         self.rating = None
#         self.image_url = None


    ##### FETCH NOT FOR MVP #####

    
    # def fetch_vinyl_details(self):
    #     modified_artist = self.artist.replace(" ","-").lower()
    #     modified_lp_name = self.lp_name.replace(" ", "-").lower()
    #     url = f"https://rateyourmusic.com/release/album/{modified_artist}/{modified_lp_name}/"

    #     # Fetch the content of the webpage
    #     response = requests.get(url)
    #     webpage = response.content

    #     # Parse the HTML content
    #     soup = BeautifulSoup(webpage, 'html.parser')

    #     image_tag = soup.find('img', {'class': 'cover-art-image'})
    #     self.image_url = image_tag['src'] if image_tag else 'Image not found'

    #     # Extract the user rating
    #     rating_tag = soup.find('span', {'class': 'avg_rating'})
    #     self.rating = rating_tag.get_text().strip() if rating_tag else 'Rating not found'

    #     # Extract the year of release
    #     year_div = soup.find('div', {'class': 'release_pri_infoblock'})
    #     if year_div:
    #         year_tag = year_div.find('span', {'class': 'release_date'})
    #         self.year_published = year_tag.get_text().strip() if year_tag else 'Year not found'
    #     else:
    #         self.year_published = 'Year not found'



    def present_vinyl(self):
        self.fetch_vinyl_details()  # Fetch details before presenting
        print_line = f"The vinyl '{self.lp_name}' by {self.artist} published in {self.year_published}.\n"
        print_line += f"Image URL: {self.image_url}\n" ########### to change phrasing 
        print_line += f"User Rating: {self.rating}\n" ########### to change phrasing 
        print_line += f"Year of Release: {self.year_published}\n" ########### to change phrasing 
        if self.on_sale:
            self.price = self.price * 0.75
            print_line += f"Item is ON SALE, price is: {self.price} after 25% discount.\n"
        if self.limited_edition:
            self.price = self.price * 1.25
            print_line += f"Item is LIMITED EDITION, price is: {self.price}.\n"
        return print_line













