from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import psycopg2
from tkinter import messagebox
from employees import connect_database
import os

# Styling Constants
PRIMARY_BLUE = "#0D6EFD"
SIDEBAR_BLUE = "#00509E"
BG_LIGHT = "#F0F2F5"
TEXT_DARK = "#212529"
CARD_WHITE = "#FFFFFF"

def clear_entry(search_entry,bill_text_widget):
    
    search_entry.delete(0, END)

    
    bill_text_widget.delete("1.0", END)

def search_bill(in_search, listbox, bill_folder, bill_text):
    
    if not in_search:
        messagebox.showinfo("Info", "Please enter a bill number.")
        return

   
    file_name = f"{in_search}.txt"
    file_path = os.path.join(bill_folder, file_name)

    try:
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"No record found for '{file_name}'.")
            return
        
       
        listbox.delete(0, END)
        listbox.insert(END, file_name)

        
        bill_text.delete(1.0, END)
        with open(file_path, "r") as file:
            content = file.read()
            bill_text.insert(END, content)
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {e}")


def sales_form(window):
    def show_file_content(event):
        bill_text.config(state=NORMAL)
        bill_text.delete(1.0, END)
        
        selection = in_list.curselection()
        if selection:
            selected_file = in_list.get(selection[0])
            file_path = os.path.join(bill_folder, selected_file)

            try:
                with open(file_path, "r") as file:
                    content = file.read()
                bill_text.insert(END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open file: {e}")
        bill_text.config(state=DISABLED)

    # Main container
    sales_frame = Frame(window, bg=BG_LIGHT)
    sales_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Header
    header_frame = Frame(sales_frame, bg="white", height=60)
    header_frame.pack(side=TOP, fill=X)
    
    Label(header_frame, text="View Sales Bills", font=("Segoe UI", 20, "bold"), 
          bg="white", fg=PRIMARY_BLUE).pack(side=LEFT, padx=30, pady=10)

    # Content Area
    content_area = Frame(sales_frame, bg=BG_LIGHT, padx=30, pady=20)
    content_area.pack(fill=BOTH, expand=True)

    # Search Section
    search_section = Frame(content_area, bg="white", padx=20, pady=20)
    search_section.pack(fill=X, pady=(0, 20))

    search_frame = Frame(search_section, bg="white")
    search_frame.pack(fill=X)

    Label(search_frame, text="Invoice No.", font=("Segoe UI", 11), bg="white").pack(side=LEFT, padx=(0, 10))
    search_entry = Entry(search_frame, font=("Segoe UI", 11), bg="#F8F9FA", bd=1, width=20)
    search_entry.pack(side=LEFT, padx=(0, 10), ipady=3)

    bill_folder = "bill"

    Button(search_frame, text="Search", font=("Segoe UI", 10, "bold"), bg=PRIMARY_BLUE, fg="white", 
           bd=0, cursor="hand2", width=10, command=lambda: search_bill(search_entry.get().strip(), in_list, bill_folder, bill_text)).pack(side=LEFT, padx=(0, 10))
    
    Button(search_frame, text="Clear", font=("Segoe UI", 10, "bold"), bg="#6C757D", fg="white", 
           bd=0, cursor="hand2", width=10, command=lambda: clear_entry(search_entry, bill_text)).pack(side=LEFT)

    # Bottom Section: List and Bill View
    view_section = Frame(content_area, bg=BG_LIGHT)
    view_section.pack(fill=BOTH, expand=True)

    # Left: Bill List
    list_frame = Frame(view_section, bg="white", padx=20, pady=20)
    list_frame.pack(side=LEFT, fill=Y, padx=(0, 20))
    
    Label(list_frame, text="All Bills", font=("Segoe UI", 12, "bold"), bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    scrollbar = Scrollbar(list_frame, orient="vertical")
    in_list = Listbox(list_frame, font=("Segoe UI", 10), bd=0, bg="#F8F9FA", 
                      highlightthickness=1, highlightbackground="#DEE2E6", 
                      yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    in_list.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=in_list.yview)

    # Right: Bill Preview
    bill_preview_frame = Frame(view_section, bg="white", padx=20, pady=20)
    bill_preview_frame.pack(side=LEFT, fill=BOTH, expand=True)
    
    Label(bill_preview_frame, text="Bill Preview", font=("Segoe UI", 12, "bold"), bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    bill_text = Text(bill_preview_frame, font=("Consolas", 10), wrap="word", bg="#F8F9FA", 
                     bd=0, highlightthickness=1, highlightbackground="#DEE2E6")
    bill_text.pack(fill=BOTH, expand=True)
    bill_text.config(state=DISABLED)

    # Load Bills
    if not os.path.exists(bill_folder):
        os.makedirs(bill_folder)
        
    try:
        files = os.listdir(bill_folder)
        txt_files = [file for file in files if file.endswith(".txt")]
        for txt_file in txt_files:
            in_list.insert(END, txt_file)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading bills: {e}")

    in_list.bind("<<ListboxSelect>>", show_file_content)

    return sales_frame
