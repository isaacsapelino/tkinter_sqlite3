''' Fixed by: Isaac A. Sapelino '''
''' Note: There are still left to do..'''

from tkinter.ttk import *
from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
from tksheet import Sheet
import sqlite3
import tkinter as tk
DEBUG = False        # This is to serve if you want to create a table that was once deleted.

def update_withdraw(name, groupno, section, num1, id):
    db = 'SELECT quantity FROM items WHERE item_name=?'

    conn = sqlite3.connect("User_Database.db")
    cursor = conn.cursor()
    if num1 > 0:
        cursor.execute("INSERT INTO groups_items(pid, name, quantity, item_id) VALUES((SELECT pid FROM groups WHERE group_number=? AND section=?), ?, ?, (SELECT id FROM items WHERE item_name=?))", (groupno, section, name, num1, name))
        num = int(cursor.execute(db, (name,)).fetchone()[0])
        result = num - num1
        cursor.execute('UPDATE items SET quantity=? WHERE id=?', (result, id))
    else:
        print('No changes to', name)
    conn.commit()
    conn.close()

def update_deposit(name, groupno, section, num1, id):
    db = 'SELECT quantity FROM items WHERE item_name=?'

    conn = sqlite3.connect("User_Database.db")
    cursor = conn.cursor()
    if num1 > 0:
        db_s = cursor.execute("SELECT pid FROM groups WHERE group_number=? AND section=?", (groupno,section)).fetchone()
        cursor.execute('DELETE FROM groups_items WHERE id=(SELECT id FROM groups_items WHERE pid=?)', (db_s))
        num = int(cursor.execute(db, (name,)).fetchone()[0])
        result = num + num1
        cursor.execute('UPDATE items SET quantity=? WHERE id=?', (result,id))
    else:
        print('No changes to', name)
    conn.commit()
    conn.close()


class PLMS_Menu(tk.Frame):
    def __init__(self, root):
        super(PLMS_Menu, self).__init__()
        self.widgets={}
        self.grid(column=0,row=0)
        self.root = root
        self.root.geometry('400x200')
        self.root.title('Physics Laboratory Management System')

        #         VARIABLE'S
        vcmd = (self.root.register(self.callback))
        self.group_number = StringVar()
        self.section = StringVar()

        Label(text="Group Number", font=('Arial Rounded MT Bold', 10)).place(x=80, y=40)

        self.group_numbeer = Entry(textvar=self.group_number, validate='all', validatecommand=(vcmd, '%P'))
        self.group_numbeer.focus_set()
        self.group_numbeer.place(x=190, y=40)

        Label(text="Section", font=('Arial Rounded MT Bold', 10)).place(x=80, y=70)
        self.seection = Entry(textvar=self.section)
        self.seection.place(x=190, y=70)

        Button(text="Withdraw", command=self.withdraw).place(x=80, y=120)
        Button(text="Deposite", command=self.deposite).place(x=260, y=120)
        Button(text="Show Record", command=self.show_records).place(x=160,y=120)

        menu = Menu(self.root)
        self.root.config(menu=menu)


        file = Menu(menu,tearoff=0)

        menu.add_cascade(label="File", menu=file)
        file.add_command(label="Register", command=self.register)
        file.add_separator()
        file.add_command(label="Storage", command=self.storage)


    def callback(root, P):
        if str.isdigit(P):
            return True
        elif P == " ":
            messagebox.showinfo("Must not empty")
        else:
            messagebox.showinfo("Alert", "Number's Only")
            return False

    def return_self(self):

        self.newroot = Tk()
        application = PLMS_Menu(self.newroot)
        self.root.mainloop()

    def user_check(self):
        group_num = self.group_number.get()
        section = self.section.get()
        conn = sqlite3.connect("User_Database.db")
        cursor = conn.cursor()
        check_user = "SELECT group_number, section FROM groups WHERE group_number=? AND section=?"
        vals = cursor.execute(check_user, (group_num, section,)).fetchone()

        if vals:
            return True
        else:
            return False      

        conn.commit()
        conn.close()

    def register(self):
        self.root.destroy()
        self.newrootregs = Tk()
        self.newrootregs.title("Register")
        self.newrootregs.geometry("400x200")
        vcmd = (self.newrootregs.register(self.callback))

        Label(text="Group Number", font=('Arial Rounded MT Bold', 10)).place(x=80, y=40)
        self.group_number = Entry(textvar=self.group_number, validate='all', validatecommand=(vcmd, '%P'))
        self.group_number.focus_set()
        self.group_number.place(x=190, y=40)

        Label(text="Section", font=('Arial Rounded MT Bold', 10)).place(x=80, y=70)
        self.section = Entry(textvar=self.section)
        self.section.place(x=190, y=70)

        Button(text="Add", command=self.add).place(x=180, y=110)

        self.newrootregs.mainloop()

    def callback(register, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            messagebox.showinfo("Alert", "Number's Only")
            return False

    def show_records(self):
        self.root.destroy()
        self.newrootSR = Tk()
        self.newrootSR.title('Current Records')
        self.newrootSR.geometry("500x500")

        Label(text='List of borrowed items:', font=('Times New Roman', 20, 'bold')).place(x=115, y=30)

        tree=Treeview(self.newrootSR, show='headings')
        tree.place(x=50, y=110)

        vsb = Scrollbar(self.newrootSR, orient='vertical', command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)
        tree['columns'] = ("one", "two", 'three', 'four')

        tree.column("one", width=100, minwidth=270, stretch=tk.NO)
        tree.column("two", width=100, minwidth=100, stretch=tk.NO)
        tree.column("three", width=100, minwidth=100, stretch=tk.NO)
        tree.column("four", width=70, minwidth=70, stretch=tk.NO)

        tree.heading("#1", text="Items", anchor=tk.W)
        tree.heading("#2", text="Quantity", anchor=tk.W)
        tree.heading("#3", text="Borrower", anchor=tk.W)
        tree.heading("#4", text="Group no.", anchor=tk.W)
        # Database side
        conn = sqlite3.connect('User_Database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, quantity, section, group_number FROM groups_items, groups WHERE groups.pid = groups_items.pid')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            tree.insert('',1, values=row)
        conn.close()
        
        Button(self.newrootSR, text='Back to main', width=15, command=self.return_self).place(x=200, y=450)

        self.newrootSR.mainloop()

 
    def withdraw(self):
        check = self.user_check()
        groupno = str(self.group_number.get())
        section = str(self.section.get())
        if (len(groupno) == 0 or len(section) == 0):
            messagebox.showinfo('Warning', 'Please enter a valid group number and section.')
            self.newrootWD.destroy()
        elif check == False:
            messagebox.showinfo('Warning', 'Group number and section does not exist. Please register')
            self.newrootWD.destroy()       

        self.root.destroy()
        self.newrootWD = Tk()
        self.newrootWD.title("Borrowing Menu")
        self.newrootWD.geometry("545x500")

        Label(text='Borrowing Items', font=("Times New Roman", 20, "bold")).place(x=165, y=30)

        Label(text='Laptop', font=('Arial Rounded MT Bold', 10)).place(x=100, y=100)
        self.laptopNum = IntVar()
        self.laptopcom = Combobox(state="readonly", width=3, textvariable=self.laptopNum)
        self.laptopcom['values'] = (0, 1, 2, 3, 4, 5)
        self.laptopcom.current(0)
        self.laptopcom.place(x=152, y=100)

        Label(text='digital ohmmeter', font=('Arial Rounded MT Bold', 10)).place(x=100, y=150)
        self.digohmcomNum = IntVar()
        self.digohmcom = Combobox(state="readonly", width=3, textvariable=self.digohmcomNum)
        self.digohmcom['values'] = (0, 1, 2, 3, 4, 5)
        self.digohmcom.current(0)
        self.digohmcom.place(x=217, y=150)

        Label(text='force sensor with', font=('Arial Rounded MT Bold', 10)).place(x=100, y=200)
        Label(text='USB link', font=('Arial Rounded MT Bold', 10)).place(x=120, y=215)
        self.fsensmcomNum = IntVar()
        self.fsensmcom = Combobox(state="readonly", width=3, textvariable=self.fsensmcomNum)
        self.fsensmcom['values'] = (0, 1, 2, 3, 4, 5)
        self.fsensmcom.current(0)
        self.fsensmcom.place(x=219, y=208)

        Label(text='force table', font=('Arial Rounded MT Bold', 10)).place(x=100, y=260)
        self.ftabcomNum = IntVar()
        self.ftabcom = Combobox(state="readonly", width=3, textvariable=self.ftabcomNum)
        self.ftabcom['values'] = (0, 1, 2, 3, 4, 5)
        self.ftabcom.current(0)
        self.ftabcom.place(x=177, y=260)

        Label(text='linear expansion', font=('Arial Rounded MT Bold', 10)).place(x=100, y=300)
        Label(text='apparatus', font=('Arial Rounded MT Bold', 10)).place(x=115, y=315)
        self.leacomNum = IntVar()
        self.leacom = Combobox(state="readonly", width=3, textvariable=self.leacomNum)
        self.leacom['values'] = (0, 1, 2, 3, 4, 5)
        self.leacom.current(0)
        self.leacom.place(x=215, y=309)

        Label(text='meter stick', font=('Arial Rounded MT Bold', 10)).place(x=300, y=100)
        Label(text='apparatus', font=('Arial Rounded MT Bold', 10)).place(x=115, y=315)
        self.mstcomNum = IntVar()
        self.mstcom = Combobox(state="readonly", width=3, textvariable=self.mstcomNum)
        self.mstcom['values'] = (0, 1, 2, 3, 4, 5)
        self.mstcom.current(0)
        self.mstcom.place(x=380, y=100)

        Label(text='resistor', font=('Arial Rounded MT Bold', 10)).place(x=300, y=150)
        self.ressomNum = IntVar()
        self.ressom = Combobox(state="readonly", width=3, textvariable=self.ressomNum)
        self.ressom['values'] = (0, 1, 2, 3, 4, 5)
        self.ressom.current(0)
        self.ressom.place(x=357, y=150)

        Label(text='rotary motion', font=('Arial Rounded MT Bold', 10)).place(x=300, y=200)
        Label(text='sensor', font=('Arial Rounded MT Bold', 10)).place(x=320, y=215)
        self.rescomNum = IntVar()
        self.rescom = Combobox(state="readonly", width=3, textvariable=self.rescomNum)
        self.rescom['values'] = (0, 1, 2, 3, 4, 5)
        self.rescom.current(0)
        self.rescom.place(x=395, y=209)

        Label(text='set of masses', font=('Arial Rounded MT Bold', 10)).place(x=300, y=260)
        self.somcomNum = IntVar()
        self.somcom = Combobox(state="readonly", width=3, textvariable=self.somcomNum)
        self.somcom['values'] = (0, 1, 2, 3, 4, 5)
        self.somcom.current(0)
        self.somcom.place(x=393, y=260)

        Label(text='temperature', font=('Arial Rounded MT Bold', 10)).place(x=300, y=300)
        Label(text='sensor', font=('Arial Rounded MT Bold', 10)).place(x=320, y=315)
        self.temcomNum = IntVar()
        self.temcom = Combobox(state="readonly", width=3, textvariable=self.temcomNum)
        self.temcom['values'] = (0, 1, 2, 3, 4, 5)
        self.temcom.current(0)
        self.temcom.place(x=389, y=309)

        Button(text='Borrow', command=self.borrow).place(x=230, y=380)


    def borrow(self):
        self.newrootWD.destroy()
        self.newroot = Tk()
        application = PLMS_Menu(self.newroot)

        # Initialization of Variables
        groupno = self.group_number.get()
        section = self.section.get()

        # Laptop
        laptopNum = self.laptopNum.get()
        update_withdraw('laptop', groupno, section, laptopNum, id=1)
        if laptopNum > 0:
            messagebox.showinfo('Success', 'Item Laptop has been deployed.')

        # Digital Ohmmeter
        digohmcomNum = self.digohmcomNum.get()
        update_withdraw('digital_ohmmeter', groupno, section, digohmcomNum, id=2)
        if digohmcomNum > 0:
            messagebox.showinfo('Success', 'Item Digital Ohmmeter has been deployed.')

        # Force Sensor
        fsensmcomNum = self.fsensmcomNum.get()
        update_withdraw('force_sensor', groupno, section, fsensmcomNum, id=3)
        if fsensmcomNum > 0:
            messagebox.showinfo('Success', 'Item Force Sensor has been deployed.')

        # Force Table
        ftabcomNum = self.ftabcomNum.get()
        update_withdraw('force_table', groupno, section, ftabcomNum, id=6)
        if ftabcomNum > 0:
            messagebox.showinfo('Success', 'Item Force Table has been deployed.')

        # Linear Expansion Apparatus
        leacomNum = self.leacomNum.get()
        update_withdraw('linear_expansion_apparatus', groupno, section, leacomNum, id=4)
        if leacomNum > 0:
            messagebox.showinfo('Success', 'Item Linear Expansion Apparatus has been deployed.')

        # Meter stick
        mstcomNum = self.mstcomNum.get()
        update_withdraw('meter_stick_apparatus', groupno, section, mstcomNum, id=5)
        if mstcomNum > 0:
            messagebox.showinfo('Success', 'Item Meter stick has been deployed.')

        # Resistor
        ressomNum = self.ressomNum.get()
        update_withdraw('resistor', groupno, section, ressomNum, id=7)
        if ressomNum > 0:
            messagebox.showinfo('Success', 'Item Resistor has been deployed.')

        # Rotary Motion Sensor
        rescomNum = self.rescomNum.get()
        update_withdraw('rotary_motion_sensor', groupno, section, rescomNum, id=8)
        if rescomNum > 0:
            messagebox.showinfo('Success', 'Item Rotary Motion Sensor has been deployed.')

        # Set of Masses
        somcomNum = self.somcomNum.get()
        update_withdraw('set_of_masses', groupno, section, somcomNum, id=9)
        if somcomNum > 0:
            messagebox.showinfo('Success', 'Item Set of Masses has been deployed.')

        # Temperature Sensor
        temcomNum = self.temcomNum.get() 
        update_withdraw('temperature_sensors', groupno, section, temcomNum, id=10)
        if temcomNum > 0:
            messagebox.showinfo('Success', 'Item Temperature sensor has been deployed.')


        self.newroot.mainloop()

    def deposite(self):
        check = self.user_check()
        groupno = str(self.group_number.get())
        section = str(self.section.get())
        if (len(groupno) == 0 or len(section) == 0):
            messagebox.showinfo('Warning', 'Please enter a valid group number and section.')
            self.newrootDP.destroy()
        elif check == False:
            messagebox.showinfo('Warning', 'Group number and section does not exist. Please register')
            self.newrootDP.destroy()       

        self.root.destroy()
        self.newrootDP = Tk()
        self.newrootDP.title("Deposite Menu")
        self.newrootDP.geometry("545x500")

        Label(text='Deposite Items', font=("Times New Roman", 20, "bold")).place(x=165, y=20)
        Label(text='Check the box if borrowed', font=("Times New Roman", 10)).place(x=180, y=60)

        Label(text='Laptop', font=('Arial Rounded MT Bold', 10)).place(x=100, y=100)
        self.laptopNum = IntVar()
        self.laptopcom = Combobox(state="readonly", width=3, textvariable=self.laptopNum)
        self.laptopcom['values'] = (0, 1, 2, 3, 4, 5)
        self.laptopcom.current(0)
        self.laptopcom.place(x=152, y=100)

        chklp = IntVar()
        self.chkLp = Checkbutton(variable=chklp)
        self.chkLp.deselect()
        self.chkLp.place(x=55, y=100)

        Label(text='digital ohmmeter', font=('Arial Rounded MT Bold', 10)).place(x=100, y=150)
        self.digohmcomNum = IntVar()
        self.digohmcom = Combobox(state="readonly", width=3, textvariable=self.digohmcomNum)
        self.digohmcom['values'] = (0, 1, 2, 3, 4, 5)
        self.digohmcom.current(0)
        self.digohmcom.place(x=217, y=150)

        chkdo = IntVar()
        self.chkLp = Checkbutton(variable=chkdo)
        self.chkLp.deselect()
        self.chkLp.place(x=55, y=150)

        Label(text='force sensor with', font=('Arial Rounded MT Bold', 10)).place(x=100, y=200)
        Label(text='USB link', font=('Arial Rounded MT Bold', 10)).place(x=120, y=215)
        self.fsensmcomNum = IntVar()
        self.fsensmcom = Combobox(state="readonly", width=3, textvariable=self.fsensmcomNum)
        self.fsensmcom['values'] = (0, 1, 2, 3, 4, 5)
        self.fsensmcom.current(0)
        self.fsensmcom.place(x=219, y=208)

        chkfs = IntVar()
        self.chkLp = Checkbutton(variable=chkfs)
        self.chkLp.deselect()
        self.chkLp.place(x=55, y=200)

        Label(text='force table', font=('Arial Rounded MT Bold', 10)).place(x=100, y=260)
        self.ftabcomNum = IntVar()
        self.ftabcom = Combobox(state="readonly", width=3, textvariable=self.ftabcomNum)
        self.ftabcom['values'] = (0, 1, 2, 3, 4, 5)
        self.ftabcom.current(0)
        self.ftabcom.place(x=177, y=260)

        chkft = IntVar()
        self.chkLp = Checkbutton(variable=chkft)
        self.chkLp.deselect()
        self.chkLp.place(x=55, y=260)

        Label(text='linear expansion', font=('Arial Rounded MT Bold', 10)).place(x=100, y=300)
        Label(text='apparatus', font=('Arial Rounded MT Bold', 10)).place(x=115, y=315)
        self.leacomNum = IntVar()
        self.leacom = Combobox(state="readonly", width=3, textvariable=self.leacomNum)
        self.leacom['values'] = (0, 1, 2, 3, 4, 5)
        self.leacom.current(0)
        self.leacom.place(x=215, y=309)

        chkle = IntVar()
        self.chkLp = Checkbutton(variable=chkle)
        self.chkLp.deselect()
        self.chkLp.place(x=55, y=300)

        Label(text='meter stick', font=('Arial Rounded MT Bold', 10)).place(x=300, y=100)
        Label(text='apparatus', font=('Arial Rounded MT Bold', 10)).place(x=115, y=315)
        self.mstcomNum = IntVar()
        self.mstcom = Combobox(state="readonly", width=3, textvariable=self.mstcomNum)
        self.mstcom['values'] = (0, 1, 2, 3, 4, 5)
        self.mstcom.current(0)
        self.mstcom.place(x=380, y=100)

        chkms = IntVar()
        self.chkLp = Checkbutton(variable=chkms)
        self.chkLp.deselect()
        self.chkLp.place(x=295, y=100)

        Label(text='resistor', font=('Arial Rounded MT Bold', 10)).place(x=300, y=150)
        self.ressomNum = IntVar()
        self.ressom = Combobox(state="readonly", width=3, textvariable=self.ressomNum)
        self.ressom['values'] = (0, 1, 2, 3, 4, 5)
        self.ressom.current(0)
        self.ressom.place(x=357, y=150)

        chkr = IntVar()
        self.chkLp = Checkbutton(variable=chkr)
        self.chkLp.deselect()
        self.chkLp.place(x=295, y=150)

        Label(text='rotary motion', font=('Arial Rounded MT Bold', 10)).place(x=300, y=200)
        Label(text='sensor', font=('Arial Rounded MT Bold', 10)).place(x=320, y=215)
        self.rescomNum = IntVar()
        self.rescom = Combobox(state="readonly", width=3, textvariable=self.rescomNum)
        self.rescom['values'] = (0, 1, 2, 3, 4, 5)
        self.rescom.current(0)
        self.rescom.place(x=395, y=209)

        chkrms = IntVar()
        self.chkLp = Checkbutton(variable=chkrms)
        self.chkLp.deselect()
        self.chkLp.place(x=295, y=200)

        Label(text='set of masses', font=('Arial Rounded MT Bold', 10)).place(x=300, y=260)
        self.somcomNum = IntVar()
        self.somcom = Combobox(state="readonly", width=3, textvariable=self.somcomNum)
        self.somcom['values'] = (0, 1, 2, 3, 4, 5)
        self.somcom.current(0)
        self.somcom.place(x=393, y=260)

        chksm = IntVar()
        self.chkLp = Checkbutton(variable=chksm)
        self.chkLp.deselect()
        self.chkLp.place(x=295, y=260)

        Label(text='temperature', font=('Arial Rounded MT Bold', 10)).place(x=300, y=300)
        Label(text='sensor', font=('Arial Rounded MT Bold', 10)).place(x=320, y=315)
        self.temcomNum = IntVar()
        self.temcom = Combobox(state="readonly", width=3, textvariable=self.temcomNum)
        self.temcom['values'] = (0, 1, 2, 3, 4, 5)
        self.temcom.current(0)
        self.temcom.place(x=389, y=309)
        chkts = IntVar()
        self.chkLp = Checkbutton(variable=chkts)
        self.chkLp.deselect()
        self.chkLp.place(x=295, y=300)

        Button(text='Deposite', command=self.balik).place(x=230, y=380)

    def balik(self):
        self.newrootDP.destroy()
        self.newroot = Tk()
        application = PLMS_Menu(self.newroot)
        groupno = self.group_number.get()
        section = self.section.get()

        # Laptop
        laptopNum = self.laptopNum.get()
        update_deposit('laptop', groupno, section, laptopNum, id=1)
        if laptopNum > 0:
            messagebox.showinfo('Success', 'Item Laptop has been returned.')

        # Digital Ohmmeter
        digohmcomNum = self.digohmcomNum.get()
        update_deposit('digital_ohmmeter', groupno, section, digohmcomNum, id=2)
        if digohmcomNum > 0:
            messagebox.showinfo('Success', 'Item Digital Ohmmeter has been returned.')
        # Force Sensor
        fsensmcomNum = self.fsensmcomNum.get()
        update_deposit('force_sensor', groupno, section, fsensmcomNum, id=3)
        if fsensmcomNum > 0:
            messagebox.showinfo('Success', 'Item Force Sensor has been returned.')
        # Force Table
        ftabcomNum = self.ftabcomNum.get()
        update_deposit('force_table', groupno, section, ftabcomNum, id=6)
        if ftabcomNum > 0:
            messagebox.showinfo('Success', 'Item Force Table has been returned.')
        # Linear Expansion Apparatus
        leacomNum = self.leacomNum.get()
        update_deposit('linear_expansion_apparatus', groupno, section, leacomNum, id=4)
        if leacomNum > 0:
            messagebox.showinfo('Success', 'Item Linear Expansion Apparatus has been returned.')
        # Meter stick
        mstcomNum = self.mstcomNum.get()
        update_deposit('meter_stick_apparatus', groupno, section, mstcomNum, id=5)
        if mstcomNum > 0:
            messagebox.showinfo('Success', 'Item Meter stick has been returned.')
        # Resistor
        ressomNum = self.ressomNum.get()
        update_deposit('resistor', groupno, section, ressomNum, id=7)
        if ressomNum > 0:
            messagebox.showinfo('Success', 'Item Resistor has been returned.')
        # Rotary Motion Sensor
        rescomNum = self.rescomNum.get()
        update_deposit('rotary_motion_sensor', groupno, section, rescomNum, id=8)
        if rescomNum > 0:
            messagebox.showinfo('Success', 'Item Rotary Motion Sensor has been returned.')
        # Set of Masses
        somcomNum = self.somcomNum.get()
        update_deposit('set_of_masses', groupno, section, somcomNum, id=9)
        if somcomNum > 0:
            messagebox.showinfo('Success', 'Item Set of Masses has been returned.')
        # Temperature Sensor
        temcomNum = self.temcomNum.get() 
        update_deposit('temperature_sensors', groupno, section, temcomNum, id=10)
        if temcomNum > 0:
            messagebox.showinfo('Success', 'Item Temperature sensor has been returned.')

        self.newroot.mainloop()

    def add(self):
        groupno = self.group_number.get()
        section = self.section.get()

        conn = sqlite3.connect('User_Database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO groups(group_number, section) VALUES(?,?)", (groupno, section))
        conn.commit()
        conn.close()

        self.newrootregs.destroy()
        self.root = Tk()
        application = PLMS_Menu(self.root)
        self.root.mainloop()

    def storage(self):
        self.root.destroy()
        self.newrootstrg = Tk()
        self.newrootstrg.mainloop()

items = [
    # Input your items with the following format: 
    # Item Name, quantity, available? 1 for yes 0 for no
    ('laptop', 5),
    ('digital_ohmmeter', 5),
    ('force_sensor', 5),
    ('linear_expansion_apparatus', 5),
    ('meter_stick_apparatus', 5,),
    ('force_table', 5),
    ('resistor', 5),
    ('rotary_motion_sensor', 5),
    ('set_of_masses', 5),
    ('temperature_sensor', 5),
]


def init_db():
    conn = sqlite3.connect("User_Database.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = 1")
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups(
                pid INTEGER PRIMARY KEY,
                group_number TEXT,
                section TEXT
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY,
                item_name TEXT NOT NULL,
                quantity INTEGER
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups_items(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER,
                pid INTEGER,
                item_id INTEGER,
                FOREIGN KEY (pid) REFERENCES groups(pid)
                ON DELETE CASCADE,
                FOREIGN KEY (item_id) REFERENCES items(id)
                ON DELETE CASCADE
            )
        """)
    if DEBUG:
        cursor.executemany("INSERT OR IGNORE INTO items(item_name, quantity) VALUES(?,?)", items)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    root = Tk()
    application = PLMS_Menu(root)
    root.mainloop()
