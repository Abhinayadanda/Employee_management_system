from tkinter import *
from sqlite3 import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt
from requests import *



mw=Tk()
mw.title("E.M.S by Abhinaya ")
mw.geometry("800x600+50+50")
f=("Arial",30,"bold")

def f1():
	mw.withdraw()
	aw.deiconify()
def f2():
	aw.withdraw()
	mw.deiconify()
def f3():
	mw.withdraw()
	vw.deiconify()
	vw_emp_data.delete(1.0,END)
	con=None
	try:
		con=connect("ems.db")
		cursor=con.cursor()
		sql="select * from employee"
		cursor.execute(sql)
		data=cursor.fetchall()
		info=""
		for d in data:
			info=info +" id: "+str(d[0])+"  name:  "+str(d[1])+"  sal: "+str(d[2])+"\n"
		vw_emp_data.insert(INSERT,info)
		
	except Exception as e:
		showerror("Issue ",e)
	finally:
		if con is not None:
			con.close()


def f4():
	vw.withdraw()
	mw.deiconify()
def f5():
	mw.withdraw()
	uw.deiconify()

def f6():
	uw.withdraw()
	mw.deiconify()
def f7():
	mw.withdraw()
	dw.deiconify()
def f8():
	dw.withdraw()
	mw.deiconify()

#save btn of add emp

def f9():
	con=None
	try:
		con=connect("ems.db")
		cursor=con.cursor()
		sql="insert into employee values('%d','%s','%f')"
		if not aw_ent_id.get():
    			showerror("issue", "id cannot be empty")
    			return
		try:
			eid=int(aw_ent_id.get())
		except ValueError:
			showerror("issue ","id should be integer only")
			return
		
		if eid<1 :
			showerror("issue ","id should be positive only")
			return

		name=aw_ent_name.get()
		if not aw_ent_name.get():
    			showerror("issue", "name cannot be empty")
    			return
		if not name.isalpha():
			showerror("issue ","name should contain only alphabets")
			return
		if len(name)<2:
			showerror("issue ","name should contain min of 2 alphabets")
			return

		if not aw_ent_salary.get():
    			showerror("issue", "salary cannot be empty")
    			return
		try:
			salary=float(aw_ent_salary.get())
		except ValueError:
			showerror("issue ","salary should be number only")
			return
		if salary<8000:
			showerror("issue ","salary should be minimum 8K")
			return

		cursor.execute(sql%(eid,name,salary))
		showinfo("Success","record created ")
		con.commit()
		
	except Exception:
		showerror("issue ","id already exists!!")
	finally:
		if con is not None:
			con.close()
		aw_ent_id.delete(0, END)
		aw_ent_name.delete(0, END)
		aw_ent_salary.delete(0, END)
		aw_ent_id.focus()

#save btn of Update
def f10():
	con=None
	try:
		con=connect("ems.db")
		cursor=con.cursor()
		sql="update employee set ename='%s',esalary='%f' where eid='%d' "
		if not uw_ent_id.get():
    			showerror("issue", "id cannot be empty")
    			return
		try:
			eid=int(uw_ent_id.get())
		except ValueError:
			showerror("issue ","id should be integer only")
			return
		
		if eid<1 :
			showerror("issue ","id should be positive only")
			return

		ename=uw_ent_name.get()
		if not uw_ent_name.get():
    			showerror("issue", "name cannot be empty")
    			return
		if not ename.isalpha():
			showerror("issue ","name should contain only alphabets")
			return
		if len(ename)<2:
			showerror("issue ","name should contain min of 2 alphabets")
			return

		if not uw_ent_salary.get():
    			showerror("issue", "salary cannot be empty")
    			return
		try:
			esalary=float(uw_ent_salary.get())
			if esalary<8000:
				showerror("issue ","salary should be minimum 8K")
				return
		except ValueError:
			showerror("issue ","salary should be number only")
			return

		cursor.execute(sql % (ename,esalary,eid))
		if cursor.rowcount == 1:
			showinfo("Success","record updated")
			con.commit()
		else:
			showerror("Error","record does not exist")
		
	except Exception as e:
		showerror("Issue ",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
		uw_ent_id.delete(0, END)
		uw_ent_name.delete(0, END)
		uw_ent_salary.delete(0, END)
		uw_ent_id.focus()

#save btn of delete
def f11(): 
	con=None
	try:
		con=connect("ems.db")
		cursor=con.cursor()
		sql="delete from employee where eid='%d' "
		if not dw_ent_id.get():
    			showerror("issue", "id cannot be empty")
    			return
		try:
			eid=int(dw_ent_id.get())
		except ValueError:
			showerror("issue ","id should be integer only")
			return
		
		if eid<1 :
			showerror("issue ","id should be positive only")
			return
		
		cursor.execute(sql % (eid))
		if cursor.rowcount == 1:
			con.commit()
			showinfo("Success","record deleted ")
		else:
			showerror("Error","record does not exist ")
	
	
	except Exception as e:
		print("issue ",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
		dw_ent_id.delete(0, END)
		dw_ent_id.focus()

#data analysis(bar graph)

def f12():
	con=None
	try:
		con=connect("ems.db")
		cursor=con.cursor()
		sql="select ename,esalary from employee order by esalary desc limit 5"
		cursor.execute(sql)
		rows=cursor.fetchall()
		
		names = [row[0] for row in rows]
		salaries = [row[1] for row in rows]
		sorted_names, sorted_salaries = zip(*sorted(zip(names, salaries), key=lambda x: x[1], reverse=True))

		fig = plt.figure(figsize=(8, 6))
		plt.bar(sorted_names, sorted_salaries, color='g', width=0.8, label='Salary')
		plt.xlabel('Employee Name',fontsize=12)
		plt.ylabel('Salary in (\u20B9)',fontsize=12)
		plt.title('Top 5 highest paid employees')
		plt.legend()
		
		plt.show()
	except Exception as e:
		print("issue ",e)
	finally:
		if con is not None:
			con.close()

#Temp loc fn

def f13():
	try:
		a1="https://api.openweathermap.org/data/2.5/weather"
		a2="?q=" + "Mumbai"
		a3="&appid=" + "c6e315d09197cec231495138183954bd"
		a4="&units=" + "metric"
		wa=a1+a2+a3+a4
		res=get(wa)
		data=res.json()
		temp=data["main"]["temp"]
		msg=data["name"]
		ans1.configure(text=msg)
		ans2.configure(text=temp)

	except Exception as e:
		print("issue ",e)

	

#Main window
mw.configure(background='lightblue')
mw_btn_add=Button(mw,text="Add",font=f,width=12,command=f1)
mw_btn_view=Button(mw,text="View",font=f,width=12,command=f3)
mw_btn_update=Button(mw,text="Update",font=f,width=12,command=f5)
mw_btn_delete=Button(mw,text="Delete",font=f,width=12,command=f7)
mw_btn_charts=Button(mw,text="Charts",font=f,width=12,command=f12)

mw_btn_add.pack(pady=5)
mw_btn_view.pack(pady=5)
mw_btn_update.pack(pady=5)
mw_btn_delete.pack(pady=5)
mw_btn_charts.pack(pady=5)

loc_lb=Label(mw,text="Location: ",font=f)
ans1=Label(mw,font=f)
temp_lb=Label(mw,text="Temp: ",font=f)
ans2=Label(mw,font=f)
loc_lb.place(x=90,y=500)
temp_lb.place(x=500,y=500)
ans1.place(x=300,y=500)
ans2.place(x=650,y=500)
f13()

#Add employee window 
aw=Toplevel(mw)
aw.title("Add Emp")
aw.geometry("800x600+50+50")
aw.configure(background='lightgreen')

aw_lb_id=Label(aw,text="enter id: ",font=f)
aw_ent_id=Entry(aw,font=f)
aw_lb_name=Label(aw,text="enter name: ",font=f)
aw_ent_name=Entry(aw,font=f)
aw_lb_salary=Label(aw,text="enter salary: ",font=f)
aw_ent_salary=Entry(aw,font=f)
aw_btn_save=Button(aw,text="Save",font=f,width=10,command=f9)
aw_btn_back=Button(aw,text="Back",font=f,width=10,command=f2)

aw_lb_id.pack(pady=5)
aw_ent_id.pack(pady=5)
aw_lb_name.pack(pady=5)
aw_ent_name.pack(pady=5)
aw_lb_salary.pack(pady=5)
aw_ent_salary.pack(pady=5)
aw_btn_save.pack(pady=5)
aw_btn_back.pack(pady=5)
aw.withdraw()

#View window
vw=Toplevel(mw)
vw.title("View Emp")
vw.geometry("800x600+50+50")
vw.configure(background='#ffb366')
f1=("Arial",28)
vw_emp_data=ScrolledText(vw,width=30,height=8,font=f1)
vw_btn_back=Button(vw,text="Back",font=f,width=12,command=f4)
vw_emp_data.pack(pady=5)
vw_btn_back.pack(pady=5)
vw.withdraw()

#Update window
uw=Toplevel(mw)
uw.title("Update Emp")
uw.geometry("800x600+50+50")
uw.configure(background='#e6ccff')

uw_lb_id=Label(uw,text="enter id: ",font=f)
uw_ent_id=Entry(uw,font=f)
uw_lb_name=Label(uw,text="enter name: ",font=f)
uw_ent_name=Entry(uw,font=f)
uw_lb_salary=Label(uw,text="enter salary: ",font=f)
uw_ent_salary=Entry(uw,font=f)
uw_btn_save=Button(uw,text="Save",font=f,width=10,command=f10)
uw_btn_back=Button(uw,text="Back",font=f,width=10,command=f6)

uw_lb_id.pack(pady=5)
uw_ent_id.pack(pady=5)
uw_lb_name.pack(pady=5)
uw_ent_name.pack(pady=5)
uw_lb_salary.pack(pady=5)
uw_ent_salary.pack(pady=5)
uw_btn_save.pack(pady=5)
uw_btn_back.pack(pady=5)
uw.withdraw()

#Delete Emp
dw=Toplevel(mw)
dw.title("Delete Emp")
dw.geometry("800x600+50+50")
dw.configure(background='#ffff99')

dw_lb_id=Label(dw,text="enter id: ",font=f)
dw_ent_id=Entry(dw,font=f)
dw_btn_save=Button(dw,text="Save",font=f,width=10,command=f11)
dw_btn_back=Button(dw,text="Back",font=f,width=10,command=f8)

dw_lb_id.pack(pady=5)
dw_ent_id.pack(pady=5)
dw_btn_save.pack(pady=5)
dw_btn_back.pack(pady=5)
dw.withdraw()


mw.mainloop()