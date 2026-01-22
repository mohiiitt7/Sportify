from login import show_login_window
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from employees import employee_form, connect_database
from supplier import supplier_form
from category import category_form
from product import product_form
from sales import sales_form
from tkinter import messagebox
import time
import qrcode
import random
from PIL import ImageTk, Image
import os
from tkinter import simpledialog

# Styling Constants
PRIMARY_BLUE = "#0D6EFD"
SIDEBAR_BLUE = "#00509E"
BG_LIGHT = "#F0F2F5"
TEXT_DARK = "#212529"
CARD_WHITE = "#FFFFFF"
SUCCESS_GREEN = "#198754"
INFO_CYAN = "#0DCAF0"
DANGER_RED = "#DC3545"
WARNING_YELLOW = "#FFC107"





def update_time():
    date_time = time.strftime("%I:%M:%S %p | %A, %B %d, %Y")
    subtitle.config(text=f"Sales Portal  |  {date_time}")
    subtitle.after(1000, update_time)

def clear_fields(pro2_entry, price_entry, quantity_entry, search_entry, name_entry, contact_entry, treeview2, bill_text, amount_button, pay_button):
    initialize_cart()
    print("clear_all called")
    for entry in (pro2_entry, price_entry, quantity_entry, search_entry, name_entry, contact_entry):
        entry.delete(0, 'end')

   
    treeview2.delete(*treeview2.get_children())

   
    bill_text.delete(1.0, 'end')

    
    amount_button.config(text="Total Amount:\n ₹0.00")
    pay_button.config(text="Net Payable:\n ₹0.00")



def generate_bill(name_entry, contact_entry, amount_button, pay_button, bill_text):
   
    
    customer_name = name_entry.get().strip()
    customer_contact = contact_entry.get().strip()

    
    if not customer_name or not customer_contact:
        messagebox.showerror("Error", "Please enter all customer details")
        return

    if not customer_contact.isdigit() or len(customer_contact) != 10:
        messagebox.showerror("Validation Error", "Contact number must be exactly 10 digits and contain only numbers.")
        return

  
    bill_no = random.randint(1000, 9999)

   
    try:
        total_amount = amount_button.cget("text").split("\n")[1][1:] 
        net_pay = pay_button.cget("text").split("\n")[1][1:]  
    except IndexError:
        messagebox.showerror("Error", "Unable to retrieve amount or net pay details.")
        return

    
    bill_content = (
        "==============================\n"
        "            SPORTFY\n"
        "==============================\n"
        f"          BILL NO: {bill_no}\n"
        "==============================\n"
        f"Customer Name: {customer_name}\n"
        f"Contact Number: {customer_contact}\n\n"
        "==============================\n"
        f"Total Amount: ₹{total_amount}\n"
        f"Net Payable: ₹{net_pay}\n"
        "==============================\n"
        "Thank you for shopping with us!\n"
        "==============================\n"
    )

    
    try:
        qr = qrcode.make(f"Bill No: {bill_no}\nTotal: ₹{total_amount}\nNet Payable: ₹{net_pay}")
        qr_path = f"bill_{bill_no}.png"
        qr.save(qr_path)
    except Exception as e:
        messagebox.showerror("Error", f"Error generating QR code: {e}")
        return

   
    bill_text.delete("1.0", "end")  
    bill_text.insert("1.0", bill_content)  

    save_response = messagebox.askyesno("Save Bill", "Do you want to save this bill?")
    if save_response:
               
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        folder_path = os.path.join(desktop_path, "sportify", "bill")
        
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

       
        file_path = os.path.join(folder_path, f"{bill_no}.txt")
        try:
               
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(bill_content)
                messagebox.showinfo("Success", f"Bill saved as {file_path}")
        except Exception as e:
                messagebox.showerror("Error", f"Error saving bill: {e}")

def on_generate_bill_button_click(name_entry, contact_entry, amount_button, pay_button, bill_text):
    """Handle the action when the 'Generate Bill' button is clicked."""
    generate_bill(name_entry, contact_entry, amount_button, pay_button, bill_text)


def calculate_bill(treeview2, amount_button, pay_button):
    """Calculate the total and discounted price."""
    mycursor, connection = connect_database()
    if not mycursor or not connection:
        return
    try:
        # Fetch prices and quantities from the cart_data table
        mycursor.execute("SELECT price, quantity FROM cart_data")
        records = mycursor.fetchall()

        # Handle empty cart case
        if not records:
            amount_button.config(text="Total Amount:\n ₹0.00")
            pay_button.config(text="Net Payable:\n ₹0.00")
            return

        # Calculate total and net payable amount
        total_price = sum(float(price) * int(quantity) for price, quantity in records)
        discount = 10  # 10% discount
        net_pay = total_price - (total_price * discount / 100)

        # Update the button texts
        amount_button.config(text=f"Total Amount:\n ₹{total_price:.2f}")
        pay_button.config(text=f"Net Payable:\n ₹{net_pay:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Error calculating bill: {e}")
    finally:
        mycursor.close()
        connection.close()


def add_customer(name,contact):
    if name=="" or contact=="":
        messagebox.showerror("Error","Please enter all customer details")
    
    if not contact.isdigit() or len(contact) != 10:
        messagebox.showerror("Validation Error", "Contact number must be exactly 10 digits and contain only numbers.")
        return
    
    mycursor,connection=connect_database()
    if not mycursor or not connection:
            return
    try:
            mycursor.execute("INSERT INTO customer_data(name,contact) VALUES(%s,%s)",(name,contact))
            connection.commit()
            messagebox.showinfo("success","Data inserted succesfully")
            
    except Exception as e:
            messagebox.showerror("error",f"error due to {e}")
    finally:
            mycursor.close()
            connection.close()
     

def treeview2_data(treeview2):
    mycursor,connection=connect_database()

    if not mycursor or not connection:
            return
    try:
        mycursor.execute("SELECT * from cart_data")
        records=mycursor.fetchall()
        treeview2.delete(*treeview2.get_children())
        for record in records:
            treeview2.insert("",END,values=record)
    except Exception as e:
        messagebox.showerror("error",f"error due to {e}")
    finally:
        mycursor.close()
        connection.close()

def initialize_cart():
    mycursor, connection = connect_database()
    if not mycursor or not connection:
        return
    try:
        mycursor.execute("TRUNCATE TABLE cart_data")
        connection.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Error initializing cart: {e}")
    finally:
        mycursor.close()
        connection.close()

def add_cart(name, price, quantity, treeview2):
    
    calculate_bill(treeview2, amount_button, pay_button)

    mycursor, connection = connect_database()
    if not mycursor or not connection:
        return
    try:

    
        mycursor.execute("SELECT quantity FROM cart_data WHERE name=%s", (name,))
        product_exists = mycursor.fetchone()

        quantity = int(quantity)
        if product_exists:
            if quantity == 0:
                confirm = messagebox.askyesno("Confirm Delete", "Quantity is 0. Remove product from cart?")
                if confirm:
                    mycursor.execute("DELETE FROM cart_data WHERE name=%s", (name,))
                    connection.commit()
                    messagebox.showinfo("Success", "Product removed from cart successfully!")
                    treeview2_data(treeview2)
                return

            
            mycursor.execute(
                "UPDATE cart_data SET quantity=quantity+%s WHERE name=%s",
                (quantity, name)
            )
        else:
            
            mycursor.execute(
                "INSERT INTO cart_data(name, price, quantity) VALUES(%s, %s, %s)",
                (name, price, quantity)
            )

        connection.commit()  
        treeview2_data(treeview2)
        messagebox.showinfo("Success", "Product added to the cart successfully")

    except Exception as e:
        messagebox.showerror("Error", f"Error adding to cart: {e}")
    finally:
        mycursor.close()
        connection.close()

    
    calculate_bill(treeview2, amount_button, pay_button)


def load_photo(photo_name, photo_label):
    if not photo_name:
        photo_label.config(image='')
        photo_label.image = None
        return
        
    photo_path = os.path.join("sportify/images/products", photo_name)
    if not os.path.exists(photo_path):
        photo_label.config(image='')
        photo_label.image = None
        return
        
    try:
        img = Image.open(photo_path)
        img = img.resize((150, 150), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        photo_label.config(image=img)
        photo_label.image = img
    except Exception as e:
        print(f"Error loading image: {e}")

def clear_data(pro2_entry, price_entry, quantity_entry, treeview, photo_label):
    
    pro2_entry.config(state='normal')  
    pro2_entry.delete(0, END) 
    pro2_entry.config(state='readonly')  

    
    price_entry.config(state='normal')  
    price_entry.delete(0, END)  
    price_entry.config(state='readonly')  

    
    quantity_entry.delete(0, END)
   
    treeview.selection_remove(treeview.selection())
    photo_label.config(image='')
    photo_label.image = None


def select_data(event,pro2_entry,price_entry,quantity_entry,treeview, photo_label):
    index=treeview.selection()
    content=treeview.item(index)
    row=content["values"]
    pro2_entry.config(state='normal')
    pro2_entry.delete(0,END)
    pro2_entry.insert(0,row[1])
    pro2_entry.config(state='readonly')

    price_entry.config(state='normal')
    price_entry.delete(0,END)
    price_entry.insert(0,row[2])
    price_entry.config(state='readonly')

    quantity_entry.delete(0,END)
    
    quantity_entry.insert(0,"1")
    
    if len(row) > 5:
        load_photo(row[5], photo_label)
    else:
        photo_label.config(image='')

def show_all(treeview,search_entry):
    treeview_data(treeview)
    search_entry.delete(0,END)

def search_product(search_entry,treeview):
    if search_entry=="":
        messagebox.showinfo("info","Please enter product name no.")
        return
    else:
        mycursor,connection=connect_database()
        if not mycursor or not connection:
        
                return
        try:
            mycursor.execute("SELECT id, name, price, quantity, status, photo from product_data WHERE name=%s",search_entry)
            record=mycursor.fetchone()
            if not record:
                messagebox.showerror("error", "NO record found")
                return
            treeview.delete(*treeview.get_children())
            treeview.insert("",END,values=record)
        except Exception as e:
                messagebox.showerror("error",f"error due to {e}")
        finally:
              mycursor.close()
              connection.close()  

def treeview_data(treeview):
    mycursor,connection=connect_database()

    if not mycursor or not connection:
            return
    try:
        mycursor.execute("SELECT id, name, price, quantity, status, photo from product_data")
        records=mycursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert("",END,values=record)
    except Exception as e:
        messagebox.showerror("error",f"error due to {e}")
    finally:
        mycursor.close()
        connection.close()

def logout(current_window):
    current_window.destroy()
    show_login_window()

def employee_dashboard():
    global subtitle, amount_button, pay_button
    window = Tk() 
    window.title("Sportify Sales Portal")
    window.geometry("1400x850+0+0")
    window.configure(bg=BG_LIGHT)

    # Header
    header = Frame(window, bg="white", height=70)
    header.pack(fill=X)
    
    Label(header, text="Sportify Sales", font=("Segoe UI", 24, "bold"), bg="white", fg=PRIMARY_BLUE).pack(side=LEFT, padx=30)
    
    subtitle = Label(header, text="Sales Portal", font=("Segoe UI", 12), bg="white", fg=TEXT_DARK)
    subtitle.pack(side=LEFT, padx=30)
    
    Button(header, text="Logout", font=("Segoe UI", 11, "bold"), bg=DANGER_RED, fg="white", 
           bd=0, cursor="hand2", padx=20, pady=5, command=lambda: logout(window)).pack(side=RIGHT, padx=30)

    # Main Area
    main_area = Frame(window, bg=BG_LIGHT, padx=20, pady=20)
    main_area.pack(fill=BOTH, expand=True)

    # Left Column: Products & Search
    left_col = Frame(main_area, bg=BG_LIGHT)
    left_col.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 20))

    # Product Search Card
    prod_search_card = Frame(left_col, bg="white", padx=20, pady=20)
    prod_search_card.pack(fill=X, pady=(0, 20))
    
    Label(prod_search_card, text="Search Products", font=("Segoe UI", 14, "bold"), bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    search_frame = Frame(prod_search_card, bg="white")
    search_frame.pack(fill=X)
    
    search_entry = Entry(search_frame, font=("Segoe UI", 11), bg="#F8F9FA", bd=1)
    search_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10), ipady=3)
    
    Button(search_frame, text="Search", font=("Segoe UI", 10, "bold"), bg=PRIMARY_BLUE, fg="white", 
           bd=0, cursor="hand2", width=10, command=lambda: search_product(search_entry.get(), treeview)).pack(side=LEFT, padx=(0, 5))
    
    Button(search_frame, text="All", font=("Segoe UI", 10, "bold"), bg="#6C757D", fg="white", 
           bd=0, cursor="hand2", width=8, command=lambda: show_all(treeview, search_entry)).pack(side=LEFT)

    # Product Treeview Card
    prod_tree_card = Frame(left_col, bg="white", padx=20, pady=20)
    prod_tree_card.pack(fill=BOTH, expand=True)

    treeview_frame = Frame(prod_tree_card, bg="white")
    treeview_frame.pack(fill=BOTH, expand=True)
    
    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeview_frame, columns=("id", "name", "price", "quantity", "status", "photo"), 
                            show="headings", yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)
    treeview.pack(fill=BOTH, expand=True)

    for col, text in [("id", "ID"), ("name", "Product Name"), ("price", "Price"), ("quantity", "Qty"), ("status", "Status")]:
        treeview.heading(col, text=text)
        treeview.column(col, width=60 if col in ["id", "price", "quantity"] else 120)

    # Middle Column: Cart & Customer
    mid_col = Frame(main_area, bg=BG_LIGHT)
    mid_col.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 20))

    # Customer Card
    cust_card = Frame(mid_col, bg="white", padx=20, pady=20)
    cust_card.pack(fill=X, pady=(0, 20))
    
    Label(cust_card, text="Customer Details", font=("Segoe UI", 14, "bold"), bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    form_f = Frame(cust_card, bg="white")
    form_f.pack(fill=X)
    
    Label(form_f, text="Name", font=("Segoe UI", 10), bg="white").grid(row=0, column=0, sticky="w")
    name_entry = Entry(form_f, font=("Segoe UI", 11), bg="#F8F9FA", bd=1)
    name_entry.grid(row=0, column=1, sticky="we", pady=5)
    
    Label(form_f, text="Contact", font=("Segoe UI", 10), bg="white").grid(row=1, column=0, sticky="w")
    contact_entry = Entry(form_f, font=("Segoe UI", 11), bg="#F8F9FA", bd=1)
    contact_entry.grid(row=1, column=1, sticky="we", pady=5)

    # Cart Card
    cart_card = Frame(mid_col, bg="white", padx=20, pady=20)
    cart_card.pack(fill=BOTH, expand=True)
    
    Label(cart_card, text="Quick Cart", font=("Segoe UI", 14, "bold"), bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    cart_form = Frame(cart_card, bg="white")
    cart_form.pack(fill=X, pady=(0, 15))
    
    def create_cart_ent(parent, label, row, col, readonly=True):
        Label(parent, text=label, font=("Segoe UI", 10), bg="white").grid(row=row, column=col*2, sticky="w", padx=(10 if col>0 else 0, 5))
        ent = Entry(parent, font=("Segoe UI", 11), bg="#F8F9FA", bd=1, width=15)
        if readonly: ent.config(state="readonly")
        ent.grid(row=row, column=col*2+1, sticky="we")
        return ent

    pro2_entry = create_cart_ent(cart_form, "Product", 0, 0)
    price_entry = create_cart_ent(cart_form, "Price", 0, 1)
    quantity_entry = create_cart_ent(cart_form, "Qty", 1, 0, False)
    
    # Photo Label
    photo_preview_frame = Frame(cart_form, bg="#F8F9FA", bd=1, relief=SUNKEN, width=100, height=100)
    photo_preview_frame.grid(row=0, column=4, rowspan=2, padx=10, sticky="ns")
    photo_preview_frame.grid_propagate(False)
    
    photo_label = Label(photo_preview_frame, bg="#F8F9FA")
    photo_label.pack(fill=BOTH, expand=True)
    
    cart_btns = Frame(cart_card, bg="white")
    cart_btns.pack(fill=X, pady=10)
    
    Button(cart_btns, text="Add/Update", font=("Segoe UI", 10, "bold"), bg=SUCCESS_GREEN, fg="white", 
           bd=0, cursor="hand2", pady=8, width=15,
           command=lambda: add_cart(pro2_entry.get(), price_entry.get(), quantity_entry.get(), treeview2)).pack(side=LEFT, padx=(0, 10))
    
    Button(cart_btns, text="Clear", font=("Segoe UI", 10, "bold"), bg="#6C757D", fg="white", 
           bd=0, cursor="hand2", pady=8, width=10,
           command=lambda: clear_data(pro2_entry, price_entry, quantity_entry, treeview, photo_label)).pack(side=LEFT)

    treeview2_frame = Frame(cart_card, bg="white")
    treeview2_frame.pack(fill=BOTH, expand=True, pady=10)
    
    treeview2 = ttk.Treeview(treeview2_frame, columns=("id", "name", "price", "quantity"), 
                             show="headings", height=8)
    treeview2.pack(fill=BOTH, expand=True)
    for col, text in [("id", "ID"), ("name", "Product"), ("price", "Price"), ("quantity", "Qty")]:
        treeview2.heading(col, text=text)
        treeview2.column(col, width=50 if col in ["id", "price", "quantity"] else 120)

    # Right Column: Billing
    right_col = Frame(main_area, bg=BG_LIGHT, width=350)
    right_col.pack(side=RIGHT, fill=Y)

    # Summary Card
    summ_card = Frame(right_col, bg="white", padx=20, pady=20)
    summ_card.pack(side=BOTTOM, fill=X, pady=(20, 0))
    
    amount_button = Button(summ_card, text="Total: ₹0.00", font=("Segoe UI", 11, "bold"), bg=PRIMARY_BLUE, fg="white", bd=0, pady=10)
    amount_button.pack(fill=X, pady=5)
    
    pay_button = Button(summ_card, text="Net Pay: ₹0.00", font=("Segoe UI", 11, "bold"), bg=SUCCESS_GREEN, fg="white", bd=0, pady=10)
    pay_button.pack(fill=X, pady=5)
    
    gen_btn = Button(summ_card, text="Generate Bill", font=("Segoe UI", 12, "bold"), bg="#212529", fg="white", 
                     bd=0, cursor="hand2", pady=15, 
                     command=lambda: generate_bill(name_entry, contact_entry, amount_button, pay_button, bill_text))
    gen_btn.pack(fill=X, pady=(10, 5))
    
    Button(summ_card, text="Clear All", font=("Segoe UI", 10), bg="#6C757D", fg="white", 
           bd=0, cursor="hand2", pady=8, 
           command=lambda: clear_fields(pro2_entry, price_entry, quantity_entry, search_entry, name_entry, contact_entry, treeview2, bill_text, amount_button, pay_button)).pack(fill=X)

    # Bill Card
    bill_card = Frame(right_col, bg="white", padx=20, pady=20)
    bill_card.pack(side=TOP, fill=BOTH, expand=True)
    
    Label(bill_card, text="Billing Area", font=("Segoe UI", 14, "bold"), bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    bill_text = Text(bill_card, font=("Consolas", 10), bg="#F8F9FA", bd=0, 
                     highlightthickness=1, highlightbackground="#DEE2E6")
    bill_text.pack(fill=BOTH, expand=True)

    update_time()
    treeview_data(treeview)
    treeview2_data(treeview2)
    treeview.bind("<ButtonRelease-1>", lambda e: select_data(e, pro2_entry, price_entry, quantity_entry, treeview, photo_label))

    window.mainloop()
