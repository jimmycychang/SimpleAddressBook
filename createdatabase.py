import sqlite3

conn = sqlite3.connect("address_book.db")
c = conn.cursor()
c.execute("""CREATE TABLE addresses (
    first_name text,
    last_name text,
    address text,
    city text,
    state text,
    zipcode integer
    )""")

conn.commit()
conn.close()