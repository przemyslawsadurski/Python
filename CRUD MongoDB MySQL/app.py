from tkinter import *
import tkinter as tk
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
import pymongo
from tkinter import messagebox

root = tk.Tk()
root.geometry("600x600")
root.title("Projekt, PythonGUI + MySQL + MongoDB ")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["python_gui"]
mycol = mydb["student"]

#MySQL
name = Label(root,text="MySQL",font=('bold',10))
name.place(x=10,y=260)

id = Label(root,text='Enter ID', font=('bold',10))
id.place(x=20,y=290)

name = Label(root,text='Enter name', font=('bold',10))
name.place(x=20,y=320)

phone = Label(root,text='Enter phone', font=('bold',10))
phone.place(x=20,y=350)

e_id = Entry()
e_id.place(x=150,y=290)

e_name = Entry()
e_name.place(x=150,y=320)

e_phone = Entry()
e_phone.place(x=150,y=350)

def insert():
    id = e_id.get()
    name = e_name.get()
    phone = e_phone.get()
    if(id=="" or name=="" or phone==""):
        MessageBox.showinfo("Blad przy wywolaniu polecenia insert" ,"wszystkie pola sa wymagane")
    else:
        con = mysql.connect(host="localhost",user="root",password="",database="pythongui")
        cursor = con.cursor()
        cursor.execute("insert into student values('"+id+"','"+name+"','"+phone+"')")
        cursor.execute("commit")
        e_id.delete(0,'end')
        e_name.delete(0,'end')
        e_phone.delete(0,'end')
        showmysql()
        MessageBox.showinfo("Akcja - Insert" ,"Wstawianie rekordu powiodlo sie!")
        con.close()

def update():
    id = e_id.get()
    name = e_name.get()
    phone = e_phone.get()
    if(id=="" or name=="" or phone==""):
        MessageBox.showinfo("Blad przy wywolaniu polecenia update","wszystkie pola sa wymagane")
    else:
        con = mysql.connect(host="localhost",user="root",password="",database="pythongui")
        cursor = con.cursor()
        cursor.execute("update student set name='"+name+"', phone='"+phone+"' where id='"+id+"'")
        cursor.execute("commit")
        e_id.delete(0,'end')
        e_name.delete(0,'end')
        e_phone.delete(0,'end')
        showmysql()
        MessageBox.showinfo("Akcja - Update","Aktualizacja rekordu powiodla sie!")
        con.close()

def read():
    if(e_id.get()==""):
        MessageBox.showinfo("Akcja odczytu nieudana","konieczne jest podanie ID")
    else:
        con = mysql.connect(host="localhost",user="root",password="",database="pythongui")
        cursor = con.cursor()
        cursor.execute("select * from student where id='"+e_id.get()+"'")
        rows = cursor.fetchall()
        for row in rows:
            e_name.insert(0,row[1])
            e_phone.insert(0,row[2])
        con.close()


def delete():
    if(e_id.get()==""):
        MessageBox.showinfo("Akcja usuwania nieudana", "konieczne jest podanie ID")
    else:
        con = mysql.connect(host="localhost",user="root",password="",database="pythongui")
        cursor = con.cursor()
        cursor.execute("delete from student where id='"+e_id.get()+"'")
        cursor.execute("commit")
        e_id.delete(0,'end')
        e_name.delete(0,'end')
        e_phone.delete(0,'end')
        showmysql()
        MessageBox.showinfo("Akcja - Delete", "Usuniecie rekordu powiodlo sie!")
        con.close()

def showmysql():
    con = mysql.connect(host="localhost", user="root", password="",database="pythongui")
    cursor = con.cursor()
    cursor.execute("Select * from student")
    rows = cursor.fetchall()
    listmysql.delete(0,listmysql.size())
    for row in rows:
        insertData = str(row[0])+'    '+row[1]+'  '+str(row[2])
        listmysql.insert(listmysql.size()+1, insertData)
    con.close()



insert = Button(root, text="Insert", font=("italic", 10), bg="white", command=insert)
insert.place(x=20,y=400)

update = Button(root,text="Update", font=("italic", 10), bg="white", command=update)
update.place(x=80,y=400)

read = Button(root,text="Read", font=("italic", 10), bg="white", command=read)
read.place(x=140,y=400)

delete = Button(root,text="Delete", font=("italic",10), bg="white", command=delete)
delete.place(x=200,y=400)


listmysql = Listbox(root)
listmysql.place(x=300,y=290)
showmysql()

#mongo
label = tk.Label(root, text="MongoDB", width=10, height=1)
label.grid(column=0,row=0)
label = tk.Label(root, text="Student ID", width=10, height=1)
label.grid(column=1,row=2)
cid = tk.StringVar()
custid = tk.Entry(root, textvariable = cid)
custid.grid(column=2,row=2)
custid.configure(state=tk.DISABLED)

label = tk.Label(root, text="Student name", width=15, height=1)
label.grid(column=1,row=3)
cname = tk.StringVar()
custname = tk.Entry(root, textvariable = cname)
custname.grid(column=2,row=3)

label = tk.Label(root, text="Student email", width=15, height=1)
label.grid(column=1,row=4)
cemail = tk.StringVar()
custemail = tk.Entry(root, textvariable = cemail)
custemail.grid(column=2,row=4)




lst = [['ID','Name','Phone']]

def msgbox(titlebar,msg):
    result = messagebox.askokcancel(title=titlebar,message=msg)
    return result

def callback(event):
    li = []
    li = event.widget._values
    cid.set(lst[li[1]][0])
    cname.set(lst[li[1]][1])
    cemail.set(lst[li[1]][2])

def creategrid(n):
    lst.clear()
    lst.append(['ID','Name','Phone'])
    cursor = mycol.find({})
    for text_fromDB in cursor:
        studid = str(text_fromDB['studid'])
        studname = str(text_fromDB['studname'].encode('utf-8').decode("utf-8"))
        studemail = str(text_fromDB['studemail'].encode('utf-8').decode("utf-8"))
        lst.append([studid,studname,studemail])
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            mgrid = tk.Entry(root, width=10)
            mgrid.insert(tk.END,lst[i][j])
            mgrid._values = mgrid.get(), i
            mgrid.grid(row=i+7,column=j+6)
            mgrid.bind("<Button-1>", callback)
    if n==1:
        for label in root.grid_slaves():
            if int(label.grid_info()["row"]) > 6:
                label.grid_forget()

def saveM():
    r = msgbox("save record?", "record")
    if r == True:
        newid = mycol.count_documents({})
        if newid!=0:
            newid = mycol.find_one(sort=[("studid",-1)])["studid"]
        id = newid+1
        cid.set(id)
        mydict = {"studid": int(custid.get()), "studname": custname.get(),"studemail": custemail.get()}
        x = mycol.insert_one(mydict)
        creategrid(1)
        creategrid(0)


def deleteM():
    r = msgbox("Delete?","record")
    if r == True:
        myquery = {"studid":int(custid.get())}
        mycol.delete_one(myquery)
        creategrid(1)
        creategrid(0)

def updateM():
    r = msgbox("Update?","record")
    if r == True:
        myquery = {"studid": int(custid.get())}
        newvalues = { "$set": {"studname": custname.get()}}
        mycol.update_one(myquery, newvalues)
        newvalues = {"$set": {"studemail": custemail.get()}}
        mycol.update_one(myquery,newvalues)
        creategrid(1)
        creategrid(0)
    

creategrid(0)
savebutton = tk.Button(text="Save", command = saveM)
savebutton.grid(column=1,row=6)
savebutton = tk.Button(text="Delete", command = deleteM)
savebutton.grid(column=2,row=6)
savebutton = tk.Button(text="Update", command = updateM)
savebutton.grid(column=3,row=6)
 


root.mainloop()