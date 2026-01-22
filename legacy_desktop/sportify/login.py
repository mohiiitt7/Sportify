from tkinter import *
from tkinter import messagebox
import dashboard 
import emp_dashboard  
from employees import connect_database
from PIL import ImageTk
import os
import psycopg2

def create_gradient(canvas, width, height, color1, color2):
    """Draw a vertical gradient from color1 to color2"""
    r1, g1, b1 = login_window.winfo_rgb(color1)
    r2, g2, b2 = login_window.winfo_rgb(color2)
    
    r_ratio = float(r2 - r1) / height
    g_ratio = float(g2 - g1) / height
    b_ratio = float(b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
        canvas.create_line(0, i, width, i, fill=color)

def show_login_window():
    global email_entry, password_entry, login_window
    login_window = Tk()
    login_window.title("Sportify Login")
    # Make the window full screen (maximized)
    login_window.state('zoomed')
    
    # Get screen width and height
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    
    # Create Canvas for Gradient Background
    canvas = Canvas(login_window, width=screen_width, height=screen_height, highlightthickness=0)
    canvas.pack(fill=BOTH, expand=True)
    
    # Draw Gradient (Blue #0D6EFD to White #FFFFFF)
    create_gradient(canvas, screen_width, screen_height, "#0D6EFD", "#FFFFFF")

    # Main Center Frame (Transparent effect using canvas window)
    # Note: Tkinter doesn't support true transparency. We fake it or place on top.
    
    # Login Card (White box with shadow effect)
    card_shadow = Frame(canvas, bg="#ced4da", padx=2, pady=2)
    card_shadow.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    card_frame = Frame(card_shadow, bg="white", padx=40, pady=40)
    card_frame.pack()

    # Header
    login_header = Label(card_frame, text="LOG IN", font=("Segoe UI", 28, "bold"), bg="white", fg="#0D6EFD")
    login_header.pack(pady=(0, 30))

    # Username Label & Entry
    email_label = Label(card_frame, text="Username", font=("Segoe UI", 12, "bold"), bg="white", fg="#495057")
    email_label.pack(anchor="w", pady=(0, 5))
    
    email_container = Frame(card_frame, bg="#F0F2F5", padx=10, pady=8, bd=1, relief=FLAT)
    email_container.pack(fill=X, pady=(0, 20))
    email_entry = Entry(email_container, font=("Segoe UI", 12), bg="#F0F2F5", bd=0, width=35)
    email_entry.pack(fill=X)
    email_entry.focus()

    # Password Label & Entry
    password_label = Label(card_frame, text="Password", font=("Segoe UI", 12, "bold"), bg="white", fg="#495057")
    password_label.pack(anchor="w", pady=(0, 5))
    
    pass_container = Frame(card_frame, bg="#F0F2F5", padx=10, pady=8, bd=1, relief=FLAT)
    pass_container.pack(fill=X, pady=(0, 30))
    password_entry = Entry(pass_container, font=("Segoe UI", 12), bg="#F0F2F5", bd=0, show="●", width=35)
    password_entry.pack(fill=X)

    # Login Button
    login_btn = Button(card_frame, text="SIGN IN", font=("Segoe UI", 12, "bold"), bg="#0D6EFD", fg="white", 
                       activebackground="#0b5ed7", activeforeground="white", bd=0, cursor="hand2", 
                       padx=20, pady=12, command=login)
    login_btn.pack(fill=X, ipady=3)
    
    # Footer Text
    Label(card_frame, text="Sportify Inventory System", font=("Segoe UI", 9), bg="white", fg="#adb5bd").pack(pady=(20, 0))

    login_window.mainloop()

def login():
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if email == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    # Check if it's the hardcoded admin
    if email == "mohit07@gmail.com" and password == "mohit123":
        messagebox.showinfo("Login Success", "Welcome Admin!")
        login_window.destroy()
        dashboard.admin_dashboard()
        return

    mycursor, connection = connect_database()
    if not mycursor or not connection:
        return

    try:
        # Check in database
        mycursor.execute("SELECT * FROM employee_data WHERE email = %s AND password = %s", (email, password))
        employee = mycursor.fetchone()

        if employee:
            messagebox.showinfo("Login Success", f"Welcome {employee[1]}!")
            login_window.destroy()
            emp_dashboard.employee_dashboard()
        else:
            messagebox.showerror("Login Failed", "Incorrect Email or Password")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        mycursor.close()
        connection.close()

def init_db_on_startup():
    """Ensure database and tables exist at startup"""
    try:
        # Initial connection to ensure database exists
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="mohit#2003",
            database="postgres"
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'sportify18'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE sportify18")
        cursor.close()
        connection.close()

        # Connect to sportify18 and run schema if needed
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="mohit#2003",
            database="sportify18"
        )
        cursor = connection.cursor()
        
        # Simple check for employee_data table
        cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'employee_data'")
        if not cursor.fetchone():
            schema_found = False
            # Check relative to sportify directory
            for path in ["database/schema.sql", "../database/schema.sql"]:
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        cursor.execute(f.read())
                    connection.commit()
                    schema_found = True
                    break
        
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Database Initialization Error: {e}")

if __name__ == "__main__":
    init_db_on_startup()
    show_login_window()