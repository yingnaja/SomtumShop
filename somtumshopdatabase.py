import csv
from datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk

#============ DATABASE ==============================================================
from basicsql import *
from memberdb import *
# View_member()
#============ menufunction ==============================================================
from menufunction import *
from productdb import *

addproduct = AddProduct()
producticon = ProductIcon()


# =========== CSV ====================================================================

def WriteToCSV(data, filename='data.csv'):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        fw = csv.writer(file)  # บันทึกลง CSV
        fw.writerow(data)
        
def UpdateCSV(data, filename='data.csv'):
    # data = [[a,b],[a,b]]
    with open(filename, 'w', newline='',encoding='utf-8') as file:
        fw = csv.writer(file)
        fw.writerows(data)   # writerows  การเขียนทับ list

# =======================================================================================
root = Tk()
root.title('โปรแกรมร้านขายส้มตำ')
root.geometry('1200x700+50+20')
root.iconbitmap('images/Steak.ico')  # ใส่ไอคอนให้หน้าต่าง
root.state('zoomed')

# ============== Menu Bar ===============================================================
menubar = Menu(root)
root.config(menu=menubar)

#=============== เมนู File =================================================================
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)   # ใส่เมนู File ในเมนูบาร์หลัก
#======= เมนูย่อยของ File =======================
def ExportDatabase():
    print('Export Database')

filemenu.add_command(label='Export', command=ExportDatabase)  # เมนูย่อยของเมนู File
filemenu.add_command(label='ปิดโปรแกรม',command=lambda: root.destroy())  # ปิดโปรแกรม  root.destroy()

#=============== เมนู Member =================================================================
membermenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Member', menu=membermenu)

#=============== เมนู Setting =================================================================
settingmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Settings', menu=settingmenu)

settingmenu.add_command(label='Add Icon', command=producticon.command)

#=============== เมนู Help =================================================================
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=helpmenu)
#======= เมนูย่อยของ Help =======================
import webbrowser  # ใช้สำหรับติดต่อเวปภายนอก

contract_url = 'https://google.co.th'
helpmenu.add_command(label='ติดต่อเรา',command=lambda: webbrowser.open(contract_url)) 

def About():
    ABGUI = Toplevel()  # สร้างหน้าต่างขึ้นมาใหม่อีกหนึ่งหน้าต่าง
    ABGUI.geometry('300x200')
    ABGUI.title('About')
    ABGUI.iconbitmap('images/Steak.ico')  # ใส่ไอคอนให้หน้าต่าง
    
    L = Label(ABGUI, text='โปรแกรมร้านขายส้มตำ',font=(None, 10, 'bold')).pack(pady=10)
    L = Label(ABGUI, text='พัฒนาโดยนายสิญญพงษ์  สุขิโต\n0897513041',font=(None, 10, 'bold')).pack()
    
    ABGUI.mainloop()

helpmenu.add_command(label='About',command=About)

#=============== เมนู product =================================================================
productmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Product', menu=productmenu)

productmenu.add_command(label='Add Product',command=addproduct.command) 

# ============== Tab ===================================================================
Tab = ttk.Notebook(root)   
Tab.pack(fill=BOTH, expand=1)

TabMain = Frame(Tab)  # แท็บใช้งานหลักของโปรแกรม
TabMember = Frame(Tab)  # แท็บสมาชิก

icon_tabmain = PhotoImage(file='images/Steak-icon.png')  # ไอคอนสำหรับแท็บ
icon_tabmember = PhotoImage(file='images/User-icon.png')   # ไอคอนสำหรับแท็บ

Tab.add(TabMain, text='หน้าร้าน',image=icon_tabmain,compound='left')   # เพิ่มแท็บเข้าไป
Tab.add(TabMember, text='สมาชิก',image=icon_tabmember,compound='left')   # เพิ่มแท็บเข้าไป

# =======================================================================================

L1 = Label(TabMain, text='ร้านขายส้มตำ',font=(None, 20, 'bold')).pack()

# =========== TabMain Frame Button =====================================================

Frame_button = Frame(TabMain)
Frame_button.place(x=30, y=70)

Frame_search = Frame(TabMain)
Frame_search.place(x=30, y=20)

Frame_tabel_order = Frame(TabMain)
Frame_tabel_order.place(x=400, y=70)

Frame_total = Frame(TabMain)
Frame_total.place(x=400, y=400)

allmenu = {}
# product = {'tumthai':{'name':'ส้มตำไทย','price':50},
#            'tumplara':{'name':'ส้มตำปลาร้า','price':60}}
product = product_icon_list()

def UpdateTable():
    table_order.delete(*table_order.get_children())  # เคลียร์ข้อมูลเก่าในตาราง
    for i,m in enumerate(allmenu.values(),start=1):  # นับ enumerate เริ่มจาก 1 .values คือเอา values มาไม่เอาคีย์
        table_order.insert('','end',value=[i, m[0],m[1],m[2],m[3]])  # ใส่ข้อมูลลงในตาราง table_order

def AddMenu(name = 'tumthai'):
    if name not in allmenu:
        allmenu[name] = [product[name]['name'],product[name]['price'],1,product[name]['price']]  # บันทึกข้อมูลเข้าไปใน allmenu
    else:
        quan = allmenu[name][2] + 1  # เพิ่มจำนวนสินค้า
        total = quan * product[name]['price']  # คำนวณราคา
        allmenu[name] = [product[name]['name'],product[name]['price'],quan,total]  
    
    # ============ คำนวณ total ==============   
    # count = sum([m[3] for m in allmenu.values()])  แบบย่อ
    # v_total.set(sum(count))
    countlist = []
    for m in allmenu.values():
        countlist.append(m[3])
    
    total = sum(countlist)
    v_total.set(total)
    
    UpdateTable()  # ใส่ข้อมูลลงในตาราง


button_dict = {}

row = 0
column = 0
column_quan = 4
for i, (k,v) in enumerate(product.items()):
    if column == column_quan:
        column = 0
        row += 1
    # print('IMG =======>',v['icon'])
    new_icon = PhotoImage(file=v['icon'])
    B = ttk.Button(Frame_button,text=v['name'],compound='top')
    
    # เอาไปใส่ในฟังชั่น Addproduct
    button_dict[v['id']] = {'button':B, 'row':row, 'column':column}
    
    B.configure(command = lambda m=k: AddMenu(m))
    B.configure(image=new_icon)
    B.image = new_icon          # เป็นการใส่ image ใน button
    B.grid(row=row,column=column,ipadx=5,ipady=5)
    column += 1
    
# print('Button Dict=====>',button_dict) 
addproduct.button_list = button_dict  # ส่ง button_dict ไปใช้ใน menufunction
addproduct.button_frame = Frame_button # ส่ง Frame_button ไปใช้ใน menufunction

producticon.button_list = button_dict  # ส่ง button_dict ไปใช้ใน menufunction
producticon.button_frame = Frame_button # ส่ง Frame_button ไปใช้ใน menufunction

# =========== TabMain Frame Table Order =====================================================

header = ['รายการที่','รายการ','ราคา','จำนวน','ราคารวม']
head_width = [100,300,100,100,120]

style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 12,'bold')) # Modify the font of the headings
style.configure("Treeview", highlightthickness=5, bd=5, font=(None, 12)) # Modify the font of the body
style.configure('Treeview', rowheight=30) # repace 40 with whatever you need
# style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
table_order = ttk.Treeview(Frame_tabel_order, columns=header, show='headings', height=10)
table_order.pack()
    
for hd ,hw in zip(header, head_width):
    table_order.heading(hd, text=hd)
    table_order.column(hd, width=hw)
    
# =========== Frame Total =================================================================================
    
v_total = StringVar()
v_total.set(0.0)

L = Label(Frame_total, text='ราคารวม : ',font=(None, 20,'bold'),fg='green').grid(row=0,column=0) # แสดงราคารวม
L = Label(Frame_total, textvariable=v_total,font=(None, 20,'bold'),fg='red').grid(row=0,column=1) 
L = Label(Frame_total, text=' บาท ',font=(None, 20,'bold'),fg='green').grid(row=0,column=2) # 

def Reset(): #  เคลียร์ข้อมูลในตาราง table_order
    global allmenu
    table_order.delete(*table_order.get_children())
    allmenu = {}
    v_total.set(0.0)
    trstamp = datetime.now().strftime('ST-%y%m%d%H%M%S')
    v_transaction.set(trstamp) 
    table_id.set('') 
    
def AddTransaction():
    stamp = datetime.now().strftime('%d-%m-%y %H:%M:%S')
    transaction = v_transaction.get()
    tableid = table_id.get()
    # print('ALLMENU =======> ',allmenu.values())
    # ['ส้มตำปลาร้า', 60, 1, 60]  allmenu.values()
    for m in allmenu.values():
        m.insert(0, tableid)   # แทรกโต๊ะที่ ไปใน list ลำดับที่ 0
        m.insert(1, transaction)   # แทรกเลขที่ ไปใน list ลำดับที่ 1
        m.insert(2, stamp)   # แทรกเวลาที่บันทึก ไปใน list ลำดับที่ 2
        WriteToCSV(m, 'transaction.csv')  # บันทึกลง CSV ชื่อไฟล์ transaction.csv (m คือ list)
    
    Reset()  # เคลียร์ข้อมูลทังหมดในหน้า Order
        
B = Button(Frame_total, text='เคลียร์ Order',font=(None,15,'bold'),command=Reset).grid(row=1,column=0,ipadx=10,ipady=10,pady=10)
B = Button(Frame_total, text='บันทึก',font=(None,15,'bold'),command=AddTransaction).grid(row=1,column=1,ipadx=10,ipady=10,pady=10)

# =======================================================================================
# =========== Transaction id ============================================================

LTB = Label(TabMain, text='โต๊ะที่ ',font=(None,15,'bold')).place(x=700, y=35)
table_id = StringVar()
ET = Entry(TabMain, textvariable=table_id,font=(None,15,'bold'),width=7).place(x=760, y=35)

L = Label(TabMain, text='เลขที่ ',font=(None,15,'bold')).place(x=890, y=35)
v_transaction = StringVar()
trstamp = datetime.now().strftime('ST-%y%m%d%H%M%S')
v_transaction.set(trstamp)
LT = Label(TabMain, text='โต๊ะที่ ',font=(None,15,'bold')).place(x=700, y=35)
LTR = Label(TabMain, textvariable=v_transaction,font=(None,15,'bold')).place(x=950, y=35)

# =======================================================================================
# =========== History window ประวัติการสั่งซื้อ ===============================================

def HistoryWindow(event=None):
    HTS = Toplevel()  # สร้าง window ขึ้นมาใหม่อีก 1 หน้าต่าง
    HTS.geometry('900x500+20+20')
    HTS.title('ประวัติการสั่งซื้อ')
    HTS.iconbitmap('images/Steak.ico')  # ใส่ไอคอนให้หน้าต่าง
    
    # ======= Table History =======================================
    LH = Label(HTS, text='ประวัติการสั่งซื้อ',font=(None,15,'bold')).pack(pady=15)
    
    header = ['โต๊ะที่','เวลาที่ซื้อ','เลขที่ใบเสร็จ','รายการ','ราคา','จำนวน','ราคารวม']
    head_width = [50,150,150,200,100,100,100]

    style = ttk.Style()
    style.configure("Treeview.Heading", font=(None, 12,'bold')) # Modify the font of the headings
    style.configure("Treeview", highlightthickness=5, bd=5, font=(None, 12)) # Modify the font of the body
    style.configure('Treeview', rowheight=30) # repace 40 with whatever you need
    table_history = ttk.Treeview(HTS, columns=header, show='headings', height=10)
    table_history.pack(pady=10)
        
    for hd ,hw in zip(header, head_width):
        table_history.heading(hd, text=hd)
        table_history.column(hd, width=hw)
        
    # ======= update from CSV =================================
    with open('transaction.csv', newline='',encoding='utf-8') as file:
        fr = csv.reader(file)   # อ่านข้อมูลจาก transaction.csv
        for row in fr:
            table_history.insert('', 0, value=row)   # เรียกข้อมูลจาก csv ลงตาราง
       
    HTS.mainloop()
    
root.bind('<F1>', HistoryWindow)  # เรียกใช้หน้าต่างประวัติการสั่งซื้อด้วย F1 ใน function ต้องใส่ event=None
B = Button(Frame_total, text='ประวัติการสั่งซื้อ',font=(None,15,'bold'),command=HistoryWindow).grid(row=1,column=2,ipadx=10,ipady=10,pady=10)

# =======================================================================================
# =========== Member Tab  ===============================================================

Frame_add_member = Frame(TabMember)
Frame_add_member.place(x=40, y=25)

Frame_add_member_button = Frame(TabMember)
Frame_add_member_button.place(x=40, y=250)

v_membercode = StringVar()
v_membercode.set('M-1001')
v_databasecode = IntVar()

L = Label(Frame_add_member, text='รหัสสมาชิก: ',font=(None, 15)).grid(row=0,column=0,sticky=W)
Lcode = Label(Frame_add_member, textvariable=v_membercode,font=(None, 15)).grid(row=0,column=1,sticky=W)

v_fullname = StringVar()
L = Label(Frame_add_member, text='ชื่อ - สกุล', font=(None, 15)).grid(row=1, column=0,sticky=W)
Ename = Entry(Frame_add_member,textvariable= v_fullname,font=(None, 15),width=20)
Ename.grid(row=1, column=1, pady=10)
v_tel = StringVar()
L = Label(Frame_add_member, text='เบอร์โทรศัพท์', font=(None, 15)).grid(row=2, column=0,sticky=W)
Ename = Entry(Frame_add_member,textvariable= v_tel,font=(None, 15),width=20)
Ename.grid(row=2, column=1, pady=10)
v_usertype = StringVar()
v_usertype.set('general')
L = Label(Frame_add_member, text='ประเภทสมาชิก', font=(None, 15)).grid(row=3, column=0,sticky=W)
Ename = Entry(Frame_add_member,textvariable= v_usertype,font=(None, 15),width=20)
Ename.grid(row=3, column=1, pady=10)
v_point = StringVar()
L = Label(Frame_add_member, text='คะแนนสะสม', font=(None, 15)).grid(row=4, column=0,sticky=W)
Ename = Entry(Frame_add_member,textvariable= v_point,font=(None, 15),width=20)
Ename.grid(row=4, column=1, pady=10)

def SaveMember():
    code = v_membercode.get()
    fullname = v_fullname.get()
    tel = v_tel.get()
    usertype = v_usertype.get()
    point = v_point.get()
    # print('Member Save ======>', fullname,tel,usertype,point)
    # WriteToCSV([code,fullname,tel,usertype,point], 'member.csv')  # บันทึกข้อมูลสมาชิกลง CSV
    Insert_member(code,fullname,tel,usertype,point)
    # table_member.insert('',0,value=[code,fullname,tel,usertype,point])  # บันทึกข้อมูลลงตารางสมาชิก
    
    UpdateTableMember()
     #============= set default ===================
    v_fullname.set('')
    v_tel.set('')
    v_usertype.set('general')
    v_point.set('0')
    
BSave = Button(Frame_add_member_button, text='บันทึก',font=(None,15,'bold'),command=SaveMember)
BSave.grid(row=0,column=0,ipadx=10,ipady=10,pady=10)

def EditMember():
    code = v_databasecode.get()  # ดึงรหัสฐานข้อมูล
    allmember[code][2] = v_fullname.get()
    allmember[code][3] = v_tel.get()
    allmember[code][4] = v_usertype.get()
    allmember[code][5] = v_point.get()
    
    # UpdateCSV(list(allmember.values()),'member.csv')
    Update_member(code, 'fullname',v_fullname.get())
    Update_member(code, 'tel',v_tel.get())
    Update_member(code, 'usertype',v_usertype.get())
    Update_member(code, 'points',v_point.get())
    
    UpdateTableMember()
    
    BSave = Button(Frame_add_member_button, text='บันทึก',font=(None,15,'bold'),command=SaveMember) # ปิดปุ่มบันทึก
    BSave.grid(row=0,column=0,ipadx=10,ipady=10,pady=10)
    BEdit = Button(Frame_add_member_button, text='แก้ไข',font=(None,15,'bold'),state=DISABLED ,command=EditMember)
    BEdit.grid(row=0,column=1,ipadx=10,ipady=10,pady=10)
    
    #============= set default ===================
    v_fullname.set('')
    v_tel.set('')
    v_usertype.set('general')
    v_point.set('0')
    
def NewMember():
    UpdateTableMember()
    BSave = Button(Frame_add_member_button, text='บันทึก',font=(None,15,'bold'),command=SaveMember) # ปิดปุ่มบันทึก
    BSave.grid(row=0,column=0,ipadx=10,ipady=10,pady=10)
    BEdit = Button(Frame_add_member_button, text='แก้ไข',font=(None,15,'bold'),state=DISABLED ,command=EditMember)
    BEdit.grid(row=0,column=1,ipadx=10,ipady=10,pady=10)
    #============= set default ===================
    v_fullname.set('')
    v_tel.set('')
    v_usertype.set('general')
    v_point.set('0')
    
    
# ======= Table Member =======================================
Frame_table_member = Frame(TabMember)
Frame_table_member.place(x=420, y=1)

LH = Label(Frame_table_member, text='ข้อมูลสมาชิก',font=(None,20,'bold')).pack(pady=15)

header = ['ID','รหัสสมาชิก','ชื่อ - สกุล','เบอร์โทรศัพท์','ประเภทสมาชิก','คะแนนสะสม']
head_width = [50,100,200,150,150,100]

style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 12,'bold')) # Modify the font of the headings
style.configure("Treeview", highlightthickness=5, bd=5, font=(None, 12)) # Modify the font of the body
style.configure('Treeview', rowheight=30) # repace 40 with whatever you need
table_member = ttk.Treeview(Frame_table_member, columns=header, show='headings', height=10)
table_member.pack(pady=10)
    
for hd ,hw in zip(header, head_width):
    table_member.heading(hd, text=hd)
    table_member.column(hd, width=hw)
    
# ========== ลบข้อมูลในตาราง =============================
def DeleteMember(event=None):
        message = messagebox.askyesno('ลบข้อมูล','คุณต้องการลบข้อมูลหรือไม่')
        if message == True:
            select = table_member.selection()  # เลือกส่วนที่ต้องการลบ
            if len(select) != 0:
                data = table_member.item(select)['values']  # ข้อมูลที่เราเลือกมา (ต้องการรหัสสมาชิกไปใช้)
            
                del allmember[data[0]]
                Delete_member(data[0])
                # UpdateCSV(list(allmember.values()),'member.csv')
                
                UpdateTableMember()
        else:
            messagebox.showwarning('error','กรูณาเลือกรายการก่อนลบข้อมูล')

table_member.bind('<Delete>', DeleteMember)  # กดปุ่ม Delete เพื่อลบข้อมูล

# ======= แก้ไขข้อมูลสมาชิก ==========================================

def UpdateMemberInfo(event=None):
    select = table_member.selection()  # เลือกส่วนที่ต้องการลบ
    if len(select) != 0:
        code = table_member.item(select)['values'][0]  # ข้อมูลที่เราเลือกมา (ต้องการรหัสสมาชิกไปใช้)
        v_databasecode.set(code)
        # print('DATA =====> ',code)
        # DATA =====>  ['M-1001', 'ปิยวรรณ์  สุขิโต', 821452145, 'vip', 500]
        
        memberinfo = allmember[code]
        v_membercode.set(memberinfo[1])
        v_fullname.set(memberinfo[2])
        v_tel.set(memberinfo[3])
        v_usertype.set(memberinfo[4])
        v_point.set(memberinfo[5])
        
        BSave = Button(Frame_add_member_button, text='บันทึก',font=(None,15,'bold'),state=DISABLED ,command=SaveMember) # ปิดปุ่มบันทึก
        BSave.grid(row=0,column=0,ipadx=10,ipady=10,pady=10)
        BEdit = Button(Frame_add_member_button, text='แก้ไข',font=(None,15,'bold'),command=EditMember)
        BEdit.grid(row=0,column=1,ipadx=10,ipady=10,pady=10)
        BSave = Button(Frame_add_member_button, text='เคลียร์ข้อมูล',font=(None,15,'bold'),command=NewMember) # ปิดปุ่มบันทึก
        BSave.grid(row=0,column=2,ipadx=10,ipady=10,pady=10)
    else:
        messagebox.showwarning('error','กรูณาเลือกรายการก่อนแก้ไขข้อมูล')
     
table_member.bind('<Double-1>', UpdateMemberInfo)  # ดับเบิ้ลคลิกเพื่อเลือก

# ======= update table from CSV =================================
last_member = ''
allmember = {}

def UpdateTableMember():
    global last_member
    
    fr = View_member()   # ดึงข้อมูลมาจากฐานข้อมูล
    # [(1, 'MB-1001', 'sinyapong sukito', '0897513041', 'vip', 100),(2, 'MB-1002', 'ปิยวรรณ์  สุขิโต', '0897513041', 'vip', 100)]
    table_member.delete(*table_member.get_children())
    for row in fr:
        table_member.insert('', 'end', value=row)   # เรียกข้อมูลจาก csv ลงตาราง
        code = row[0]
        allmember[code] = list(row)
            
    # print('LASTMEMBER ====> ',row)
    last_member = row[1]
    next_member = int(last_member.split('-')[1]) + 1  # แยกnumbercode ออก แล้วนำมา + 1
    v_membercode.set(f'M-{next_member}')
    # print('ALLMEMBER =====> ',allmember)
    
    
# ======= Popup Menu =================================
member_right_clickmenu = Menu(root, tearoff=0)
member_right_clickmenu.add_command(label='Delete',command=DeleteMember)
member_right_clickmenu.add_command(label='Edit', command=UpdateMemberInfo)

# table_member.bind('<Button-3>', lambda event: member_right_clickmenu.post(event.x_root, event.y_root))
def popup(event):
    member_right_clickmenu.post(event.x_root, event.y_root)
    
table_member.bind('<Button-3>',popup)

def SearchName():
    try:
        select = table_member.selection()
        name = table_member.item(select)['values'][1]
        # print('CODE =====> ', code)
        url = 'https://www.google.com/search?q={}'.format(name)
        webbrowser.open(url)
    except:
        pass
    
member_right_clickmenu.add_command(label='Search Name', command=SearchName)


# =======================================================================================
# =======Search product ==================================================================

v_search_barcode = StringVar()
Esearch = Entry(Frame_search, textvariable=v_search_barcode, font=(None, 20),width=18)
Esearch.grid(row=0,column=0)

def SearchBarcode(event=None):
    barcode = v_search_barcode.get()
    try:
        res = View_product_single(barcode)
        # print('RES ================>', res)
        # (4, 'A-1002', 'ส้มตำปลาร้า', 100.0, 'C:/Users/ying4/coffee-icon.png'
        productid = res[0]
        AddMenu(productid)
    except:
        messagebox.showerror('ไม่พบสินค้า','ไม่มีสินค้าในระบบ')
        v_search_barcode.set('')
        Esearch.focus()
    

Bsearch = Button(Frame_search, text='Search', font=(None, 13),command=SearchBarcode)
Bsearch.grid(row=0,column=1)

Esearch.bind('<Return>',SearchBarcode)
Esearch.bind('<F3>', lambda x : v_search_barcode.set(''))

# =======================================================================================

try:
    UpdateTableMember()
except:
    print('กรุณากรอกข้อมูลอย่างน้อย 1 รายการ')
    
root.mainloop()
