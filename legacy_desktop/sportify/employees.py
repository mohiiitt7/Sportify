from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import psycopg2
from tkinter import messagebox

# Styling Constants
PRIMARY_BLUE = "#0D6EFD"
SIDEBAR_BLUE = "#00509E"
BG_LIGHT = "#F0F2F5"
TEXT_DARK = "#212529"
CARD_WHITE = "#FFFFFF"

def connect_database():
    try:
        # First connect to default postgres database to create sportify18 if needed
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="mohit#2003",
            database="postgres"
        )
        connection.autocommit = True
        mycursor = connection.cursor()
        
        # Create database if it doesn't exist
        mycursor.execute("SELECT 1 FROM pg_database WHERE datname = 'sportify18'")
        if not mycursor.fetchone():
            mycursor.execute("CREATE DATABASE sportify18")
        
        mycursor.close()
        connection.close()
        
        # Now connect to sportify18 database
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="mohit#2003",
            database="sportify18"
        )
        mycursor = connection.cursor()
        
    except Exception as e:
        messagebox.showerror("error", f"Database connectivity issue: {e}")
        return None, None
    
    return mycursor, connection

def treeview_data():
    mycursor,connection=connect_database()
    if not mycursor or not connection:
            return
    try: 
        mycursor.execute("SELECT * from employee_data")
        employee_records=mycursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert("",END,values=record)
    except Exception as e:
        messagebox.showerror("error",f"error due to {e}")
    finally:
        mycursor.close()
        connection.close()

def select_data(event,eid_entry,name_entry,email_entry,gender_combobox,dob_entry,contact_entry,emp_type_combobox,education_combobox,shift_combobox,address_text,doj_entry,salary_entry,usertype_combobox,password_entry):
    index=employee_treeview.selection()
    content=employee_treeview.item(index)
    row=content["values"]
    clear_fields(eid_entry,name_entry,email_entry,gender_combobox,dob_entry,contact_entry,emp_type_combobox,education_combobox,shift_combobox,address_text,doj_entry,salary_entry,usertype_combobox,password_entry,False)
    eid_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    email_entry.insert(0,row[2])
    gender_combobox.set(row[3])
    dob_entry.set_date(row[4])
    contact_entry.insert(0,row[5])
    emp_type_combobox.set(row[6])
    education_combobox.set(row[7])
    shift_combobox.set(row[8])
    address_text.insert(1.0,row[9])
    doj_entry.set_date(row[10])
    salary_entry.insert(0,row[11])
    usertype_combobox.set(row[12])
    password_entry.insert(0,row[13])

def add_employee(eid,name,email,gender,dob,contact,emp_type,education,work_shift,address,doj,salary,userType,password):
    print(eid,name)
    if(eid==""or name=="" or email==""or gender=="Select Gender" or contact=="" or emp_type=="Select Type" or education=="Select Type" or work_shift=="Select Shift" or address=="\n" or salary=="" or userType=="Select Type" or password==""):
        messagebox.showerror("ERROR","All fields are required")

    if not contact.isdigit() or len(contact) != 10:
        messagebox.showerror("ERROR", "Contact must be a 10-digit number")
        return

    # Validate salary: must be digits
    if not salary.isdigit():
        messagebox.showerror("ERROR", "Salary must be a valid number")
        return

    # Validate email: must contain '@'
    if "@" not in email:
        messagebox.showerror("ERROR", "Email must be a valid email address with '@'")
        return

    mycursor,connection=connect_database()
    if not mycursor or not connection:
            return
    try:
            mycursor.execute("SELECT eid from employee_data WHERE eid=%s",(eid))
            if mycursor.fetchone():
                messagebox.showerror("error","ID already exixts")
                return
            address=address.strip()
            mycursor.execute("INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(eid,name,email,gender,dob,contact,emp_type,education,work_shift,address,doj,salary,userType,password))
            connection.commit()
            treeview_data()
            messagebox.showinfo("success","Data inserted succesfully")
    except Exception as e:
            messagebox.showerror("error",f"error due to {e}")
    finally:
            mycursor.close()
            connection.close()

def clear_fields(eid_entry,name_entry,email_entry,gender_combobox,dob_entry, contact_entry,emp_type_combobox,education_combobox,shift_combobox,address_text,doj_entry,salary_entry,usertype_combobox,password_entry,check):
    eid_entry.delete(0,END)
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    from datetime import date
    dob_entry.set_date(date.today())
    gender_combobox.set("Select Gender")
    contact_entry.delete(0,END)
    emp_type_combobox.set("Select Type")
    education_combobox.set("Select Type")
    shift_combobox.set("Select Shift")
    address_text.delete(1.0,END)
    doj_entry.set_date(date.today())
    salary_entry.delete(0,END)
    usertype_combobox.set("Select Type")
    password_entry.delete(0,END)
    if check:

       employee_treeview.selection_remove(employee_treeview.selection())

def update_employee(eid,name,email,gender,dob,contact,emp_type,education,work_shift,address,doj,salary,userType,password):
    selected=employee_treeview.selection()
    if not selected:

        messagebox.showerror("error","NO row is selected")
    else:
        mycursor,connection=connect_database()
        if not mycursor or not connection:
            return
        
        mycursor.execute("SELECT * from employee_data WHERE eid=%s",(eid))
        current_data=mycursor.fetchone()
        current_data=current_data[1:]
        
        address=address.strip()
        new_data=(name,email,gender,dob,contact,emp_type,education,work_shift,address,doj,salary,userType,password)
        
        if current_data==new_data:
            messagebox.showinfo("Info","NO changes made")
            return
        mycursor.execute("UPDATE employee_data SET name=%s,email=%s,gender=%s,dob=%s,contact=%s,emp_type=%s,education=%s,work_shift=%s,address=%s,doj=%s,salary=%s,userType=%s,password=%s WHERE eid=%s",(name,email,gender,dob,contact,emp_type,education,work_shift,address,doj,salary,userType,password,eid))
        connection.commit()
        treeview_data()
        messagebox.showinfo("success","Data updated succesfully")

def delete_employee(eid):
    selected=employee_treeview.selection()
    if not selected:
        messagebox.showerror("Erro","No row is selected")
    else:
        result=messagebox.askyesno("confirm","Do you really want to delete a record?")
        if result:
            mycursor,connection=connect_database()
            if not mycursor or not connection:
                return

            try:                
                mycursor.execute("DELETE FROM employee_data WHERE eid=%s",(eid))
                connection.commit()
                treeview_data()
                messagebox.showinfo("success","Record deleted successfully")
            except Exception as e:
                 messagebox.showerror("error",f"error due to {e}")
            finally:
                 mycursor.close()
                 connection.close()

def search_employee(search_option,value):
    if search_option=="Search By":
        messagebox.showerror("error","No option is selected")
    elif value=="":
        messagebox.showerror("error","Enter value to search")
    else:
        mycursor,connection=connect_database()
        if not mycursor or not connection:
                return
        try:
            mycursor.execute(f"SELECT * from employee_data WHERE {search_option} LIKE %s",f"%{value}%")
            records=mycursor.fetchall()
            if len(records)==0:
                messagebox.showerror("error","NO records found")
                return
            employee_treeview.delete(*employee_treeview.get_children())
            for record in records:
                employee_treeview.insert("",END,value=record)
        except Exception as e:
                 messagebox.showerror("error",f"error due to {e}")
        finally:
                 mycursor.close()
                 connection.close()

def show_all(search_entry,serach_combobox):
    treeview_data()
    search_entry.delete(0,END)
    serach_combobox.set("Search By")

def employee_form(window):
    global employee_treeview
    
    # Main container
    employee_frame = Frame(window, bg=BG_LIGHT)
    employee_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Header
    header_frame = Frame(employee_frame, bg="white", height=60)
    header_frame.pack(side=TOP, fill=X)
    
    Label(header_frame, text="Manage Employees", font=("Segoe UI", 20, "bold"), 
          bg="white", fg=PRIMARY_BLUE).pack(side=LEFT, padx=30, pady=10)

    # Content Area
    content_area = Frame(employee_frame, bg=BG_LIGHT, padx=30, pady=20)
    content_area.pack(fill=BOTH, expand=True)

    # Top Section: Search and Table
    top_section = Frame(content_area, bg="white", padx=20, pady=20)
    top_section.pack(fill=X, pady=(0, 20))

    search_frame = Frame(top_section, bg="white")
    search_frame.pack(fill=X, pady=(0, 15))

    search_combobox = ttk.Combobox(search_frame, values=("eid", "name", "email"), 
                                   font=("Segoe UI", 11), state="readonly")
    search_combobox.pack(side=LEFT, padx=(0, 10))
    search_combobox.set("Search By")

    search_entry = Entry(search_frame, font=("Segoe UI", 11), bg="#F8F9FA", bd=1)
    search_entry.pack(side=LEFT, padx=(0, 10), ipady=3)

    Button(search_frame, text="Search", font=("Segoe UI", 10, "bold"), bg=PRIMARY_BLUE, fg="white", 
           bd=0, cursor="hand2", width=10, command=lambda: search_employee(search_combobox.get(), search_entry.get())).pack(side=LEFT, padx=(0, 10))
    
    Button(search_frame, text="Show All", font=("Segoe UI", 10, "bold"), bg="#6C757D", fg="white", 
           bd=0, cursor="hand2", width=10, command=lambda: show_all(search_entry, search_combobox)).pack(side=LEFT)

    # Treeview with style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

    tree_frame = Frame(top_section, bg="white")
    tree_frame.pack(fill=X)

    scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
    scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)

    employee_treeview = ttk.Treeview(tree_frame, columns=("eid", "name", "email", "gender", "dob", "contact", 
                                                          "emp_type", "education", "work_shift", "address", 
                                                          "doj", "salary", "userType"), 
                                     show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.config(command=employee_treeview.yview)
    scroll_x.config(command=employee_treeview.xview)
    employee_treeview.pack(fill=X)

    # Table Headings
    headings = [("eid", "ID"), ("name", "NAME"), ("email", "Email"), ("gender", "GENDER"), 
                ("dob", "DOB"), ("contact", "CONTACT"), ("emp_type", "EMP TYPE"), 
                ("education", "EDUCATION"), ("work_shift", "SHIFT"), ("address", "ADDRESS"), 
                ("doj", "DOJ"), ("salary", "SALARY"), ("userType", "ROLE")]
    
    for id, text in headings:
        employee_treeview.heading(id, text=text)
        employee_treeview.column(id, width=100 if id != "address" else 200)

    treeview_data()

    # Form Section
    form_section = Frame(content_area, bg="white", padx=30, pady=30)
    form_section.pack(fill=BOTH, expand=True)

    def create_label_entry(parent, text, row, col, type="entry", values=None):
        Label(parent, text=text, font=("Segoe UI", 11), bg="white", fg=TEXT_DARK).grid(row=row, column=col*2, sticky="w", pady=10, padx=(20 if col>0 else 0, 10))
        if type == "entry":
            ent = Entry(parent, font=("Segoe UI", 11), bg="#F8F9FA", bd=1)
            ent.grid(row=row, column=col*2+1, sticky="we", pady=10)
            return ent
        elif type == "combobox":
            cb = ttk.Combobox(parent, values=values, font=("Segoe UI", 11), state="readonly")
            cb.grid(row=row, column=col*2+1, sticky="we", pady=10)
            return cb
        elif type == "date":
            de = DateEntry(parent, font=("Segoe UI", 11), width=18, state="readonly", date_pattern="dd/mm/yy")
            de.grid(row=row, column=col*2+1, sticky="we", pady=10)
            return de
        elif type == "text":
            tx = Text(parent, width=30, height=3, font=("Segoe UI", 11), bg="#F8F9FA", bd=1)
            tx.grid(row=row, column=col*2+1, rowspan=2, sticky="we", pady=10)
            return tx

    eid_entry = create_label_entry(form_section, "Emp ID", 0, 0)
    name_entry = create_label_entry(form_section, "Full Name", 0, 1)
    email_entry = create_label_entry(form_section, "Email Address", 0, 2)

    gender_combobox = create_label_entry(form_section, "Gender", 1, 0, "combobox", ("Male", "Female"))
    dob_entry = create_label_entry(form_section, "Date of Birth", 1, 1, "date")
    contact_entry = create_label_entry(form_section, "Contact No", 1, 2)

    emp_type_combobox = create_label_entry(form_section, "Emp Type", 2, 0, "combobox", ("Full time", "Part time", "Casual", "Contract", "Intern"))
    education_combobox = create_label_entry(form_section, "Education", 2, 1, "combobox", ("B.Tech", "M.Tech", "MCA", "M.Com", "MBA"))
    shift_combobox = create_label_entry(form_section, "Work Shift", 2, 2, "combobox", ("Morning", "Evening", "Night"))

    address_text = create_label_entry(form_section, "Address", 3, 0, "text")
    doj_entry = create_label_entry(form_section, "Joining Date", 3, 1, "date")
    salary_entry = create_label_entry(form_section, "Salary", 3, 2)

    usertype_combobox = create_label_entry(form_section, "User Role", 4, 1, "combobox", ("Admin", "Employee"))
    password_entry = create_label_entry(form_section, "Password", 4, 2)

    # Action Buttons
    btn_frame = Frame(form_section, bg="white")
    btn_frame.grid(row=5, column=0, columnspan=6, pady=30)

    def action_btn(text, color, cmd):
        Button(btn_frame, text=text, font=("Segoe UI", 11, "bold"), bg=color, fg="white", 
               bd=0, cursor="hand2", width=12, pady=8, command=cmd).pack(side=LEFT, padx=10)

    action_btn("ADD", PRIMARY_BLUE, lambda: add_employee(eid_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(), dob_entry.get(), contact_entry.get(), emp_type_combobox.get(), education_combobox.get(), shift_combobox.get(), address_text.get(1.0, END), doj_entry.get(), salary_entry.get(), usertype_combobox.get(), password_entry.get()))
    action_btn("UPDATE", "#FFC107", lambda: update_employee(eid_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(), dob_entry.get(), contact_entry.get(), emp_type_combobox.get(), education_combobox.get(), shift_combobox.get(), address_text.get(1.0, END), doj_entry.get(), salary_entry.get(), usertype_combobox.get(), password_entry.get()))
    action_btn("DELETE", "#DC3545", lambda: delete_employee(eid_entry.get()))
    action_btn("CLEAR", "#6C757D", lambda: clear_fields(eid_entry, name_entry, email_entry, gender_combobox, dob_entry, contact_entry, emp_type_combobox, education_combobox, shift_combobox, address_text, doj_entry, salary_entry, usertype_combobox, password_entry, True))

    employee_treeview.bind("<ButtonRelease-1>", lambda e: select_data(e, eid_entry, name_entry, email_entry, gender_combobox, dob_entry, contact_entry, emp_type_combobox, education_combobox, shift_combobox, address_text, doj_entry, salary_entry, usertype_combobox, password_entry))

    return employee_frame
"""employee_treeview.bind("<ButtonRelease-1>",select_data(event,eid_entry,name_entry,email_entry,gender_combobox,dob_entry,contact_entry,emp_type_combobox,education_combobox,shift_combobox,address_text,doj_entry,salary_entry,usertype_combobox,password_entry))"""
    
    
   