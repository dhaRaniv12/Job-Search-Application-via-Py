# Student Portfolio - 668, 669
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox as Messagebox
import mysql.connector as mysql
import re
from tkinter import filedialog
import os
import webbrowser
from pathlib import Path


filepath = ''
init_filePath = ''
ontop = False
ontop1 = False


def onTopApply(event):
    global ontop
    ontop = False


def onTopDetails(event):
    global ontop1
    ontop1 = False


def clickApply():
    global ontop
    if not ontop:
        def choose_file():
            global filepath
            filepath = StringVar()
            if(filepath == ""):
                filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                      title="Upload Your Resume",

                                                      filetypes=(("PDF", "*.pdf*"),))
            else:
                filepath = filedialog.askopenfilename(initialdir=filepath,
                                                      title="Upload Your Resume", filetypes=(("PDF",
                                                                                              "*.pdf*"), ))
                label_file_explorer.delete(0, "end")
                if not filepath:
                    label_file_explorer.insert(
                        0, "                           "+'No file choosen.')
                else:
                    fileName = Path(filepath).name
                    label_file_explorer.insert(
                        0, "                           "+fileName)

        def ApplyButton():
            global validation
            validation = ''

            is_any_error = False
            first_name = f_name.get()
            first_name = first_name.strip()
            last_name = l_name.get()
            E_mail = email.get()
            phone = Phone_number.get()

            # validation patterns
            first_name_last_name_validation = re.compile("^[A-Za-z ]+$")
            pattern_mail_validation = re.compile(
                r"^([a-z0-9\.-]+)@([a-z0-9-]+).([a-z]{2,8})(.[a-z]{2,8})?$")
            phone_number_pattern = re.compile(r"^[0-9]{10}$")

            # conditions for validations

            # first name and second name validation
            if not first_name:
                is_any_error = True
                validation += "|First Name| "
            elif re.match(first_name_last_name_validation, first_name) is None:
                is_any_error = True
                Messagebox.showerror("Warning!", "Invalid First Name.")
            if not last_name:
                is_any_error = True
                validation += "|Last Name| "
            elif re.match(first_name_last_name_validation, last_name) is None:
                is_any_error = True
                Messagebox.showerror("Warning!", "Invalid Last Name.")

            # E_mail validation

            if not E_mail:
                is_any_error = True
                validation += "|Email| "
            elif re.match(pattern_mail_validation, E_mail) is None:
                is_any_error = True
                Messagebox.showerror("Warning!", "Invalid Email.")

            # Resume validation

            filename = filepath
            if not filename:
                validation += "|Upload Resume| "
            else:
                def convertToBinaryData(filename):
                    with open(filename, 'rb') as file:
                        binaryData = file.read()
                    return binaryData

                def insertBLOB(biodataFile):
                    global file
                    file = convertToBinaryData(biodataFile)
                    return file

                insertBLOB(filename)

            # phone validation
            if not phone:
                is_any_error = True
                validation += "|Phone Number| "

            elif re.match(phone_number_pattern, phone) is None:
                is_any_error = True
                Messagebox.showerror(
                    "Warning!", "Invalid Phone Number.")

            if validation == '':
                if(is_any_error != False):
                    return
                else:
                    # sending data to database
                    con = mysql.connect(host="remotemysql.com", user="XgfA7Oer3H",
                                        password="PWc4Z5OBXP", database="XgfA7Oer3H")
                    cursor = con.cursor()
                    query = "INSERT INTO student_details (FirstName,LastName,Email,Resume,PhoneNumber) VALUES (%s,%s,%s,%s,%s)"

                    values = (first_name, last_name, E_mail, file, phone)
                    course = cursor.execute(query, values)
                    con.commit()

                    Messagebox.showinfo(
                        "Student Portfolio", "Successfully Uploaded.")
                    con.close()

            else:
                Messagebox.showerror("Enter the following", validation)

        root = tkinter.Toplevel()
        root.geometry("412x380")
        root.configure(background='white')
        style = ttk.Style()
        root.title("Apply Student Portfolio")
        root.resizable(False, False)
        root.iconbitmap("student.ico")
        # root.iconbitmap(".icon\\student.ico")

        label = ttk.Label(root, background="black")
        # width=412, height=1
        label.pack(ipadx=412, ipady=1)

        label_1 = ttk.Label(root, text="Job Application", background='white', foreground="black", font=(
            'Verdana', 18, 'bold'))
        label_1 = label_1.place(x=110, y=21)

        label_2 = ttk.Label(root, text="- dhaRani V (668) & Mirza Abbas (669) - ",
                            background='white', foreground="black", font=('Roboto', 10, 'bold'))
        label_2.place(x=90, y=55)
        label_3 = Label(root, text="Name", background='white',
                        foreground="black")
        label_3.place(x=5, y=80)

        label_4 = Label(root, text="First Name", font=(
            'verdana', 7), background="white")
        label_4.place(x=125, y=100)

        label_5 = Label(root, text="Last Name", font=(
            'verdana', 7), background="white")
        label_5.place(x=262, y=100)

        label_6 = Label(root, text="Email", background='white',
                        foreground="black")
        label_6.place(x=5, y=120)

        label_8 = Label(root, text="Resume", background='white',
                        foreground="black").place(x=5, y=180)

        label_16 = Label(root, text="Phone Number", background='white',
                         foreground="black").place(x=5, y=230)

        # Entry Box

        # Name
        f_name = Entry(root, background="white")
        f_name.place(x=128, y=80)
        l_name = Entry(root, background="white")
        l_name.place(x=265, y=80)

        # Email
        email = Entry(root, width="40", background="white")
        email.place(x=128, y=123)

        # File(.PDF)
        label_file_explorer = Entry(
            root, background="white", width=43, state="normal")
        label_file_explorer.insert(INSERT, "                           ")
        label_file_explorer.insert(END, " No file choosen yet.")
        label_file_explorer.bind("<Key>", lambda e: "break")
        label_file_explorer.place(x=128, y=177, height=32)
        Btn2 = Button(root, text="choose file", command=choose_file)
        Btn2.pack(ipadx=10, ipady=1)
        Btn2.place(x=130, y=179)

        Phone_number = Entry(root, width="36", background="white")
        Phone_number.place(x=128, y=230)

        style.configure('C.TLabel', padding=[
                        5, 5, 15, 5], font=('Roboto', 10, 'bold'))
        style.map('C.TLabel',
                  foreground=[('!active', 'white'), ('active', 'white')],
                  background=[('!disabled', 'black')],
                  relief=[('active', 'sunken'),
                          ('active', 'raised')]
                  )
        ApplyButton = Button(root, text="  Apply",
                             style='C.TLabel', command=ApplyButton)
        ApplyButton.place(x=180, y=300)
        root.bind('<Destroy>', onTopApply)

    ontop = True


def clickDetails():
    global ontop1
    if not ontop1:
        def write_file(data, filename):

            # Convert binary data to proper format and write it on local drive

            with open(filename, 'wb') as file:
                file.write(data)

        def downloadButton():
            defaultValue = "Choose Student's ID"
            id = entery_of_search.get()

            if (id == defaultValue):
                Messagebox.showerror(
                    "Select the ID", "Please choose an user ID to download their resume.")
            else:
                global init_filePath
                init_filePath = StringVar()

                init_filePath = filedialog.askdirectory()

                if not init_filePath:
                    print("no file path")
                    return Messagebox.showerror("No File Path", "Please select a valid path to download resume.")
                else:
                    # print("entered file path")
                    try:
                        id = entery_of_search.get()
                        con = mysql.connect(host="remotemysql.com", user="XgfA7Oer3H",
                                            password="PWc4Z5OBXP", database="XgfA7Oer3H")
                        cursor = con.cursor()
                        sql = "SELECT * FROM student_details WHERE id = %s"
                        cursor.execute(sql, (id,))
                        record = cursor.fetchall()

                        for row in record:
                            name = row[1]
                            userfilename = (name+".pdf")
                            finalPath = os.path.join(
                                init_filePath, userfilename)
                            file = row[4]
                            write_file(file, finalPath)
                            dlPath = ('file:///'+finalPath)
                            # Messagebox.showinfo('Job Application', str(
                            #     'Successfully downloaded the Resume of '+name))
                            Messagebox.showinfo('Job Application', str(
                                'Resume of '+name+' downloaded at '+init_filePath))
                        if not init_filePath:
                            return exit()
                        else:
                            entery_of_search.set(value=defaultValue)

                            webbrowser.open(dlPath)

                    except mysql.Error as error:
                        Messagebox.showerror("sql error", error)

        def update(rows):
            for i in rows:
                trv.insert('', 'end', values=i)

        con = mysql.connect(host="remotemysql.com", user="XgfA7Oer3H",
                            password="PWc4Z5OBXP", database="XgfA7Oer3H")
        cursor = con.cursor()
        cursor.execute(
            "select Id,FirstName,LastName,Email,PhoneNumber from student_details")
        rows = cursor.fetchall()

        root1 = tkinter.Toplevel()
        root1.geometry("600x680")
        root1.iconbitmap("student.ico")
        # root1.iconbitmap(".icon\\student.ico")

        root1.configure(bg='black')
        style = ttk.Style(root1)
        style = ttk.Style(root1)
        style.theme_use()
        root1.title("Student Portfolio Details")
        root1.resizable(False, False)
        wrapper1 = LabelFrame(root1, text="  Students Details")
        wrapper1.pack(fill="both", expand="yes", padx="10", pady="5")
        trv = Treeview(wrapper1, columns=(1, 2, 3, 4, 5),
                       show="headings", height="14")
        trv.pack()
        wrapper2 = LabelFrame(root1, text="  Download Resume")
        wrapper2.pack(fill="both", expand="yes", padx="10", pady="5")

        trv.pack(side=RIGHT)
        trv.place(x=0, y=0)
        trv.heading(1, text="ID")
        trv.heading(2, text="First Name")
        trv.heading(3, text="Last Name")
        trv.heading(4, text="Email")
        trv.heading(5, text="Phone")

        trv.column("1", width=20, minwidth=30)
        trv.column("2", width=80, minwidth=100)
        trv.column("3", width=80, minwidth=100)
        trv.column("4", width=120, minwidth=150)
        trv.column("5", width=300, minwidth=200)

        # Vertical Scorllbar
        yscrollbar = ttk.Scrollbar(
            wrapper1, orient="vertical", command=trv.yview)
        yscrollbar.pack(side=RIGHT, fill="y")
        trv.configure(yscrollcommand=yscrollbar.set)

        # Horizontal Scrollbar
        xscrollbar = ttk.Scrollbar(
            wrapper1, orient="horizontal", command=trv.xview)
        xscrollbar.pack(side=BOTTOM, fill="x")
        trv.configure(xscrollcommand=xscrollbar.set)
        update(rows)

        def getId():
            con = mysql.connect(host="remotemysql.com", user="XgfA7Oer3H",
                                password="PWc4Z5OBXP", database="XgfA7Oer3H")
            cursor = con.cursor()
            cursor.execute("select id from student_details")
            rows = cursor.fetchall()
            listOfID = []
            for row in rows:
                listOfID.append(row[0])
            return listOfID

        lel = Label(wrapper2, text="Download Student's Resume as PDF")
        lel.pack(side=tkinter.LEFT, padx=10)

        entery_of_search = StringVar(wrapper2)
        entery_of_search.set("Choose Student's ID")
        course = ttk.Combobox(
            wrapper2, width=26, textvariable=entery_of_search, values=getId(), state="readonly")
        course.pack(side=tkinter.LEFT, padx=6)
        btn = Button(wrapper2, text="Download", command=downloadButton)
        btn.pack(side=tkinter.LEFT, padx=6)
        root1.bind('<Destroy>', onTopDetails)
    ontop1 = True


top = tkinter.Tk()
top.geometry("300x300")
top.configure(bg='white')
top.title("Student Portfolio")
top.resizable(False, False)


button = tkinter.Button(top, text="Apply", font=(
    'Roboto', 10, 'bold'), bg="black", fg="white", width="8", height="1", command=clickApply)
button.place(x=116, y=99)
button1 = tkinter.Button(top, text="Details", font=(
    'Roboto', 10, 'bold'), bg="black", fg="white", width="8", height="1", command=clickDetails)
button1.place(x=116, y=159)

top.iconbitmap("student.ico")
# top.iconbitmap(".icon\\student.ico")


top.mainloop()
