import sqlite3

conn = sqlite3.connect('orderdb.sqlite3')
c = conn.cursor()  # สร้างเคอร์เซอร์

# ========= สร้างตารางจัดเก็บข้อมูล =================================================================================

c.execute("""CREATE TABLE IF NOT EXISTS orderstable (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                tables TEXT,
                transactions TEXT,
                timeorders TEXT,
                names TEXT,
                price REAL,
                quantity INTEGER,
                total REAL)""")

# ======= Function ใส่ข้อมูลลงไปในฐานข้อมูล =========================================================================

def Insert_order(tables, transactions, timeorders, names, price, quantity, total):
    with conn:
        command = 'INSERT INTO orderstable VALUES (?,?,?,?,?,?,?,?)'
        c.execute(command, (None,tables, transactions, timeorders, names, price, quantity, total))
        
    conn.commit()
    print('Saved')
    
    
    
# Insert_order(2, 'ST-1003', '22:20:22','somtummeekrop',200,1,200)