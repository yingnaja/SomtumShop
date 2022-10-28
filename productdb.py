import sqlite3

conn = sqlite3.connect('productdb.sqlite3')
c = conn.cursor()

# ========= สร้างตารางจัดเก็บข้อมูล =================================================================================

c.execute("""CREATE TABLE IF NOT EXISTS product (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                productid TEXT,
                title TEXT,
                price REAL,
                images TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS product_status (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                statuss TEXT)""")

# ==============================================================================================================
# ========= Function การใส่ข้อมูลลงตาราง product_status ==========================================================================

def Insert_product_status(pid,statuss):
    # pid = product_id
    check = View_product_status(pid)
    if check == None:
        with conn:
            command = 'INSERT INTO product_status VALUES (?,?,?)'
            c.execute(command, (None,pid,statuss))
        conn.commit()
        print('Status Saved')
    else:
        print('======PID EXIT======')
        print('CHECK INSERT ======>',check)
        Update_product_status(pid, statuss)
        
        
def View_product_status(pid):
    with conn:
        command = 'SELECT * FROM product_status WHERE product_id=(?)'
        c.execute(command, ([pid]))
        result = c.fetchone()
    return result

       
def Update_product_status(pid,statuss):
    with conn:
        command = 'UPDATE product_status SET statuss = (?) WHERE product_id = (?)'
        c.execute(command, ([statuss, pid]))
    conn.commit()
    print('Update Statuss',statuss)


# ========= Function การใส่ข้อมูลลงตาราง =================================================================================

def Insert_product(productid,title,price,images):
    ######################################
    # ตรวจสอบก่อนว่า productid ที่มีแล้ว ห้ามซ้ำ
    ######################################
    
    with conn:
        command = 'INSERT INTO product VALUES (?,?,?,?,?)'
        c.execute(command, (None,productid,title,price,images))
    conn.commit()
    print('Product Saved')
    # add status after insert product
    find = View_product_single(productid)
    Insert_product_status(find[0],'show')

# ==============================================================================================================
# ========= Function เรียกข้อมูลทั้งหมดมาใช้ =================================================================================

def View_product():
    with conn:
        command = 'SELECT * FROM product'
        c.execute(command)
        result = c.fetchall()
    # print('View_product =====> ',result)
    return result

# ==============================================================================================================
# ========= Function เรียกข้อมูล ข้อมูลเดียว มาใช้  =================================================================

def View_product_single(productid):
    with conn:
        command = 'SELECT * FROM product WHERE productid=(?)'
        c.execute(command, ([productid]))
        result = c.fetchone()
    return result

# ==============================================================================================================
# ========= Function เรียกข้อมูล เฉพาะบางส่วน มาใช้  =================================================================

def View_product_table_icon():
    with conn:
        command = 'SELECT ID, productid, title FROM product'
        c.execute(command)
        result = c.fetchall()
    # print('View_product =====> ',result)
    return result

# ==============================================================================================================

# ========= Function เรียกข้อมูล เฉพาะบางส่วน มาใช้  =================================================================
product = {'tumthai':{'name':'ส้มตำไทย','price':50},
           'tumplara':{'name':'ส้มตำปลาร้า','price':60},
           'tummeekrop':{'name':'ส้มตำหมี่กรอบ','price':100},
           'tummookrop':{'name':'ส้มตำหมูกรอบ','price':200},
           'tummoo':{'name':'ส้มตำหมูกรอบ','price':300}}

def product_icon_list():
    with conn:
        command = 'SELECT * FROM product'
        c.execute(command)
        product = c.fetchall()
        
    with conn:
        command = "SELECT * FROM product_status WHERE statuss = 'show'"
        c.execute(command)
        status = c.fetchall()
    
    # print('PRODUCT ===============>',product) # [[(1, 'ST-1001', 'somtumthai', 50.0, 'C:\\UsersSteak-icon.png')]
    # print('STATUS ===============>',status) # [(23, 1, 'show'), (24, 3, 'show'), (25, 4, 'show')
    
    result = []
    
    for s in status:
        for p in product:
            if s[1] == p[0]:
                result.append(p)
    # print('RESULT ======> ',result)  #[(1, 'ST-1001', 'somtumthai'), (2, 'ST-1002', 'somtumprala')]
    result_dict = {}
    for r in result:
        result_dict[r[0]] = {'id':r[0],'productid':r[1],'name':r[2],'price':r[3],'icon':r[4]}

    return result_dict

# ==============================================================================================================


if __name__ == '__main__':
    x = product_icon_list()
    print('ProDUct ====>',x)
    # View_product_show_icon()
    # View_product_status(1)
    # View_product_table_icon()
    # Insert_product('ST-1002','somtumprala',100,r'C:\Users\ying4\OneDrive\Desktop\Somtum\images\Steak-icon.png')