from tkinter import *
from tkinter import ttk
from employees import employee_form
from supplier import supplier_form
from category import category_form
from product import product_form
from sales import sales_form
from employees import connect_database
from customer import customer_form
from tkinter import messagebox
import time

# Styling Constants
PRIMARY_BLUE = "#0D6EFD"
SIDEBAR_BLUE = "#00509E"
BG_LIGHT = "#F0F2F5"
TEXT_DARK = "#212529"
CARD_WHITE = "#FFFFFF"

def update_time():
    try:
        mycursor, connection = connect_database()
        if not mycursor or not connection:
            return
        
        mycursor.execute("SELECT COUNT(*) from employee_data")
        emp_count_Label.config(text=str(mycursor.fetchone()[0]))

        mycursor.execute("SELECT COUNT(*) from supplier_data")
        sup_count_Label.config(text=str(mycursor.fetchone()[0]))

        mycursor.execute("SELECT COUNT(*) from category_data")
        cat_count_Label.config(text=str(mycursor.fetchone()[0]))

        mycursor.execute("SELECT COUNT(*) from product_data")
        prod_count_Label.config(text=str(mycursor.fetchone()[0]))

        mycursor.execute("SELECT COUNT(*) from customer_data")
        sales_count_Label.config(text=str(mycursor.fetchone()[0]))

        date_time = time.strftime("%I:%M:%S %p | %A, %B %d, %Y")
        subtitle.config(text=f"Admin Portal  |  {date_time}")
        subtitle.after(1000, update_time)
        
        mycursor.close()
        connection.close()
    except Exception as e:
        print(f"Update Time Error: {e}")

def tax_window():
    def save_tax():
        value = tax_count.get()
        mycursor, connection = connect_database()
        if not mycursor or not connection:
            return
        try:
            mycursor.execute("SELECT * from tax_data WHERE id=1")
            if mycursor.fetchone():
                mycursor.execute("UPDATE tax_data SET tax=%s WHERE id=1", (value,))
            else:
                mycursor.execute("INSERT INTO tax_data (id, tax) VALUES(1, %s)", (value,))
            connection.commit()
            messagebox.showinfo("Success", f"Tax is set to {value}% and saved successfully", parent=tax_w)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving tax: {e}")
        finally:
            mycursor.close()
            connection.close()

    tax_w = Toplevel()
    tax_w.title("Tax Settings")
    tax_w.geometry("350x250")
    tax_w.configure(bg="white")
    tax_w.grab_set()
    
    Label(tax_w, text="Tax Configuration", font=("Segoe UI", 16, "bold"), bg="white", fg=PRIMARY_BLUE).pack(pady=20)
    Label(tax_w, text="Enter Tax Percentage (%)", font=("Segoe UI", 12), bg="white").pack(pady=5)
    
    tax_count = Spinbox(tax_w, from_=0, to=100, font=("Segoe UI", 14), width=10, bd=2, relief=RIDGE)
    tax_count.pack(pady=10)

    Button(tax_w, text="SAVE SETTINGS", command=save_tax, font=("Segoe UI", 12, "bold"), 
           bg=PRIMARY_BLUE, fg="white", bd=0, padx=20, pady=10, cursor="hand2").pack(pady=20)

current_frame = None

def show_form(from_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    # Create the form in the content_area
    current_frame = from_function(content_area)

def logout(current_window):
    current_window.destroy()
    from login import show_login_window
    show_login_window()

def admin_dashboard():
    global emp_count_Label, sup_count_Label, cat_count_Label, prod_count_Label, window, subtitle, sales_count_Label, content_area
    
    window = Tk()
    window.title("Sportify Admin Dashboard")
    window.geometry("1340x800+0+0")
    window.configure(bg=BG_LIGHT)

    # Sidebar
    sidebar = Frame(window, bg=SIDEBAR_BLUE, width=280)
    sidebar.pack(side=LEFT, fill=Y)

    # Logo / Title in Sidebar
    Label(sidebar, text="Dashboard", font=("Segoe UI", 24, "bold"), bg=SIDEBAR_BLUE, fg="white", pady=30).pack()

    # Sidebar Buttons
    def nav_btn(text, icon_path, cmd):
        btn = Button(sidebar, text=f"  {text}", font=("Segoe UI", 14), bg=SIDEBAR_BLUE, fg="white",
                     activebackground=PRIMARY_BLUE, activeforeground="white", bd=0, anchor="w",
                     padx=30, pady=15, cursor="hand2", command=cmd)
        btn.pack(fill=X)
        return btn

    nav_btn("Dashboard", None, lambda: show_form(lambda w: create_dashboard_view(w)))
    nav_btn("Employees", None, lambda: show_form(employee_form))
    nav_btn("Suppliers", None, lambda: show_form(supplier_form))
    nav_btn("Categories", None, lambda: show_form(category_form))
    nav_btn("Products", None, lambda: show_form(product_form))
    nav_btn("Sales", None, lambda: show_form(sales_form))
    nav_btn("Customers", None, lambda: show_form(customer_form))
    nav_btn("Tax Settings", None, tax_window)
    
    Button(sidebar, text="  Logout", font=("Segoe UI", 14), bg=SIDEBAR_BLUE, fg="white",
           activebackground="#DC3545", activeforeground="white", bd=0, anchor="w",
           padx=30, pady=15, cursor="hand2", command=lambda: logout(window)).pack(side=BOTTOM, fill=X)

    # Main Area
    main_area = Frame(window, bg=BG_LIGHT)
    main_area.pack(side=RIGHT, fill=BOTH, expand=True)

    # Header in Main Area
    header = Frame(main_area, bg="white", height=70, bd=0)
    header.pack(fill=X)
    
    subtitle = Label(header, text="Welcome Admin", font=("Segoe UI", 12), bg="white", fg=TEXT_DARK)
    subtitle.pack(side=LEFT, padx=30)

    # Content Area
    content_area = Frame(main_area, bg=BG_LIGHT)
    content_area.pack(fill=BOTH, expand=True, padx=30, pady=30)

    def create_dashboard_view(parent):
        global emp_count_Label, sup_count_Label, cat_count_Label, prod_count_Label, sales_count_Label
        
        view = Frame(parent, bg=BG_LIGHT)
        view.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        Label(view, text="Overview", font=("Segoe UI", 24, "bold"), bg=BG_LIGHT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
        
        # Stats Grid
        stats_frame = Frame(view, bg=BG_LIGHT)
        stats_frame.pack(fill=X)

        def create_stat_card(parent, title, color):
            card = Frame(parent, bg="white", bd=0, padx=20, pady=20)
            card.pack(side=LEFT, expand=True, fill=BOTH, padx=10)
            
            Label(card, text=title, font=("Segoe UI", 12), bg="white", fg=TEXT_DARK).pack(anchor="w")
            count_label = Label(card, text="0", font=("Segoe UI", 32, "bold"), bg="white", fg=color)
            count_label.pack(anchor="w", pady=(10, 0))
            return count_label

        emp_count_Label = create_stat_card(stats_frame, "Total Employees", "#745c97")
        sup_count_Label = create_stat_card(stats_frame, "Total Suppliers", "#e0ac00")
        cat_count_Label = create_stat_card(stats_frame, "Total Categories", "#ff4365")
        prod_count_Label = create_stat_card(stats_frame, "Total Products", "#17a398")
        sales_count_Label = create_stat_card(stats_frame, "Total Customers", "#e75a23")

        # Quick Links
        Label(view, text="Quick Links", font=("Segoe UI", 18, "bold"), bg=BG_LIGHT, fg=TEXT_DARK).pack(anchor="w", pady=(40, 20))
        
        links_frame = Frame(view, bg=BG_LIGHT)
        links_frame.pack(fill=X)

        def quick_link(parent, text, cmd):
            btn = Button(parent, text=text, font=("Segoe UI", 12, "bold"), bg=PRIMARY_BLUE, fg="white",
                         activebackground=SIDEBAR_BLUE, activeforeground="white", bd=0, width=15, pady=10, 
                         cursor="hand2", command=cmd)
            btn.pack(side=LEFT, padx=10)

        quick_link(links_frame, "Add Product", lambda: show_form(product_form))
        quick_link(links_frame, "Manage Sales", lambda: show_form(sales_form))
        quick_link(links_frame, "View Employees", lambda: show_form(employee_form))
        quick_link(links_frame, "Add Supplier", lambda: show_form(supplier_form))

        return view

    # Initialize Dashboard View
    current_frame = create_dashboard_view(content_area)
    update_time()

    window.mainloop()

if __name__ == "__main__":
    admin_dashboard()