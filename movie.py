import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class movies ():
    def __init__(self, root):
        self.root = root
        self.root.title("Book My Seat")


        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Book My Seat", bd=4, relief="raised", bg="light yellow", font= ("Arial", 50, "bold")) 
        title.pack(side="top", fill="x")         
        
        
        # global variables
        self.row = 4
        self.seat = 5


        self.frame = tk.Frame(self.root, bd=5, relief="ridge", bg="Light yellow")
        self.frame.place(width=self.width-300, height=self.height-180, x=150, y=100)

        optLbl = tk.Label(self.frame, text="Select_Show:", bg="Light yellow", font=("Arial",15,"bold"))
        optLbl.grid(row=0, column=0, padx=20, pady=30,)
        self.opt = ttk.Combobox(self.frame,font=("Arial",15,"bold"),values=("First","Second","Third"),width=17 )
        self.opt.set("Select_One")
        self.opt.grid(row=0, column=1, padx=10, pady=30)

        nameLbl = tk.Label(self.frame, text="Your_Name:", bg="Light yellow", font=("Arial",15,"bold"))
        nameLbl.grid(row=0, column=2, padx=20, pady=30)
        self.name = tk.Entry(self.frame, bd=3, width=18,font=("Arial",15,"bold") )
        self.name.grid(row=0, column=3, padx=10, pady=30)

        okBtn = tk.Button(self.frame,command=self.reservFun, text="Reserve", font=("Arial",15,"bold"),width=8)
        okBtn.grid(row=0, column=4, padx=30, pady=30)
        
        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.frame, bd=5, relief="ridge", bg="Light yellow")
        tabFrame.place(width=self.width-400, height=self.height-300, x=50,y=90)

        x_scrol = tk.Scrollbar(tabFrame,orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("show_no","show_time","movie_name","price","available_seats"))

        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        
        self.table.heading("show_no", text="Show_No")
        self.table.heading("show_time", text="Time")
        self.table.heading("movie_name", text="Movie_Name")
        self.table.heading("price", text="Price")
        self.table.heading("available_seats", text="Available_seats")
        self.table["show"]="headings"

        self.table.column("show_no", width=200)
        self.table.column("show_time", width=200)
        self.table.column("movie_name", width=200)
        self.table.column("price", width=80)
        self.table.column("available_seats", width=80)
        
        self.table.pack(fill="both", expand=1)

        self.showFun()


    def showFun(self):
        try:
            self.dbFun()
            self.cur.execute("select * from movie")
            data = self.cur.fetchall()

            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('',tk.END, values=i)

            self.con.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

    def reservFun(self):
        opt = self.opt.get()
        name = self.name.get()


        if opt and name:
            try:
                self.dbFun()
                self.cur.execute("select show_time, movie_name, price, available_seats from movie where show_no=%s", opt)
                row = self.cur.fetchone()
                if row[3] >0:
                    if self.row >0:
                        if self.seat>0:
                            self.seat = self.seat-1
                            
                            upd = row[3]-1
                            self.cur.execute("update movie set available_seats=%s where show_no=%s",(upd,opt))
                            self.con.commit()
                            tk.messagebox.showinfo("Success", f"Seat No.{5-self.seat} in row.{5-self.row} is Reserved For Mr/Mrs.{name}\nNow Pay {row[2]}$")

                            self.cur.execute("select * from movie ")
                            data = self.cur.fetchall()

                            
                            self.table.delete(*self.table.get_children())
                            for i in data:
                                self.table.insert('',tk.END, values=i)

                            self.con.close()
                        else:
                            self.row = self.row-1
                            self.seat = 5

                else:
                    tk.messagebox.showerror("Error","All Seats Reserved for this Show")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
        else:
            tk.messagebox.showerror("Error","Please Fill All Input Fields!")

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="Rasengan@10", database="movies")
        self.cur = self.con.cursor()




root = tk.Tk()
obj = movies(root)
root.mainloop()