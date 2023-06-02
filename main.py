from tkinter import *
import sqlite3

root = Tk()
root.title("Address Book")
root.iconbitmap("icon.ico")

conn = sqlite3.connect("address_book.db")
c = conn.cursor()

# Functions
def submit():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
              { 
                "f_name" : f_name.get(),
                "l_name" : l_name.get(),
                "address" : address.get(),
                "city" : city.get(),
                "state" : state.get(),
                "zipcode" : zipcode.get()
              }         
            )
    conn.commit()
    conn.close()
    
    f_name.delete(0,END)
    l_name.delete(0,END)
    address.delete(0,END)
    city.delete(0,END)
    state.delete(0,END)
    zipcode.delete(0,END)

def delete():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()
    c.execute("DELETE from addresses WHERE oid = " + delete_box.get())
    conn.commit()
    conn.close()  

def update():
  conn = sqlite3.connect("address_book.db")
  c = conn.cursor()
  record_id = delete_box.get()
  c.execute("""UPDATE addresses SET
      first_name = :first,
      last_name = :last,
      address = :address,
      city = :city,
      state = :state,
      zipcode = :zipcode

      WHERE oid = :oid""",
      {'first':f_name_editor.get(),
       'last':l_name_editor.get(),
       'address':address_editor.get(),
       'city':city_editor.get(),
       'state':state_editor.get(),
       'zipcode':zipcode_editor.get(),
       'oid': record_id}
      )
  
  conn.commit()
  conn.close()
  editor.destroy()

def edit():
  global editor
  editor = Tk()
  editor.title("Edit Record")
  editor.iconbitmap("icon.ico")
  conn = sqlite3.connect("address_book.db")
  c = conn.cursor()
  
  record_id = delete_box.get()
  c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
  records = c.fetchall()

  global f_name_editor
  global l_name_editor
  global address_editor  
  global city_editor  
  global state_editor  
  global zipcode_editor

  f_name_editor = Entry(editor, width=30)
  f_name_editor.grid(row=1, column=1, padx=20, pady=(10,0))
  l_name_editor = Entry(editor, width=30)
  l_name_editor.grid(row=2, column=1, padx=20)
  address_editor = Entry(editor, width=30)
  address_editor.grid(row=3, column=1, padx=20)
  city_editor = Entry(editor, width=30)
  city_editor.grid(row=4, column=1, padx=20)
  state_editor = Entry(editor, width=30)
  state_editor.grid(row=5, column=1, padx=20)
  zipcode_editor = Entry(editor, width=30)
  zipcode_editor.grid(row=6, column=1, padx=20)

  f_name_label = Label(editor, text="First Name")
  f_name_label.grid(row=1,column=0, pady=(10,0), sticky=W)
  l_name_label = Label(editor, text="Last Name")
  l_name_label.grid(row=2,column=0, sticky=W)
  address_label = Label(editor, text="Address")
  address_label.grid(row=3,column=0, sticky=W)
  city_label = Label(editor, text="City")
  city_label.grid(row=4,column=0, sticky=W)
  state_label = Label(editor, text="State")
  state_label.grid(row=5,column=0, sticky=W)
  zipcode_label = Label(editor, text="Zipcode")
  zipcode_label.grid(row=6,column=0, sticky=W)
  
  for record in records:
     f_name_editor.insert(0, record[0])
     l_name_editor.insert(0, record[1])
     address_editor.insert(0, record[2])
     city_editor.insert(0, record[3])
     state_editor.insert(0, record[4])
     zipcode_editor.insert(0, record[5])

  edit_btn = Button(editor, text="Save Record", command=update)
  edit_btn.grid(row=8, column=0, columnspan=2, pady=10, sticky=W+E)
  
def query():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()

    print_records = ""
    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + " " + "\t" +  str(record[6]) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=0, columnspan=2)
    conn.commit()
    conn.close()

def show():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    pop = Toplevel()
    pop.title("Address Book")
    pop.iconbitmap("icon.ico")
    pop.geometry("500x500")
    print_records = ""
    for record in records:
        print_records += "Number: "+ str(record[6]
          ) + "\nFirst Name: "+ str(record[0]
          ) + "\nLast Name: " + str(record[1]
          ) + "\nAddress: " + str(record[2]
          ) + "\nCity: " + str(record[3]
          ) + "\nState: " + str(record[4]
          ) + "\nZipcode: " + str(record[5]
          ) + "\n===================\n"

    query_label = Label(pop, text=print_records, justify="left")
    query_label.pack(anchor=NW)
    conn.commit()
    conn.close()

f_name = Entry(root, width=30)
f_name.grid(row=1, column=1, padx=10, pady=(10,0))
l_name = Entry(root, width=30)
l_name.grid(row=2, column=1, padx=10)
address = Entry(root, width=30)
address.grid(row=3, column=1, padx=10)
city = Entry(root, width=30)
city.grid(row=4, column=1, padx=10)
state = Entry(root, width=30)
state.grid(row=5, column=1, padx=10)
zipcode = Entry(root, width=30)
zipcode.grid(row=6, column=1, padx=10)
delete_box = Entry(root, width=30)
delete_box.insert(0, "Enter the number:")
delete_box.grid(row=9, column=1)

f_name_label = Label(root, text="First Name")
f_name_label.grid(row=1,column=0, pady=(10,0), sticky=W)
l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=2,column=0, sticky=W)
address_label = Label(root, text="Address")
address_label.grid(row=3,column=0, sticky=W)
city_label = Label(root, text="City")
city_label.grid(row=4,column=0, sticky=W)
state_label = Label(root, text="State")
state_label.grid(row=5,column=0, sticky=W)
zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=6,column=0, sticky=W)
delete_label = Label(root, text="Select ID")
delete_label.grid(row=9,column=0, sticky=W)

submit_btn = Button(root, text="Add to database", command=submit)
submit_btn.grid(row=7,column=0, columnspan=2, pady=(10,0), sticky=W+E)
query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=8, column=0, columnspan=2, pady=(0,10), sticky=W+E)
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=(10,0), sticky=W+E)
edit_btn = Button(root, text="Edit Record", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=(0,10), sticky=W+E)
show_btn = Button(root, text="Show Address Book", command=show)
show_btn.grid(row=0, column=0, columnspan=2, pady=(10,0), sticky=W+E)

conn.commit()
conn.close()

root.mainloop()
