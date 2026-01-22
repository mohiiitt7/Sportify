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

def delete_category(id,treeview):
     index=treeview.selection()
     content=treeview.item(index)
     row=content["values"]
     id=row[0]
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
                mycursor.execute("DELETE from category_data WHERE id=%s",id)
                connection.commit()
                treeview_data(treeview)
                messagebox.showinfo("success","Record deleted successfully")
            except Exception as e:
                messagebox.showerror("error",f"error due to {e}")
            finally:
              mycursor.close()
              connection.close()  


def clear_category(id_entry,name_entry,discription_text):
    id_entry.delete(0,END)
    name_entry.delete(0,END)
    
    discription_text.delete(1.0,END)

def treeview_data(treeview):
    mycursor,connection=connect_database()

    if not mycursor or not connection:
            return
    try:
        mycursor.execute("SELECT * from category_data")
        records=mycursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert("",END,values=record)
    except Exception as e:
        messagebox.showerror("error",f"error due to {e}")
    finally:
        mycursor.close()
        connection.close()

def add_category(id,name,descriprion,treeview):
    if id=="" or name=="" or descriprion=="":
        messagebox.showerror("error","All fields are required")
        return
    else:
        mycursor,connection=connect_database()
        if not mycursor or not connection:
            return
        try:
            mycursor.execute("SELECT * from category_data WHERE id=%s",(id,))
            if mycursor.fetchone():
                    messagebox.showerror("error","ID already exists")
                    return
        
            mycursor.execute("INSERT INTO category_data VALUES(%s,%s,%s)",(id,name,descriprion))
            connection.commit()
            messagebox.showinfo("success","Data inserted succesfully")
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror("error",f"error due to {e}")
        finally:
            mycursor.close()
            connection.close()


def category_form(window):
    # Main container
    category_frame = Frame(window, bg=BG_LIGHT)
    category_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Header
    header_frame = Frame(category_frame, bg="white", height=60)
    header_frame.pack(side=TOP, fill=X)
    
    Label(header_frame, text="Manage Categories", font=("Segoe UI", 20, "bold"), 
          bg="white", fg=PRIMARY_BLUE).pack(side=LEFT, padx=30, pady=10)

    # Content Area
    content_area = Frame(category_frame, bg=BG_LIGHT, padx=30, pady=20)
    content_area.pack(fill=BOTH, expand=True)

    # Top Section: Table
    table_section = Frame(content_area, bg="white", padx=20, pady=20)
    table_section.pack(fill=X, pady=(0, 20))

    # Treeview
    tree_frame = Frame(table_section, bg="white")
    tree_frame.pack(fill=X)

    scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
    scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(tree_frame, columns=("id", "name", "description"), 
                            show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.config(command=treeview.yview)
    scroll_x.config(command=treeview.xview)
    treeview.pack(fill=X)

    treeview.heading("id", text="Category ID")
    treeview.heading("name", text="Category Name")
    treeview.heading("description", text="Description")
 
    treeview.column("id", width=100)
    treeview.column("name", width=200)
    treeview.column("description", width=500)

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

    id_entry = create_label_entry(form_section, "Category ID", 0, 0)
    name_entry = create_label_entry(form_section, "Category Name", 0, 1)
    description_text = create_label_entry(form_section, "Description", 1, 0, "text")

    # Action Buttons
    btn_frame = Frame(form_section, bg="white")
    btn_frame.grid(row=2, column=0, columnspan=4, pady=30)

    def action_btn(text, color, cmd):
        Button(btn_frame, text=text, font=("Segoe UI", 11, "bold"), bg=color, fg="white", 
               bd=0, cursor="hand2", width=12, pady=8, command=cmd).pack(side=LEFT, padx=10)

    action_btn("ADD", PRIMARY_BLUE, lambda: add_category(id_entry.get(), name_entry.get(), description_text.get(1.0, END), treeview))
    action_btn("DELETE", "#DC3545", lambda: delete_category(id_entry.get(), treeview))
    action_btn("CLEAR", "#6C757D", lambda: clear_category(id_entry, name_entry, description_text))

    treeview_data(treeview)
    
    return category_frame
