from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pyodbc
import customtkinter
import  time

Profile = {1: ""}

def clock():
    date =time.strftime("%d/%m/%Y")
    currentTime= time.strftime("%H:%M:%S")
    print(date,currentTime)
    datetimeLabel.config(text=f'    Date: {date}\nTime: {currentTime}')
    datetimeLabel.after(1000,clock) #saniye artsın değişsin

def add_customer():
    name = entryName.get()
    phone = entryPhone.get()
    more= entryMore.get()
    print(name,"---",phone)
    try:
        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=K\SQLEXPRESS;' +
                                    'Database=ADDRESBOOK;' +
                                    'Trusted_Connection=True')

        cursor = connection.cursor()

        # Yeni kaydı ekle
        cursor.execute("INSERT INTO customer (name, phone, moreinfo) VALUES (?, ?, ?)",
                       (name, phone, more))

        # Değişiklikleri kaydet
        connection.commit()

        # Bağlantıyı kapat
        connection.close()

        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=K\SQLEXPRESS;' +
                                    'Database=ADDRESBOOK;' +
                                    'Trusted_Connection=True')

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customer order by id desc")

        row = cursor.fetchone() #ilkini al

        # Eğer bir satır varsa, tuple oluştur ve ekleyin
        if row:
            my_tuple2 = tuple(row)
            tree.insert('', END, values=my_tuple2)
        connection.close()
        # Sorguyu çalıştır

        #Resim kaydetmek icin

        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=K\SQLEXPRESS;' +
                                    'Database=ADDRESBOOK;' +
                                    'Trusted_Connection=True')

        cursor = connection.cursor()
        select = cursor.execute("SELECT * FROM  customer order by id desc")

        row = cursor.fetchone()
        #print(row[0])
        id = row[0]

        filename = entryPhoto.get()
        im = Image.open(filename)
        res_im = im.resize((150,150))
        rgb_im = res_im.convert('RGB')
        rgb_im.save(("images/profile_"+ str(id) + "." + "jpg"))
        connection.close()

    except pyodbc.Error as ex:
        print("Failed! ", ex)

def delete_customer():
    #print(tree.item(tree.selection()))
    #print(tree.item(tree.selection())['values'])

    idSelected = tree.item(tree.selection())['values'][0]

    connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                'Server=K\SQLEXPRESS;' +
                                'Database=ADDRESBOOK;' +
                                'Trusted_Connection=True')

    cursor = connection.cursor()
    delete = cursor.execute("DELETE  FROM customer WHERE  id = {}".format(idSelected))
    connection.commit()
    tree.delete(tree.selection())

def sortByName():
    #clear the treeview
    for x in tree.get_children():
        tree.delete(x)

    connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                'Server=K\SQLEXPRESS;' +
                                'Database=ADDRESBOOK;' +
                                'Trusted_Connection=True')

    cursor = connection.cursor()
    select = cursor.execute("SELECT * FROM customer ORDER BY name ASC")
    rows = cursor.fetchall()

    for row in rows:
        my_tuple3 = tuple(row)
        tree.insert('',END, values=my_tuple3)

    connection.commit()
    connection.close()

def SearchByName(event):
    for x in tree.get_children():
        tree.delete(x)
    name = entrySearchByName.get()

    connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                'Server=K\SQLEXPRESS;' +
                                'Database=ADDRESBOOK;' +
                                'Trusted_Connection=True')

    cursor = connection.cursor()
    select = cursor.execute("SELECT * FROM customer WHERE name = ?", (name,))
    rows = cursor.fetchall()

    for row in rows:
        my_tuple4= tuple(row)
        tree.insert('', END, values=my_tuple4)

    connection.commit()

def SearchByPhone(event):
    for x in tree.get_children():
        tree.delete(x)
    phone = entrySearchByPhone.get()

    connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                'Server=K\SQLEXPRESS;' +
                                'Database=ADDRESBOOK;' +
                                'Trusted_Connection=True')

    cursor = connection.cursor()
    select = cursor.execute("SELECT * FROM customer WHERE phone = ?", (phone,))
    rows = cursor.fetchall()
    
    for row in rows:
        my_tuple4= tuple(row)
        tree.insert('', END, values=my_tuple4)

    connection.commit()


def BrowsePhoto():
    entryPhoto.delete(0,END)
    filename = filedialog.askopenfilename(initialdir="/",title="Select File")
    entryPhoto.insert(END,filename)


def treeActionSelect(event):
    #load image
    label_image.destroy()

    idSelect = tree.item(tree.selection())['values'][0]
    imgProfile = "images/profile_"+ str(idSelect)+ "." +"jpg"
    load = Image.open(imgProfile)
    load.thumbnail((300,150))
    photo = ImageTk.PhotoImage(load)
    Profile[1] = photo
    lblImage = Label(root, image=photo, width=150, height=150)
    lblImage.place(relx=0.22, rely=0.65)

    nameSelect = tree.item(tree.selection())['values'][1]
    phoneSelect = tree.item(tree.selection())['values'][2]
    moreInfoSelect = tree.item(tree.selection())['values'][3]


    lid= Text(root,font=("Arial",10), state='disabled')
    lid.place(relx=0.35, rely=0.65,width=200, height =20)

    lname= Text(root, font=("Arial",10), state='disabled')
    lname.place(relx=0.35, rely=0.69,width=200, height =20)

    lphone= Text(root,font=("Arial",10), state='disabled')
    lphone.place(relx=0.35, rely=0.73,width=200, height =20)

    Tmore = Text(root,font=("Arial",10), state='disabled')
    Tmore.place(relx=0.35, rely=0.77, width=280, height =100)

    Tmore.config(state="normal")
    lid.config(state="normal")
    lname.config(state="normal")
    lphone.config(state="normal")

    Tmore.insert(END,"More Info: "+ moreInfoSelect)
    lid.insert(END,"ID : "+str(idSelect))
    lname.insert(END,"Name : "+nameSelect)
    lphone.insert(END,"Phone : "+str(phoneSelect))

    Tmore.config(state="disabled")
    lid.config(state="disabled")
    lname.config(state="disabled")
    lphone.config(state="disabled")

root = Tk()
root.title("MÜŞTERİ TELEFON REHBERİ")
root.geometry("1280x720+70+30")
root.resizable(0,0)

mainFrame = Frame(root,background="#DFD9D8", highlightthickness=2, highlightbackground="black", width=1240, height=700)
mainFrame.place(x=20, y=10)

datetimeLabel= Label(mainFrame,font=('arial',15,'bold'), fg="green")
datetimeLabel.place(x=50,y=10)

clock()

#Baslik
lblTitle = Label(mainFrame, text="MÜŞTERİ TELEFON REHBERİ",font=("Arial",21,"italic bold"),fg="#5FB060", borderwidth=1)
lblTitle.place(relx=0.25, rely=0.04,width=500, height=45)

#Search
lbSearchByName= Label(mainFrame, text="Search by Name:",font=("Arial",10,"italic bold"))
lbSearchByName.place(relx=0.2, rely=0.129,width=110)

entrySearchByName= Entry(mainFrame)
entrySearchByName.bind("<Return>", SearchByName)
entrySearchByName.place(relx=0.3, rely=0.129,width=150)

lbSearchByPhone= Label(mainFrame, text="Search by Phone:",font=("Arial",10,"italic bold"))
lbSearchByPhone.place(relx=0.45, rely=0.129,width=110)

entrySearchByPhone= Entry(mainFrame)
entrySearchByPhone.bind("<Return>", SearchByPhone)
entrySearchByPhone.place(relx=0.55, rely=0.129,width=150)


#label Name & Surname
lblName = Label(mainFrame, text="Name & Surname :",font=("Arial",10,"italic bold"))
lblName.place(relx=0.2, rely=0.18, width=125)
entryName= Entry(mainFrame)
entryName.place(relx=0.32, rely=0.18,width=400)

lblPhone = Label(mainFrame, text="Phone Number :",font=("Arial",10,"italic bold"))
lblPhone.place(relx=0.2, rely=0.22 ,width=125)
entryPhone= Entry(mainFrame)
entryPhone.place(relx=0.32, rely=0.22,width=400)

lblPhoto = Label(mainFrame, text="Photo :",font=("Arial",10,"italic bold"))
lblPhoto.place(relx=0.2, rely=0.26, width=125)
bPhoto= customtkinter.CTkButton(mainFrame,text="Browse", command=BrowsePhoto,width=25, height=10, fg_color="#5FB060")
bPhoto.place(relx=0.59, rely=0.26)
entryPhoto= Entry(mainFrame)
entryPhoto.place(relx=0.32, rely=0.26,width=320)

#More Info
lblMore= Label(mainFrame, text="More Info :",font=("Arial",10,"italic bold"))
lblMore.place(relx=0.2, rely=0.3,width=125)
entryMore= Entry(mainFrame)
entryMore.place(relx=0.32, rely=0.3, width=400)

#Command Button
bAdd= customtkinter.CTkButton(mainFrame, text="Add Customer", command=add_customer, height=35, fg_color="#5FB060")
bAdd.place(relx=0.2, rely=0.34)

bDelete= customtkinter.CTkButton(mainFrame, text="Delete Selected", command=delete_customer, height=35, fg_color="#5FB060")
bDelete.place(relx=0.2, rely=0.4)

bEdit= customtkinter.CTkButton(mainFrame, text="Edit Selected", height=35, fg_color="#5FB060")
bEdit.place(relx=0.2, rely=0.46 )

bSort= customtkinter.CTkButton(mainFrame, text="Sort By Name", command=sortByName, height=35, fg_color="#5FB060")
bSort.place(relx=0.2, rely=0.52)

bExit= customtkinter.CTkButton(mainFrame, text="Exit App", command=quit, height=35, fg_color="#5FB060")
bExit.place(relx=0.2, rely=0.58 )

load = Image.open("download.png")
load.thumbnail((350,150))
photo=ImageTk.PhotoImage(load)
label_image=Label(mainFrame,image=photo)
label_image.place(relx=0.2, rely=0.65)




#add TreeView

tree = ttk.Treeview(mainFrame,columns=(1,2,3), height=5, show="headings")
tree.place(relx=0.33, rely=0.34, width=350, height=200)
tree.bind("<<TreeviewSelect>>",treeActionSelect)

#Add Headings
tree.heading(1,text="ID")
tree.heading(2, text="Name")
tree.heading(3,text="Phone")

#define column width
tree.column(1,width=50)
tree.column(2,width=100)


#Display data in treeview object
try:
    connection= pyodbc.connect('DRIVER={SQL SERVER};'+
                                    'Server=K\SQLEXPRESS;'+
                                    'Database=ADDRESBOOK;'+
                                    'Trusted_Connection=True')
    cursor = connection.cursor()
    cursor.execute("select * from CUSTOMER")

    for data in cursor:
        my_tuple = ()
        for i in range(0,len(data)):
            deger = data[i]
            my_tuple = my_tuple + (deger,)

        tree.insert("", END, value=my_tuple)

except pyodbc.Error as ex:
    print("Failed! ",ex)


root.mainloop()
