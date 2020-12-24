import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from functools import partial
import datetime

def createtable():
    conn = psycopg2.connect("dbname='routine' user='postgres' password='postgres' port='5432' host='localhost' ")
    cur = conn.cursor()
    cur.execute(" CREATE TABLE sahil(date TEXT ,exercise TEXT ,earnings INTEGER ,study TEXT) ")
    conn.commit()
    conn.close()

def insert(date,exercise,earnings,study):
    date = date.get()
    if date=="":
        date = datetime.date.today().strftime("%d-%m-%y")
    elif len(date) > 8 or any(c.isalpha() for c in date):
        l6.config(text='Date should be in dd-mm-yy format')
        raise Exception("WrongDateFound")
    exercise = exercise.get()
    if exercise=="":
        exercise ="N/A"
    elif len(exercise) > 20 or any(c.isdigit() for c in exercise):
        l6.config(text='Exercise cannot contain number')
        raise Exception("ExerciseNumFOund")
    earnings = earnings.get()
    if earnings=="":
        earnings = 0
    study = study.get()
    if study == "":
        study = "N/A"
    conn = psycopg2.connect("dbname='routine' user='postgres' password='postgres' port='5432' host='localhost' ")
    cur = conn.cursor()
    try:
        cur.execute("select * from sahil where date=%s and exercise=%s and earnings=%s and study=%s",(date,exercise,earnings,study,))
        rows = cur.fetchall()
        if len(rows)>0:
            l6.config(text='Same entry already found in database')
        else:
            cur.execute( " INSERT INTO sahil VALUES(%s,%s,%s,%s) ",(date,exercise,earnings,study) )
        conn.commit()
        conn.close()
    except:
        l6.config(text='Earnings cannot be letters')
    view()

def view():
    conn = psycopg2.connect("dbname='routine' user='postgres' password='postgres' port='5432' host='localhost' ")
    cur = conn.cursor()
    cur.execute( " SELECT * FROM sahil " )
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    list1.delete(0, END)
    for i in rows:
        list1.insert(0,i)

def refresh():
    date.set("")
    exercise.set("")
    earnings.set("")
    study.set("")
    l6.configure(text="Nothing selected ")
    conn = psycopg2.connect("dbname='routine' user='postgres' password='postgres' port='5432' host='localhost' ")
    cur = conn.cursor()
    cur.execute( " SELECT * FROM sahil " )
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    list1.delete(0, END)
    for i in rows:
        list1.insert(0,i)

def delete(date,exercise,earnings,study):
    date = date.get()
    exercise = exercise.get()
    earnings = earnings.get()
    study = study.get()
    conn = psycopg2.connect("dbname='routine' user='postgres' password='postgres' port='5432' host='localhost' ")
    cur = conn.cursor()
    if not exercise and not earnings and not study:
        cur.execute(" DELETE from sahil WHERE date=%s ",(date,))
        rows = cur.fetchall()
    elif not date and not earnings and not study:
        cur.execute(" delete from sahil WHERE exercise=%s ",(exercise,))
        rows = cur.fetchall()
    elif not date and not exercise and not study:
        cur.execute(" delete from sahil WHERE earnings=%s ",(earnings,))
        rows = cur.fetchall()
    elif not date and not earnings and not exercise:
        cur.execute(" delete from sahil WHERE study=%s ",(study,))
        rows = cur.fetchall()
    elif not date and not exercise:
        cur.execute(" delete from sahil WHERE study=%s AND earnings=%s ",(study,earnings,))
        rows = cur.fetchall()
    elif not date and not earnings:
        cur.execute(" delete from sahil WHERE exercise=%s AND study=%s ",(exercise,study,))
        rows = cur.fetchall()
    elif not date and not study:
        cur.execute(" delete from sahil WHERE exercise=%s AND earnings=%s ",(exercise,earnings,))
        rows = cur.fetchall()
    elif not date and not exercise:
        cur.execute(" delete from sahil WHERE study=%s AND earnings=%s ",(study,earnings,))
        rows = cur.fetchall()
    elif not exercise and not earnings:
        cur.execute(" delete from sahil WHERE date=%s AND study=%s ",(date,study,))
        rows = cur.fetchall()
    elif not study and not exercise:
        cur.execute(" delete from sahil WHERE date=%s AND earnings=%s ",(date,earnings,))
        rows = cur.fetchall()
    elif not study and not earnings:
        cur.execute(" delete from sahil WHERE date=%s AND exercise=%s ",(date,exercise,))
        rows = cur.fetchall()
    elif not date:
        cur.execute(" delete from sahil WHERE study=%s AND exercise=%s AND earnings=%s ",(study,exercise,earnings,))
        rows = cur.fetchall()
    elif not exercise:
        cur.execute(" delete from sahil WHERE study=%s AND date=%s AND earnings=%s ",(study,date,earnings,))
        rows = cur.fetchall()
    elif not earnings:
        cur.execute(" delete from sahil WHERE study=%s AND exercise=%s AND date=%s ",(study,exercise,date,))
        rows = cur.fetchall()
    else:
        cur.execute(" delete from sahil WHERE date=%s AND exercise=%s AND earnings=%s ",(date,exercise,earnings,))
        rows = cur.fetchall()
    conn.commit()
    conn.close()
    view()

def update(list1):
    list1 = list1.get(ACTIVE)
    if len(list1) == 0:
        l6.config(text='Please select something from list')
        raise Exception("NoSelection")
    date.set(list1[0])
    exercise.set(list1[1])
    earnings.set(list1[2])
    study.set(list1[3])
    conn = psycopg2.connect("dbname='routine' user='postgres' password='postgres' port='5432' host='localhost' ")
    cur = conn.cursor()
    cur.execute( " UPDATE sahil SET date=%s , exercise=%s , earnings=%s , study=%s WHERE date=%s ",(list1[0],list1[1],list1[2],list1[3],list1[0]) )
    conn.commit()
    conn.close()
    view()

def search(date,exercise,earnings,study):
    date = date.get()
    exercise = exercise.get()
    earnings = earnings.get()
    study = study.get()
    conn = psycopg2.connect("dbname='routine' user='postgres' password='postgres' port='5432' host='localhost' ")
    cur = conn.cursor()
    if not exercise and not earnings and not study:
        cur.execute(" SELECT * from sahil WHERE date=%s ",(date,))
        rows = cur.fetchall()
    elif not date and not earnings and not study:
        cur.execute(" SELECT * from sahil WHERE exercise=%s ",(exercise,))
        rows = cur.fetchall()
    elif not date and not exercise and not study:
        cur.execute(" SELECT * from sahil WHERE earnings=%s ",(earnings,))
        rows = cur.fetchall()
    elif not date and not earnings and not exercise:
        cur.execute(" SELECT * from sahil WHERE study=%s ",(study,))
        rows = cur.fetchall()
    elif not date and not exercise:
        cur.execute(" SELECT * from sahil WHERE study=%s AND earnings=%s ",(study,earnings,))
        rows = cur.fetchall()
    elif not date and not earnings:
        cur.execute(" SELECT * from sahil WHERE exercise=%s AND study=%s ",(exercise,study,))
        rows = cur.fetchall()
    elif not date and not study:
        cur.execute(" SELECT * from sahil WHERE exercise=%s AND earnings=%s ",(exercise,earnings,))
        rows = cur.fetchall()
    elif not date and not exercise:
        cur.execute(" SELECT * from sahil WHERE study=%s AND earnings=%s ",(study,earnings,))
        rows = cur.fetchall()
    elif not exercise and not earnings:
        cur.execute(" SELECT * from sahil WHERE date=%s AND study=%s ",(date,study,))
        rows = cur.fetchall()
    elif not study and not exercise:
        cur.execute(" SELECT * from sahil WHERE date=%s AND earnings=%s ",(date,earnings,))
        rows = cur.fetchall()
    elif not study and not earnings:
        cur.execute(" SELECT * from sahil WHERE date=%s AND exercise=%s ",(date,exercise,))
        rows = cur.fetchall()
    elif not date:
        cur.execute(" SELECT * from sahil WHERE study=%s AND exercise=%s AND earnings=%s ",(study,exercise,earnings,))
        rows = cur.fetchall()
    elif not exercise:
        cur.execute(" SELECT * from sahil WHERE study=%s AND date=%s AND earnings=%s ",(study,date,earnings,))
        rows = cur.fetchall()
    elif not earnings:
        cur.execute(" SELECT * from sahil WHERE study=%s AND exercise=%s AND date=%s ",(study,exercise,date,))
        rows = cur.fetchall()
    else:
        cur.execute(" SELECT * from sahil WHERE date=%s AND exercise=%s AND earnings=%s ",(date,exercise,earnings,))
        rows = cur.fetchall()
    if not rows:
        l6.config(text='Nothing matched your search')
    list1.delete(0, END)
    for i in rows:
        list1.insert(0,i)
    conn.commit()
    conn.close()

def callback(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        date.set(data[0])
        exercise.set(data[1])
        earnings.set(data[2])
        study.set(data[3])
        l6.configure(text=data)
    else:
        date.set("")
        exercise.set("")
        earnings.set("")
        study.set("")
        l6.configure(text="Nothing selected ")

def test(date,exercise,earnings,study):
    date = date.get()
    exercise = exercise.get()
    earnings = earnings.get()
    study = study.get()
    string = "testing data : "+date +" "+exercise+ " "+earnings+" "+study
    l6.config(text=string)
    view()


win = Tk()
win.geometry('1200x500')


date = StringVar()
exercise = StringVar()
earnings = StringVar()
study = StringVar()

l1 = Label(win,text='Routine',font='Courier 25',fg='blue')
l2 = Label(win,text='Date :',font='Times 16',fg='black')
e1 = Entry(win,bg='lightgrey',font='Times 16', textvariable=date )
l3 = Label(win,text='Exercise :',font='Times 16',fg='black')
e2 = Entry(win,bg='lightgrey',font='Times 16', textvariable=exercise )
l4 = Label(win,text='Earnings :',font='Times 16',fg='black')
e3 = Entry(win,bg='lightgrey',font='Times 16', textvariable=earnings)
l5 = Label(win,text='Language :',font='Times 16',fg='black')
combo1 = ttk.Combobox(win ,font='Times 16', textvariable = study)
combo1['values'] = ('C','C++','JAVA','Python','HTML/CSS','JAVAScript')
frame1 = Frame(win)
frame1.place(x=10,y=150)
scroll = Scrollbar(frame1)
list1 = Listbox(frame1, font='Times 14',bg="light yellow", width=100 ,yscrollcommand=scroll.set)
scroll.config(command=list1.yview)
list1.bind('<FocusOut>', lambda e: list1.selection_clear(0, END)) 
list1.bind("<<ListboxSelect>>", callback)
insert = partial(insert,date,exercise,earnings,study)
b1 = Button(win,text='Insert',font='Times 14' , command=insert)
search = partial(search,date,exercise,earnings,study)
b2 = Button(win,text='Search',font='Times 14' , command=search )
delete = partial(delete,date,exercise,earnings,study)
b3 = Button(win,text='Delete',font='Times 14' , command=delete)
update = partial(update,list1)
b4 = Button(win,text='Update',font='Times 14' ,command=test)
b5 = Button(win,text='Close',font='Times 14' , command=win.destroy)
test = partial(test,date,exercise,earnings,study)
b6 = Button(win,text='Test',font='Times 14' , command=test)
b7 = Button(win,text='Refresh',font='Times 14' , command=refresh)
l6 = Label(win,text='Errors will be displayed here !',font='Courier 25',fg='red',bg='yellow')

l1.place(x=500,y=0)
l2.place(x=10,y=50)
e1.place(x=100,y=50)
l3.place(x=10,y=90)
e2.place(x=100,y=90)
l4.place(x=300,y=50)
e3.place(x=390,y=50)
l5.place(x=300,y=90)
combo1.place(x=390,y=90)
list1.pack(side=LEFT)
scroll.pack(side=RIGHT,fill=Y)
b1.place(x=1000,y=50)
b2.place(x=1000,y=100)
b3.place(x=1000,y=150)
b4.place(x=1000,y=200)
b5.place(x=1000,y=250)
b6.place(x=1000,y=300)
b7.place(x=800,y=100)
l6.place(x=20,y=400)

view()
mainloop()