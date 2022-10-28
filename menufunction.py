
from sqlite3 import Row
from tkinter import *
from tkinter import filedialog, ttk
import os

DIR = os.getcwdb     # เลือกตำแหน่งโฟลเดอร์ที่ทำงานรัน

from productdb import *

# ======================== CLASS PRODUCT =======================================================

class AddProduct:
    
    def __init__(self):
        self.v_productid = None
        self.v_title = None
        self.v_price = None
        self.v_imgepath = None
        self.MGUI = None
        self.LProductImage = None
        self.button_list = None     # รับ button_dict มาจาก main
        self.button_frame = None    # รับ Frame_button มาจาก main
        
    def popup(self):
        self.MGUI = Toplevel()
        self.MGUI.geometry('400x400')
        self.MGUI.title('Add Product')
        
        L = Label(self.MGUI, text='Add Product',font=(None, 20)).place(x=120, y=5)
        
        Frame_addproduct = Frame(self.MGUI)
        Frame_addproduct.place(x=20, y=50)
        
        self.v_productid = StringVar()
        self.v_title = StringVar()
        self.v_price = StringVar()
        self.v_imgepath = StringVar()
        
        L = Label(Frame_addproduct, text='รหัสสินค้า',font=(None, 15)).grid(row=1,column=0)
        E = Entry(Frame_addproduct, textvariable=self.v_productid,font=(None,15))
        E.grid(row=1,column=1,pady=10)
        
        L = Label(Frame_addproduct, text='ชื่อสินค้า',font=(None, 15)).grid(row=2,column=0)
        E = Entry(Frame_addproduct, textvariable=self.v_title,font=(None,15))
        E.grid(row=2,column=1,pady=10)
        
        L = Label(Frame_addproduct, text='ราคาสินค้า',font=(None, 15)).grid(row=3,column=0)
        E = Entry(Frame_addproduct, textvariable=self.v_price,font=(None,15))
        E.grid(row=3,column=1,pady=10)
        
        # ใส่รูปภาพขนาด 64x64 px
        img = PhotoImage(file='C:/Users/ying4/OneDrive/Desktop/Somtum/images/pictures-icon.png')
        self.LProductImage = Label(Frame_addproduct, image=img, compound='top')
        self.LProductImage.grid(row=4, column=1, columnspan=2)
        
        
        Bselect = Button(Frame_addproduct, text='เลือกรูปสินค้า ขนาด 50x50 px',font=(None, 10),command=self.selectFile)
        Bselect.grid(row=5,column=1,pady=10, columnspan=2)
        
        Bsave = Button(Frame_addproduct, text='Save',font=(None, 10),command=self.saveproduct)
        Bsave.grid(row=6,column=1,pady=10, ipadx=10, ipady=10, columnspan=2)
        
        self.MGUI.mainloop()
        
        
    def selectFile(self):
        filetypes = (
            ('PNG', '*.png'),
            ('All Files', '*.*'))
        
        DIR = os.getcwdb()  # ตำแหน่งโฟลเดอร์
        select = filedialog.askopenfilename(title='เลือกไฟล์ภาพ',initialdir='DIR',filetypes=filetypes)
        img = PhotoImage(file=select)
        self.LProductImage.configure(image=img)
        self.LProductImage.image = img  # ใส่รูปภาพใน Label
        self.v_imgepath.set(select)
        self.MGUI.focus_force()   # โฟกัสหน้าต่างให้อยู่ข้างบน
        self.MGUI.grab_set()
        
        
    def saveproduct(self):
        v1 = self.v_productid.get()
        v2 = self.v_title.get()
        v3 = float(self.v_price.get())
        v4 = self.v_imgepath.get()
        Insert_product(v1,v2,v3,v4)
        self.v_productid.set('')
        self.v_title.set('')
        self.v_price.set('')
        self.v_imgepath.set('')
        View_product()
        
        self.clearbutton()   # เคลียร์ปุ่มก่อน
        self.create_button()  # สร้าง button ใหม่
        
        
    def clearbutton(self):
        for b in self.button_list.values():
            # b = ['button':B, 'row':row, 'column':column]
            # b['button'].grid_forget()  # ลืมปุ่ม
            b['button'].destroy()  # ลบปุ่ม
            
    
    def create_button(self):
        product = product_icon_list()
        global button_dict
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
            B = ttk.Button(self.button_frame,text=v['name'],compound='top')
            
            # เอาไปใส่ในฟังชั่น Addproduct
            button_dict[v['id']] = {'button':B, 'row':row, 'column':column}
            
            B.configure(command = lambda m=k: AddMenu(m))
            B.configure(image=new_icon)
            B.image = new_icon          # เป็นการใส่ image ใน button
            B.grid(row=row,column=column,ipadx=5,ipady=5)
            column += 1
        
        
    def command(self):
        self.popup()
        
        
class ProductIcon:
    
    def __init__(self):
        self.table_product_icon = None
        self.v_radio_status = None
        self.button_list = None   
        self.button_frame = None
    
    def popup(self):
        PGUI = Toplevel()
        PGUI.geometry('500x500')
        PGUI.title('ตั้งค่าโชว์ไอคอนสินต้า')
        
        header = ['ID','รหัสสินค้า','ชื่อสินค้า','แสดงไอคอน']
        head_width = [50,80,220,100]

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 12,'bold')) # Modify the font of the headings
        style.configure("Treeview", highlightthickness=5, bd=5, font=(None, 12)) # Modify the font of the body
        style.configure('Treeview', rowheight=30) # repace 40 with whatever you need
        self.table_product_icon = ttk.Treeview(PGUI, columns=header, show='headings', height=10)
        self.table_product_icon.pack(pady=20)
            
        for hd ,hw in zip(header, head_width):
            self.table_product_icon.heading(hd, text=hd)
            self.table_product_icon.column(hd, width=hw)
        
        self.table_product_icon.bind('<Double-1>', self.Change_status)  
        self.Insert_table()
        PGUI.mainloop()
        
    def Insert_table(self):
        self.table_product_icon.delete(*self.table_product_icon.get_children())
        data = View_product_table_icon()
        print('View_product_table_icon',data)
        
        for d in data:
            row = list(d)
            check = View_product_status(row[0])  #   row[0] = ID
            
            if check[-1] == 'show':
                row.append('✓')
                
            self.table_product_icon.insert('','end',value=row)
            
    def Change_status(self, event=None):
        select = self.table_product_icon.selection()
        pid = self.table_product_icon.item(select)['values'][0]
        # print('PID =========> ', pid)
        
        SGUI = Toplevel()
        SGUI.geometry('300x100')
        
        self.v_radio = StringVar()
        
        RB1 = ttk.Radiobutton(SGUI, text='โชว์เมนู',variable=self.v_radio, value='show',command=lambda x=None:Insert_product_status(int(pid),'show'))
        RB2 = ttk.Radiobutton(SGUI, text='ซ่อนเมนู',variable=self.v_radio, value='',command=lambda x=None:Insert_product_status(int(pid),''))
        RB1.pack(pady=10)
        RB2.pack()
        
        check = View_product_status(pid)
        
        if check[-1] == 'show':
            RB1.invoke()    # ตั้งค่า default
        else:
            RB2.invoke()
         
        # dropdown = ttk.Combobox(SGUI, values=['โชว์เมนู','ไม่โชว์เมนู'])
        # dropdown.pack(pady=10)
        # dropdown.set('โชว์เมนู')
        # dropdown.bind('<<ComboboxSelected>>', lambda x=None: print(dropdown.get()))
        
        def check_code():
            print('Closed')
            SGUI.destroy()
            self.Insert_table()
            self.clearbutton()
            self.create_button()
            
            
        # เมื่อปิดหน้าต่างเลือกแล้วจะอัพเดท status 
        SGUI.protocol('WM_DELETE_WINDOW',check_code)
        
        
        SGUI.mainloop()
        
    def clearbutton(self):
        for b in self.button_list.values():
            # b = ['button':B, 'row':row, 'column':column]
            # b['button'].grid_forget()  # ลืมปุ่ม
            b['button'].destroy()  # ลบปุ่ม
            
    
    def create_button(self):
        product = product_icon_list()
        global button_dict
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
            B = ttk.Button(self.button_frame,text=v['name'],compound='top')
            
            # เอาไปใส่ในฟังชั่น Addproduct
            button_dict[v['id']] = {'button':B, 'row':row, 'column':column}
            
            B.configure(command = lambda m=k: AddMenu(m))
            B.configure(image=new_icon)
            B.image = new_icon          # เป็นการใส่ image ใน button
            B.grid(row=row,column=column,ipadx=5,ipady=5)
            column += 1
            
        
    def command(self):
        self.popup()
    
    
        
 
 
 
        
if __name__=='__main__':
    test = ProductIcon()