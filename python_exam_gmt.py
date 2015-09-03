# -*- coding: utf-8 -*-
"""
    Python Exam
    by GMT
    for Geek Academy

Stworzyć aplikację, która umożliwi uczestnikom GeekAcademy zdanie testu końcowego.
Test składa się z pytań jednokrotnego wyboru: A, B, C, D.
1.  Pytania testowe znajdują się w pliku tekstowym (7 pytań, każde ma 4 odpowiedzi ABCD, jedną poprawną)
    - stworzyć plik z pytaniami
    - wczytać i zdekodować
2.  Tworzymy strukturę do przechowywania danych z pliku tekstowego.
3.  Tworzymy GUI, wyświetlające pytania, umożliwiające udzielenie odpowiedzi na pytania.
3.5 Na GUI musi być widoczne logo firmy.
4.  Aplikacja tworzy raport na końcu - informuje użytkownika o ilości poprawnych odpowiedzi.
5.  Zapisuje raport na dysku z określaną nazwą użytkownika i datą.   dla CHĘTNYCH
6.  Wysyła e-mail z raportem do fikcyjnego adresu.   dla AMBITNYCH
7.  Sieciowo połączyć się z odbiorcą (druga aplikacja), który zbiera wyniki  dla MASTERÓW

"""

import tkinter as tk
import sys
import datetime
import smtplib
import socket
from tkinter import ttk
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

ANSWERS_PER_QUEST = 4

canvas_width = 100
canvas_height = 1300
questions = []
answers = []
rightAnswers = [3, 4, 2, 3, 3, 4, 4]
userAnswers = [0, 0, 0, 0, 0, 0, 0]
totalQuestNo = len(rightAnswers)
userRightAns = 0
studentName = ''
filepath = 'C:\\Users\\Public\\questions.txt'
resultFile = ''
resultFileName = ''
actualDate = str(datetime.datetime.now().date())

VarSelect = {
    0 : "var1",
    1 : "var2",
    2 : "var3",
    3 : "var4",
    4 : "var5",
    5 : "var6",
    6 : "var7"
}


def read_file():
    try:
        file = open(filepath, 'r')
    except:
        print("There is no access to the guestions file!")

    for index, line in enumerate(file):
        if index % 5:
            answers.append(line)
        else:
            questions.append(line)


def sel():
    for i in range(totalQuestNo):
        if VarSelect[i].get() != '':
            if i == int(VarSelect[i].get()[0]) - 1:
                userAnswers[int(VarSelect[i].get()[0]) - 1] = int(VarSelect[i].get()[1])


def submit():
    global userRightAns
    global studentName
    global userRightAns

    userRightAns = 0
    studentName = name.get()

    for i in range(totalQuestNo):
        if userAnswers[i] == rightAnswers[i]:
            userRightAns += 1

    score = round(userRightAns / totalQuestNo, 2)
    message = studentName + ' your score is ' + str(score) + '.\nCorrect answers: '
    message += str(userRightAns) + ', total questions: ' + str(totalQuestNo) + '.'
    message += str('\nYour score was e-mailed to professor :)')
    message += str('\nExam raport was written on disc.')
    title = "Exam result"
    if studentName == '':
        showMessage('Info', 'Enter your name first and submit again!')
    else:
        showMessage(title, message)
        writeOnDisc(score)
        sendMail()
        sendRaport()


def showMessage(title, msg):
    raport = tk.Tk()
    raport.title(title)
    raport.minsize(width = 200, height = 100)
    raport.configure(background = 'white')
    msg = tk.Label(raport, text = msg)
    msg.pack()


def writeOnDisc(score):
    global resultFile
    global resultFileNname
    resultFileName = studentName + "_" + str(actualDate)
    resultFile = 'C:\\Users\\Public\\' + resultFileName + '.txt'

    raport = "Student: " + studentName
    raport += " \nIlosc poprawnych odpowiedzi: " + str(userRightAns)
    raport += " \nWynik procentowy: " + str(score)

    try:
        file = open(resultFile, 'w')
        file.writelines(raport)
        file.close()
    except:
        showMessage('Info', 'File write failed.')


def sendMail():
    global resultFile

    sender = 'adres@wp.pl'
    password = 'jakies_haslo'
    recipient = 'adres@jakas_domena.pl'

    resultFileName = studentName + "_" + str(actualDate)
    outer = MIMEMultipart()
    outer['Subject'] = "Raport z egzaminu: " + resultFileName
    outer['To'] = recipient
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    try:
        with open(resultFile, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
        msg.add_header('Content-Disposition', 'attachment', filename = resultFileName + ".txt")
        outer.attach(msg)
    except:
        showMessage('Info', 'Could not open the report file.')

    composed = outer.as_string()

    try:
        with smtplib.SMTP('smtp.wp.pl', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, password)
            s.sendmail(sender, recipient, composed)
            s.close()
    except:
        showMessage('Info', 'Could not send an e-mail!')


def sendRaport():
    global resultFile
    host = '81.190.92.80'
    port = 51235
    try:
        s = socket.socket()
        s.connect((host, port))
        f = open(resultFile, 'rb')
        data = f.read(1024)
        while data:
            print("Sending...")
            s.sendall(data)
            data = f.read(1024)
        f.close()
        print("Done sending")
        s.close()
    except socket.error as msg:
        showMessage('Info', 'Could not send the report!')
        print('Exception: ', msg)
        s.close()


# Top-level frame
root = tk.Tk()
root.title( "Sii Geek Academy - Python exam           by GMT software" )
root.minsize(width = 800, height = 500)
root.configure(background = 'white')
frame = ttk.Frame(root, relief="sunken")


# Canvas creation with double scrollbar
hscrollbar = ttk.Scrollbar(frame, orient = tk.HORIZONTAL)
vscrollbar = ttk.Scrollbar(frame, orient = tk.VERTICAL)
sizegrip = ttk.Sizegrip(frame)
canvas = tk.Canvas(frame, bd=0, highlightthickness=0, yscrollcommand = vscrollbar.set, xscrollcommand = hscrollbar.set
                        , bg = 'white')
vscrollbar.config(command = canvas.yview)
hscrollbar.config(command = canvas.xview)


# Add controls here
subframe = ttk.Frame(canvas)

logo = tk.Canvas(subframe, width = canvas_width, height = canvas_height, bg = 'white', bd = 0, highlightcolor = 'white')
logo.grid(row = 0, column = 0, sticky = 'news')
img = tk.PhotoImage(file = "logoGMT.gif")
logo.create_image(50, 250, anchor = 's', image = img)

app = tk.Canvas(subframe, background='white', bd = 0, highlightcolor = 'white')
app.grid(row = 0, column = 1, sticky = 'news')
welcome = tk.Text(app, height = 5, wrap='none', bg = 'white', bd = 0
                     , selectborderwidth = 0, insertborderwidth =0, highlightthickness = 0, highlightcolor = 'white'
                     , highlightbackground = 'white', width = 130)
welcome.grid(row = 0, column = 0, sticky = 'news')
welcome.insert('end', 'Welcome on the final Sii Geek Academy Python exam!\n')
welcome.insert('end', 'Please click on the right answer for the following questions.\n\n')
welcome.insert('end', 'Enter your name:                    Today is:   ' + str(actualDate) + '\n')
welcome.configure(state = 'disabled')
name = tk.Entry(app, validate = 'key', bg = 'white')
name.grid(row = 1, column = 0, columnspan = 2, sticky = 'w')

read_file()

for i in range(totalQuestNo):
    egzamin = tk.Text(app, fg = 'blue', bg = 'white', wrap='none'
                         , bd = 0, selectborderwidth = 0, insertborderwidth =0, highlightthickness = 0
                         , height = 6, highlightcolor = 'white', highlightbackground = 'white', width = 130)
    egzamin.grid(row = i * totalQuestNo + 2, column = 0, sticky = 'w')
    egzamin.insert('end', '\n' + questions[i])
    egzamin.insert('end', answers[i * ANSWERS_PER_QUEST])
    egzamin.insert('end', answers[i * ANSWERS_PER_QUEST + 1])
    egzamin.insert('end', answers[i * ANSWERS_PER_QUEST + 2])
    egzamin.insert('end', answers[i * ANSWERS_PER_QUEST + 3])
    egzamin.configure(state = 'disabled')
    radioButton = tk.Canvas(app, background='white', bd = 0, highlightcolor = 'white', cursor = 'arrow')
    radioButton.grid(row = i * totalQuestNo + 3, column = 0, sticky = 'w')
    VarSelect[i] = tk.StringVar()
    R = tk.Radiobutton(radioButton, text = 'A', variable = VarSelect[i], value = str(i+1) + '1'
                               , command = sel, bg = 'white', fg = 'blue')
    R.grid(row = 0, column = 0, sticky = 'w')
    R = tk.Radiobutton(radioButton, text = 'B', variable = VarSelect[i], value = str(i+1) + '2'
                               , command = sel, bg = 'white', fg = 'blue')
    R.grid(row = 0, column = 1, sticky = 'w')
    R = tk.Radiobutton(radioButton, text = 'C', variable = VarSelect[i], value = str(i+1) + '3'
                               , command = sel, bg = 'white', fg = 'blue')
    R.grid(row = 0, column = 2, sticky = 'w')
    R = tk.Radiobutton(radioButton, text = 'D', variable = VarSelect[i], value = str(i+1) + '4'
                               , command = sel, bg = 'white', fg = 'blue')
    R.grid(row = 0, column = 3, sticky = 'w')

buttonSubmit = tk.Button(app, text = "Submit", command = submit)
buttonSubmit.grid(row = 55, column = 0, sticky = 'w')


#Packing everything
subframe.pack(padx   = 15, pady   = 15, fill = tk.BOTH, expand = tk.TRUE)
hscrollbar.pack( fill=tk.X, side=tk.BOTTOM, expand=tk.FALSE)
vscrollbar.pack( fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
sizegrip.pack(in_ = hscrollbar, side = tk.BOTTOM, anchor = "se")
canvas.pack(side = tk.LEFT, padx  = 5, pady   = 5, fill = tk.BOTH, expand= tk.TRUE)
frame.pack( padx   = 5, pady   = 5, expand = True, fill = tk.BOTH)


canvas.create_window(0,0, window = subframe)
root.update_idletasks() # update geometry
canvas.config(scrollregion = canvas.bbox("all"))
canvas.xview_moveto(0) 
canvas.yview_moveto(0)

# launch the GUI
root.mainloop()
