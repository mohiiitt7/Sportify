from tkinter import *
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
import psycopg2
from tkinter import messagebox
from employees import connect_database
from PIL import Image, ImageTk
import shutil
import os

# Styling Constants
PRIMARY_BLUE = "#0D6EFD"
SIDEBAR_BLUE = "#00509E"
BG_LIGHT = "#F0F2F5"
TEXT_DARK = "#212529"
CARD_WHITE = "#FFFFFF"

def show_product(treeview,search_entry,serach_combobox):
    treeview_data(treeview)
    search_entry.delete(0,END)
    serach_combobox.set("Search By")


def search_product(search_option,value):
    if search_option=="Search By":
        messagebox.showerror("error","No option is selected")
    elif value=="":
        messagebox.showerror("error","Enter value to search")
    else:
        mycursor,connection=connect_database()
        if not mycursor or not connection:
                return
        try:
            mycursor.execute(f"SELECT * from product_data WHERE {search_option} LIKE %s",f"%{value}%")
            records=mycursor.fetchall()
            if len(records)==0:
                messagebox.showerror("error","NO records found")
                return
            treeview.delete(*treeview.get_children())
            for record in records:
                treeview.insert("",END,value=record)
        except Exception as e:
                 messagebox.showerror("error",f"error due to {e}")
        finally:
                 mycursor.close()
                 connection.close()


def clear_data(category_combobox, supplier_combobox, name_entry, price_entry, dis_count, quantity_entry, status_combobox, photo_label, treeview):
    category_combobox.set("Select Category")
    supplier_combobox.set("Select Supplier")
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    dis_count.delete(0, END)
    quantity_entry.delete(0, END)
    status_combobox.set("Select Status")
    photo_label.config(image='')
    photo_label.image = None
    photo_label.path = ""
    treeview.selection_remove(treeview.selection())



def delete_product(name,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror("error","NO row is selected")
        return
    else:
        result=messagebox.askyesno("confirm","Do you really want to delete a record?")
        if result:
            mycursor,connection=connect_database()
            if not mycursor or not connection:
                return
            try:
                mycursor.execute("DELETE from product_data WHERE name=%s",name)
                connection.commit()
                treeview_data(treeview)
                messagebox.showinfo("success","Record deleted successfully")
                clear_data(name,treeview)
            except Exception as e:
                messagebox.showerror("error",f"error due to {e}")
            finally:
              mycursor.close()
              connection.close()  


def update_product(category, supplier, name, price, discount, quantity, status, photo_path, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror("error", "No row is selected")
        return
        
    dict_data = treeview.item(index)
    content = dict_data["values"]
    id = content[0]

    # Image Saving Logic
    final_photo_name = photo_path
    if photo_path:
        dest_dir = "sportify/images/products"
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        if os.path.exists(photo_path):
            filename = os.path.basename(photo_path)
            dest_path = os.path.join(dest_dir, filename)
            try:
                if os.path.abspath(photo_path) != os.path.abspath(dest_path):
                    shutil.copy(photo_path, dest_path)
                final_photo_name = filename
            except Exception as e:
                messagebox.showerror("error", f"Error saving image: {e}")
                return

    mycursor, connection = connect_database()
    if not mycursor or not connection:
        return
    try:
        # Fetch current data for comparison
        mycursor.execute("SELECT category, supplier, name, price, discount, quantity, status, photo from product_data WHERE id=%s", (id,))
        current_data = mycursor.fetchone()
        
        # Format current data for comparison (decimal/int conversion)
        current_data = list(current_data)
        current_data[3] = str(current_data[3]) # price
        current_data[4] = str(current_data[4]) # discount
        current_data[5] = int(current_data[5]) # quantity
        
        new_data = [category, supplier, name, price, int(discount), int(quantity), status, final_photo_name]
        
        if list(current_data) == new_data:
            messagebox.showinfo("info", "No changes made")
            return
            
        discounted_price = round(float(price) * (1 - int(discount) / 100), 2)
        mycursor.execute("""
            UPDATE product_data 
            SET category=%s, supplier=%s, name=%s, price=%s, discount=%s, discounted_price=%s, quantity=%s, status=%s, photo=%s 
            WHERE id=%s
        """, (category, supplier, name, price, discount, discounted_price, quantity, status, final_photo_name, id))
        
        connection.commit()
        messagebox.showinfo("success", "Data updated successfully")
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror("error", f"Error: {e}")
    finally:
        mycursor.close()
        connection.close()

def select_data(event, treeview, category_combobox, supplier_combobox, name_entry, price_entry, dis_count, quantity_entry, status_combobox, photo_label):
    index = treeview.selection()
    if not index: return
    content = treeview.item(index)
    row = content["values"]
    
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    dis_count.delete(0, END)
    
    category_combobox.set(row[1])
    supplier_combobox.set(row[2])
    name_entry.insert(0, row[3])
    price_entry.insert(0, row[4])
    dis_count.insert(0, row[5])
    quantity_entry.insert(0, row[7])
    status_combobox.set(row[8])
    
    photo_name = row[9]
    if photo_name:
        load_photo(photo_name, photo_label)

def load_photo(photo_name, photo_label):
    photo_path = os.path.join("sportify/images/products", photo_name)
    if not os.path.exists(photo_path):
        photo_label.config(image='')
        photo_label.path = ""
        return
        
    try:
        img = Image.open(photo_path)
        img = img.resize((120, 120), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        photo_label.config(image=img)
        photo_label.image = img
        photo_label.path = photo_name
    except Exception as e:
        print(f"Error loading image: {e}")

def browse_photo(photo_label):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        filename = os.path.basename(file_path)
        # In a real app, we'd copy the file to the products directory
        # For simplicity, we just store the filename
        load_photo_from_path(file_path, photo_label)
        photo_label.path = file_path # Store full path temporarily until saved

def load_photo_from_path(file_path, photo_label):
    try:
        img = Image.open(file_path)
        img = img.resize((120, 120), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        photo_label.config(image=img)
        photo_label.image = img
    except Exception as e:
        messagebox.showerror("Error", f"Could not load image: {e}")

def treeview_data(treeview):
    mycursor,connection=connect_database()

    if not mycursor or not connection:
            return
    try:
        mycursor.execute("SELECT * from product_data")
        records=mycursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert("",END,values=record)
    except Exception as e:
        messagebox.showerror("error",f"error due to {e}")
    finally:
        mycursor.close()
        connection.close()

def fetch_supplier_category(category_combobox,supplier_combobox):
    category_option=[]
    supplier_option=[]
    mycursor,connection=connect_database()
    if not mycursor or not connection:
        return
    mycursor.execute("SELECT name from category_data")
    names=mycursor.fetchall()
    for name in names:
        category_option.append(name[0])
    category_combobox.config(values=category_option)

    mycursor.execute("SELECT name from supplier_data")
    names2=mycursor.fetchall()
    for name2 in names2:
        supplier_option.append(name2[0])
    supplier_combobox.config(values=supplier_option)


def add_product(category, supplier, name, price, discount, quantity, status, photo_path, treeview):
    if category == "Select Category" or supplier == "Select Supplier" or name == "" or price == "" or quantity == "" or status == "Select Status":
        messagebox.showerror("error", "All fields are required")
        return

    if not quantity.isdigit():
        messagebox.showerror("error", "Quantity must be a valid number")
        return

    try:
        price = float(price)
    except ValueError:
        messagebox.showerror("error", "Price must be a valid number")
        return

    # Image Saving Logic
    final_photo_name = ""
    if photo_path:
        dest_dir = "sportify/images/products"
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        if os.path.exists(photo_path):
            filename = os.path.basename(photo_path)
            dest_path = os.path.join(dest_dir, filename)
            try:
                if os.path.abspath(photo_path) != os.path.abspath(dest_path):
                    shutil.copy(photo_path, dest_path)
                final_photo_name = filename
            except Exception as e:
                messagebox.showerror("error", f"Error saving image: {e}")
                return
        else:
             # If path doesn't exist as absolute, maybe it's already a filename (though unlikely for new add)
             final_photo_name = photo_path

    mycursor, connection = connect_database()
    if not mycursor or not connection:
        return 
    try:
        mycursor.execute("SELECT * from product_data WHERE name=%s", (name,))
        if mycursor.fetchone():
            messagebox.showerror("error", "Product ALREADY exists")
            return
            
        discounted_price = round(float(price) * (1 - int(discount) / 100), 2)
        mycursor.execute("""
            INSERT INTO product_data(category, supplier, name, price, discount, discounted_price, quantity, status, photo)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (category, supplier, name, price, discount, discounted_price, quantity, status, final_photo_name))
        
        connection.commit()
        messagebox.showinfo("success", "Data inserted successfully")
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror("error", f"Error: {e}")
    finally:
        mycursor.close()
        connection.close()

def product_form(window):
    # Main container
    product_frame = Frame(window, bg=BG_LIGHT)
    product_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Header
    header_frame = Frame(product_frame, bg="white", height=60)
    header_frame.pack(side=TOP, fill=X)
    
    Label(header_frame, text="Manage Products", font=("Segoe UI", 20, "bold"), 
          bg="white", fg=PRIMARY_BLUE).pack(side=LEFT, padx=30, pady=10)

    # Content Area
    content_area = Frame(product_frame, bg=BG_LIGHT, padx=30, pady=20)
    content_area.pack(fill=BOTH, expand=True)

    # Top Section: Search and Table
    top_section = Frame(content_area, bg="white", padx=20, pady=10)
    top_section.pack(fill=X, pady=(0, 10))

    search_frame = Frame(top_section, bg="white")
    search_frame.pack(fill=X, pady=(0, 5))

    search_combobox = ttk.Combobox(search_frame, values=("Category", "name", "supplier", "status"), 
                                   font=("Segoe UI", 11), state="readonly")
    search_combobox.pack(side=LEFT, padx=(0, 10))
    search_combobox.set("Search By")

    search_entry = Entry(search_frame, font=("Segoe UI", 11), bg="#F8F9FA", bd=1)
    search_entry.pack(side=LEFT, padx=(0, 10), ipady=3)

    Button(search_frame, text="Search", font=("Segoe UI", 10, "bold"), bg=PRIMARY_BLUE, fg="white", 
           bd=0, cursor="hand2", width=10, command=lambda: search_product(search_combobox.get(), search_entry.get())).pack(side=LEFT, padx=(0, 10))
    
    Button(search_frame, text="Show All", font=("Segoe UI", 10, "bold"), bg="#6C757D", fg="white", 
           bd=0, cursor="hand2", width=10, command=lambda: show_product(treeview, search_entry, search_combobox)).pack(side=LEFT)

    # Treeview
    tree_frame = Frame(top_section, bg="white")
    tree_frame.pack(fill=X)

    scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
    scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(tree_frame, columns=("id", "category", "supplier", "name", "price", "discount", "discounted_price", "quantity", "status"), 
                            show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=6)
    
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.config(command=treeview.yview)
    scroll_x.config(command=treeview.xview)
    treeview.pack(fill=X)

    # Table Headings
    headings = [("id", "ID"), ("category", "Category"), ("supplier", "Supplier"), 
                ("name", "Product Name"), ("price", "Price"), ("discount", "Disc(%)"), 
                ("discounted_price", "Disc Price"), ("quantity", "Qty"), ("status", "Status")]
    
    for id, text in headings:
        treeview.heading(id, text=text)
        treeview.column(id, width=80 if id in ["id", "discount", "quantity"] else 120)

    treeview_data(treeview)

    # Form Section
    form_section = Frame(content_area, bg="white", padx=20, pady=10)
    form_section.pack(fill=BOTH, expand=True)

    def create_label_entry(parent, text, row, col, type="entry", values=None):
        Label(parent, text=text, font=("Segoe UI", 11), bg="white", fg=TEXT_DARK).grid(row=row, column=col*2, sticky="w", pady=5, padx=(10 if col>0 else 0, 5))
        if type == "entry":
            ent = Entry(parent, font=("Segoe UI", 11), bg="#F8F9FA", bd=1)
            ent.grid(row=row, column=col*2+1, sticky="we", pady=5)
            return ent
        elif type == "combobox":
            cb = ttk.Combobox(parent, values=values, font=("Segoe UI", 11), state="readonly")
            cb.grid(row=row, column=col*2+1, sticky="we", pady=5)
            return cb
        elif type == "spinbox":
            sb = Spinbox(parent, from_=0, to=100, font=("Segoe UI", 11), bd=1)
            sb.grid(row=row, column=col*2+1, sticky="we", pady=5)
            return sb

    category_combobox = create_label_entry(form_section, "Category", 0, 0, "combobox")
    supplier_combobox = create_label_entry(form_section, "Supplier", 0, 1, "combobox")
    name_entry = create_label_entry(form_section, "Product Name", 0, 2)

    price_entry = create_label_entry(form_section, "Price", 1, 0)
    dis_count = create_label_entry(form_section, "Discount (%)", 1, 1, "spinbox")
    quantity_entry = create_label_entry(form_section, "Quantity", 1, 2)

    status_combobox = create_label_entry(form_section, "Status", 2, 0, "combobox", ("Active", "Inactive"))

    # Photo Section
    Label(form_section, text="Product Photo", font=("Segoe UI", 11), bg="white", fg=TEXT_DARK).grid(row=2, column=2, sticky="w", pady=5, padx=(10, 5))
    photo_preview_frame = Frame(form_section, bg="#F8F9FA", bd=1, relief=SUNKEN, width=120, height=120)
    photo_preview_frame.grid(row=2, column=3, rowspan=2, sticky="nw", pady=5)
    photo_preview_frame.grid_propagate(False)
    
    photo_label = Label(photo_preview_frame, bg="#F8F9FA")
    photo_label.pack(fill=BOTH, expand=True)
    photo_label.path = ""

    Button(form_section, text="Browse Photo", font=("Segoe UI", 10), bg=PRIMARY_BLUE, fg="white", 
           bd=0, cursor="hand2", command=lambda: browse_photo(photo_label)).grid(row=3, column=2, sticky="nw", padx=(10, 5), pady=(0, 10))

    # Action Buttons
    btn_frame = Frame(form_section, bg="white")
    btn_frame.grid(row=4, column=0, columnspan=6, pady=30)

    def action_btn(text, color, cmd):
        Button(btn_frame, text=text, font=("Segoe UI", 11, "bold"), bg=color, fg="white", 
               bd=0, cursor="hand2", width=12, pady=8, command=cmd).pack(side=LEFT, padx=10)

    action_btn("ADD", PRIMARY_BLUE, lambda: add_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), dis_count.get(), quantity_entry.get(), status_combobox.get(), photo_label.path, treeview))
    action_btn("UPDATE", "#FFC107", lambda: update_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), dis_count.get(), quantity_entry.get(), status_combobox.get(), treeview)) # Need to update update_product too
    action_btn("DELETE", "#DC3545", lambda: delete_product(name_entry.get(), treeview))
    action_btn("CLEAR", "#6C757D", lambda: clear_data(category_combobox, supplier_combobox, name_entry, price_entry, dis_count, quantity_entry, status_combobox, photo_label, treeview))

    fetch_supplier_category(category_combobox, supplier_combobox)
    treeview.bind("<ButtonRelease-1>", lambda e: select_data(e, treeview, category_combobox, supplier_combobox, name_entry, price_entry, dis_count, quantity_entry, status_combobox, photo_label))

    return product_frame
