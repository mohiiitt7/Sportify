from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import psycopg2
from tkinter import messagebox
from employees import connect_database

# Styling Constants
PRIMARY_BLUE = "#0D6EFD"
SIDEBAR_BLUE = "#00509E"
BG_LIGHT = "#F0F2F5"
TEXT_DARK = "#212529"
CARD_WHITE = "#FFFFFF"

def show_all(treeview,in_entry):
    treeview_data(treeview)
    in_entry.delete(0,END)


def clear_supplier(invoice_entry,name_entry,contact_entry,discription_text,treeview):
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    discription_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())

def search_supplier(in_search,treeview):
    if in_search=="":
        messagebox.showinfo("info","Please enter invoice no.")
        return
    else:
        mycursor,connection=connect_database()
        if not mycursor or not connection:
        
                return
        try:
            mycursor.execute("SELECT * from supplier_data WHERE invoice=%s",in_search)
            record=mycursor.fetchone()
            if not record:
                messagebox.showerror("error","NO record found")
                return
            treeview.delete(*treeview.get_children())
            treeview.insert("",END,values=record)
        except Exception as e:
                messagebox.showerror("error",f"error due to {e}")
        finally:
              mycursor.close()
              connection.close()  

def delete_supplier(invoice,treeview):
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
                mycursor.execute("DELETE from supplier_data WHERE invoice=%s",invoice)
                connection.commit()
                treeview_data(treeview)
                messagebox.showinfo("success","Record deleted successfully")
            except Exception as e:
                messagebox.showerror("error",f"error due to {e}")
            finally:
              mycursor.close()
              connection.close()  

def update_supplier(invoice,name,contact,discription,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror("error","NO row is selected")
        return
    else:
        mycursor,connection=connect_database()
        if not mycursor or not connection:
            return
        try:
            mycursor.execute("SELECT * from supplier_data WHERE invoice=%s",(invoice))
            current_data=mycursor.fetchone()
            current_data=current_data[1:]
            
            new_data=(name,contact,discription)
            if new_data==current_data:
                messagebox.showinfo("info","No changes made")
                return

            mycursor.execute("UPDATE supplier_data SET name=%s,contact=%s,discription=%s WHERE invoice=%s",(name,contact,discription,invoice))
            connection.commit()
            messagebox.showinfo("success","Data updated successfully")
            treeview_data(treeview)
        except Exception as e:
           messagebox.showerror("error",f"error due to {e}")
        finally:
           mycursor.close()
           connection.close()

def select_data(event,invoice_entry,name_entry,contact_entry,discription_text,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    row=content["values"]
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    discription_text.delete(1.0,END)
    invoice_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    contact_entry.insert(0,row[2])
    discription_text.insert(1.0,row[3])



def treeview_data(treeview):
    mycursor,connection=connect_database()

    if not mycursor or not connection:
            return
    try:
        mycursor.execute("SELECT * from supplier_data")
        records=mycursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert("",END,values=record)
    except Exception as e:
        messagebox.showerror("error",f"error due to {e}")
    finally:
        mycursor.close()
        connection.close()
        
def add_supplier(invoice,name,contact,discription,treeview):
    if invoice=="" or name=="" or contact=="" or discription=="":
        messagebox.showerror("Error","All fields are required")
    
    if not contact.isdigit() or len(contact) != 10:
        messagebox.showerror("Validation Error", "Contact number must be exactly 10 digits and contain only numbers.")
        return
    


    mycursor,connection=connect_database()
    if not mycursor or not connection:
            return
    try:
            mycursor.execute("SELECT * from supplier_data WHERE invoice=%s",(invoice,))
            if mycursor.fetchone():
                messagebox.showerror("error","ID already exists")
                return
            mycursor.execute("INSERT INTO supplier_data VALUES(%s,%s,%s,%s)",(invoice,name,contact,discription))
            connection.commit()
            messagebox.showinfo("success","Data inserted succesfully")
            treeview_data(treeview)
    except Exception as e:
            messagebox.showerror("error",f"error due to {e}")
    finally:
            mycursor.close()
            connection.close()
def supplier_form(window):
    # Main container
    suplier_frame = Frame(window, bg=BG_LIGHT)
    suplier_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Header
    header_frame = Frame(suplier_frame, bg="white", height=60)
    header_frame.pack(side=TOP, fill=X)
    
    Label(header_frame, text="Manage Suppliers", font=("Segoe UI", 20, "bold"), 
          bg="white", fg=PRIMARY_BLUE).pack(side=LEFT, padx=30, pady=10)

    # Content Area
    content_area = Frame(suplier_frame, bg=BG_LIGHT, padx=30, pady=20)
    content_area.pack(fill=BOTH, expand=True)

    # Top Section: Search and Table
    search_section = Frame(content_area, bg="white", padx=20, pady=20)
    search_section.pack(fill=X, pady=(0, 20))

    search_frame = Frame(search_section, bg="white")
    search_frame.pack(fill=X, pady=(0, 15))

    Label(search_frame, text="Invoice No.", font=("Segoe UI", 11), bg="white").pack(side=LEFT, padx=(0, 10))
    in_entry = Entry(search_frame, font=("Segoe UI", 11), bg="#F8F9FA", bd=1, width=15)
    in_entry.pack(side=LEFT, padx=(0, 10), ipady=3)

    Button(search_frame, text="Search", font=("Segoe UI", 10, "bold"), bg=PRIMARY_BLUE, fg="white", 
           bd=0, cursor="hand2", width=10, command=lambda: search_supplier(in_entry.get(), treeview)).pack(side=LEFT, padx=(0, 10))
    
    Button(search_frame, text="Show All", font=("Segoe UI", 10, "bold"), bg="#6C757D", fg="white", 
           bd=0, cursor="hand2", width=10, command=lambda: show_all(treeview, in_entry)).pack(side=LEFT)

    # Treeview
    tree_frame = Frame(search_section, bg="white")
    tree_frame.pack(fill=X)

    scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
    scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(tree_frame, columns=("invoice", "name", "contact", "description"), 
                            show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.config(command=treeview.yview)
    scroll_x.config(command=treeview.xview)
    treeview.pack(fill=X)

    treeview.heading("invoice", text="Invoice ID")
    treeview.heading("name", text="Name")
    treeview.heading("contact", text="Contact")
    treeview.heading("description", text="Description")
 
    treeview.column("invoice", width=100)
    treeview.column("name", width=200)
    treeview.column("contact", width=150)
    treeview.column("description", width=400)

    # Form Section
    form_section = Frame(content_area, bg="white", padx=30, pady=30)
    form_section.pack(fill=BOTH, expand=True)

    def create_label_entry(parent, text, row, col, type="entry"):
        Label(parent, text=text, font=("Segoe UI", 11), bg="white", fg=TEXT_DARK).grid(row=row, column=col*2, sticky="w", pady=10, padx=(20 if col>0 else 0, 10))
        if type == "entry":
            ent = Entry(parent, font=("Segoe UI", 11), bg="#F8F9FA", bd=1, width=30)
            ent.grid(row=row, column=col*2+1, sticky="we", pady=10)
            return ent
        elif type == "text":
            tx = Text(parent, width=30, height=4, font=("Segoe UI", 11), bg="#F8F9FA", bd=1)
            tx.grid(row=row, column=col*2+1, sticky="we", pady=10)
            return tx

    invoice_entry = create_label_entry(form_section, "Invoice No.", 0, 0)
    name_entry = create_label_entry(form_section, "Supplier Name", 0, 1)
    contact_entry = create_label_entry(form_section, "Contact No.", 1, 0)
    description_text = create_label_entry(form_section, "Description", 1, 1, "text")

    # Action Buttons
    btn_frame = Frame(form_section, bg="white")
    btn_frame.grid(row=2, column=0, columnspan=4, pady=30)

    def action_btn(text, color, cmd):
        Button(btn_frame, text=text, font=("Segoe UI", 11, "bold"), bg=color, fg="white", 
               bd=0, cursor="hand2", width=12, pady=8, command=cmd).pack(side=LEFT, padx=10)

    action_btn("ADD", PRIMARY_BLUE, lambda: add_supplier(invoice_entry.get(), name_entry.get(), contact_entry.get(), description_text.get(1.0, END).strip(), treeview))
    action_btn("UPDATE", "#FFC107", lambda: update_supplier(invoice_entry.get(), name_entry.get(), contact_entry.get(), description_text.get(1.0, END).strip(), treeview))
    action_btn("DELETE", "#DC3545", lambda: delete_supplier(invoice_entry.get(), treeview))
    action_btn("CLEAR", "#6C757D", lambda: clear_supplier(invoice_entry, name_entry, contact_entry, description_text, treeview))

    treeview_data(treeview)
    treeview.bind("<ButtonRelease-1>", lambda e: select_data(e, invoice_entry, name_entry, contact_entry, description_text, treeview))
    
    return suplier_frame
