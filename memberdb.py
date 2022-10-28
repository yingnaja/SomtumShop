import sqlite3

conn = sqlite3.connect('memberdb.sqlite3')  # สร้างไฟล์ฐานข้อมูล
c = conn.cursor()  # สร้างเคอร์เซอร์

# ========= สร้างตารางจัดเก็บข้อมูล =================================================================================

c.execute("""CREATE TABLE IF NOT EXISTS member (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                membercode TEXT,
                fullname TEXT,
                tel TEXT,
                usertype TEXT,
                points INTEGER)""")


# ======= Function ใส่ข้อมูลลงไปในฐานข้อมูล =========================================================================

def Insert_member(membercode,fullname,tel,usertype,pionts):
    with conn:
        command = 'INSERT INTO member VALUES (?,?,?,?,?,?)'
        c.execute(command, (None,membercode,fullname,tel,usertype,pionts))
        
    conn.commit()   # save database
    print('Saved')
    
# ======= Function ดูข้อมูลทั้งหมดในฐานข้อมูล =========================================================================

def View_member():
    with conn:
        command = 'SELECT * FROM member'
        c.execute(command)
        result = c.fetchall()   # คำสั่งดึงข้อมูลมาโชว์
    return result

# ======= Function อัพเดทข้อมูลในฐานข้อมูลเฉพาะบางฟิว =========================================================================

def Update_member(ID, field, newvalue): # ใส่ ID  ชื่อ ฟิวที่จะแก้ และข้อความที่แก้
    with conn:
        command = 'UPDATE member SET {} = (?) WHERE ID=(?)'.format(field)  # field คือการอัพเดทเฉพาะรายการ เช่น fullname
        c.execute(command,([newvalue, ID]))
    conn.commit()
    print('updated')
    
# ======= Function ลบข้อมูลในฐานข้อมูลเฉพาะบางฟิว =========================================================================
        
def Delete_member(ID):
    with conn:
        command = 'DELETE FROM member WHERE ID = (?)'
        c.execute(command, ([ID]))
    conn.commit()
    print('Deleted')



# Delete_member(3)
# Update_member(1,'fullname','สิญญพงษ์  สุขิโต')   
# View_member()  
# Insert_member('MB-1004','ปิยวรรณ์  สุขิโต', '0895746512','vvip',300)  # ทดลองใส่ข้อมูลลงฐานข้อมูล