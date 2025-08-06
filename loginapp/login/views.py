from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.db import models
import mysql.connector
from json import dumps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import json
from django.utils.html import format_html
from django.urls import resolve
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse

import csv
import random
import string
from django.contrib.auth import logout

#dictionary to hold the meeting details
meeting = {}

#list containing the mentor schedule
mentor_meeting = []

#maintain the login status of a user
mentorlogin = False

def getmentorlogin():
    global mentorlogin
    return mentorlogin

def setmentorlogin(value):
    global mentorlogin
    mentorlogin = value

'''menteelogin = False
def getmenteelogin():
    global mentorlogin
    return mentorlogin

def setmenteelogin(value):
    global mentorlogin
    mentorlogin = value'''

managerlogin = False
def getmanagerlogin():
    global managerlogin
    return managerlogin

def setmanagerlogin(value):
    global managerlogin
    managerlogin = value

email_dict = {}


menteeans = []





#list containing the subjects of the eight semesters
subjects = [
    ["Courses","Course 1","Course 2","Course 3","Course 4","Course 5","Course 6","Course 7","Course 8"],
    ["Semester 1","Engineering Physics","Engineering Chemistry","Maths","Programming in Python","Engineering Graphics","Heritage of Tamils","Programming in Python(lab)","Physics and Chemistry Laboratory"],
    ["Semester 2","Programming and Data Structures","Complex function and Laplace Transforms","Basic Electrical and Electronic engineering","Heritage of Tamils","Physics for Information Science and Technology","Humanities","Software Development","Design thinking and Engineering Practices Lab"],
    ["Semester 3","Discrete Mathematics","Universal Human Values 2: Understanding Harmony","Programming and Design Patterns","DataBase Technology","Digital Logic and Computer Organization","Introduction to Digital Communication","Database Tecchnology Lab","Programming and Design Patterns Lab"],
    ["Semester 4","Probability and Statistics","Microprocessor and Microcotroller","Indian Constitution","Advanced Data Structures and Algorithm Analysis","Data communication and networks","Automata Theory and compiler design","Network Programming Lab","Digital Systems and Microprocessors lab"],
    ["Semester 5","Principles of Software Engineering and Practices","Data Analytics and Visualization","Principles of Operating Systems","Artificial Intelligence","Profession Elective 1","Management Elective","Software Development Project 2","Operating Systems Practices Lab"],
    ["Semester 6","Pattern Recognition and Machine Learning","Web Programming","Internet of Things and C Programming","Professional Elective 2","Open Elective 1","Mobile Application Development Lab"],
    ["Semester 7","Network and Communication Security","Cloud and Distributed Computing","Professional Elective 3","Professional Elective 4","Professional Elective 5","Project Work - Phase 1","Industrial Trainig / Internship"],
    ["Semester 8","Professional Elective 6","Open Elective 2","Project Phase 2"]
]

#defining a stack adt
class Stack:

    '''class representing a stack'''

    def __init__(self):
        self.items = []
    
    def __len__(self):
        return len(self.items)
    
    def __str__(self):
        return str(self.items)
    
    def push(self,element):
        self.items.append(element)
    
    def isempty(self):
        return (self.items == [])
    
    def top(self):
        return self.items[-1]
    
    def pop(self):
        if self.isempty():
            return False
        self.items.pop()
        return True
    
    '''def __iter__(self):
        return iter(self._items)'''

class StackEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Stack):
            return obj.items  # Serialize only the items in the stack
        return json.JSONEncoder.default(self, obj)
    


my = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "login"
)
mycursor = my.cursor()
if my.is_connected() == False:
    print("Connection not established")
else:
    print("Connection established")


# Create your views here.

def home(request):
    return render(request,'home.html')
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        mycursor.execute("SELECT * FROM login")
        result = mycursor.fetchall()
        for i in result:
            if email == i[2] and  password == i[3]:
                    name = i[1]
                    request.session["name"] = name
                    if i[4] == "Mentee":
                        name = i[1]
                        email_dict[email] = True
                        request.session["menteeemail"] = email
                        return redirect(mentee)
                        
                    elif i[4] == "Mentor":
                        setmentorlogin(True)
                        request.session["mentoremail"] = email
                        return redirect(mentor)
                    
                    elif i[4] == "Manager":
                        setmanagerlogin(True)
                        return redirect(manager)
                       
                        
            else:
                continue
        else:
            return render(request,"403.html",{"content":"LOGIN CREDENTIALS ARE INCORRECT"})
    return render(request,'home.html')

'''def loginview(request):
    user = User.objects.create_user("Abinaya", "abinaya1708@gmail.com", "summa")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request,email = email,password = password)
        if user is not None:
            login(request,user)
            return render(request,"mentor.html")
        else:
            return render(request,"403.html")
    else:
        return render(request,"home.html")'''


def mentor(request):
    val1 = getmentorlogin()
    print("mentor login",val1)
    request.session["mentoremail"] = "karthika@gmail.com"
    try:
        deletedu = request.session["delmentee"]
    except:
        deletedu = None
    print(val1)
    if val1:
        dict = {}
        mycursor.execute("Select * from personal order by Name asc")
        result = mycursor.fetchall()
        for j in result:
            dict[j[0]] = {"name":j[2],"regno":j[1]}
        #dict = {1:{"name":"Abinaya","dept":"CSE"},2:{"name":"arohi","dept":"civil"}}
        request.session["regnodict"] = dict
        return render(request,"mentor.html",{"dict":dict,"mentor":mentor_meeting,"deletedjs":deletedu})
    else:
        return render(request,"403.html",{"content":"ACCESS RESTRICTED"})

def manager(request):
    request.session["testemail"] = "shahina@gmail.com"
    val2 = getmanagerlogin()
    if val2:
        list1 = []
        mycursor.execute("Select * from personal order by Name asc")
        result = mycursor.fetchall()
        for k in result:
            list1.append(k[1])
        request.session["list1"] = list1
        return render(request,"manager.html",{"list":list1})
    else:
        return render(request,"403.html",{"content":"ACCESS RESTRICTED"})



def mentee(request):
    try:
        email = request.session["menteeemail"]
        val1 = email_dict.get(email)
        if val1 is True:
            name = request.session["name"]
            email = request.session["menteeemail"]
            print(email)
            mycursor.execute("SELECT * from personal")
            result1 = mycursor.fetchall()
            print(email)
            for j in result1:
                if str(email) == j[4]:
                    print(True)
                    personal = {
                        "regno":j[1],
                        "name":j[2],
                        "mobile":j[3],
                        "email":j[4],
                        "add":j[5],
                        "g":j[6],
                        "bg":j[7],
                        "dob":j[8],
                        "dept":j[9]
                    }
                    regno = j[1]
                    print(regno)
                    request.session["regno"] = j[1]
                    request.session["email"] = email
            mycursor.execute("SELECT * from father")
            result2 = mycursor.fetchall()
            regno = request.session["regno"]
            for k in result2:
                if regno == k[1]:
                    father = {
                        "na":k[2],
                        "em":k[3],
                        "mob":k[4],
                        "qua":k[5],
                        "occ":k[6]
                    }
            mycursor.execute("SELECT * FROM mother")
            result3 = mycursor.fetchall()
            for a in result3:
                if regno == a[1]:
                    mother = {
                        "name" : a[2],
                        "email":a[3],
                        "mobile":a[4],
                        "qua":a[5],
                        "occ":a[6]
                    }
            mycursor.execute("SELECT * FROM academic")
            result4 = mycursor.fetchall()
            for b in result4:
                if regno == b[1]:
                    academic = {
                        "high_s" : b[2],
                        "sec_s" : b[3]
                }
            print(mentor_meeting)

            return render(request,"mentee.html",{
                                    "personal":personal,
                                    "father":father,
                                    "mother":mother,
                                    "academic":academic,
                                    "mentor_meeting":mentor_meeting})
        else:
            return render(request,"403.html")
    except:
        return render(request,"403.html")

        
def add(request):
    result = False
    setmentorlogin(True)
    if request.method == "POST":
        setmentorlogin(True)
        #inserting details into the personal table
        Name = request.POST.get("name")
        Mobile = request.POST.get("mobile")
        Email = request.POST.get("email")
        Address = request.POST.get("add")
        Gender = request.POST.get('gender')
        Blood_Group = request.POST.get('bg')
        regno = request.POST.get("regno")
        DOB = request.POST.get("dob")
        Department = request.POST.get("dept")
        mycursor.execute("Select * from personal")
        result = mycursor.fetchall()
        S_No = len(result) + 1
        print(S_No)
        query = "insert into personal values({},{},'{}',{},'{}','{}','{}','{}','{}','{}');".format(S_No,regno,Name,Mobile,Email,Address,Gender,Blood_Group,DOB,Department)
        mycursor.execute(query)
        print("Personal done")

        #inserting details into the father table
        Name = request.POST.get("name")
        fname = request.POST.get("fname")
        fmail = request.POST.get("fmail")
        fmob = request.POST.get("fmob")
        fqua = request.POST.get("fqua")
        focc = request.POST.get("focc")
        mycursor.execute("Select * from father")
        result = mycursor.fetchall()
        S_No = len(result) + 1
        query = 'insert into father values({},{},"{}","{}","{}",{},"{}","{}");'.format(S_No,regno,Name,fname,fmail,fmob,fqua,focc)
        print("father done")
        mycursor.execute(query)

        #inserting details into the mother table
        Name = request.POST.get("name")
        mname = request.POST.get("mname")
        mmail = request.POST.get("mmail")
        mmob = request.POST.get("mmob")
        mqua = request.POST.get("mqua")
        mocc = request.POST.get("mocc")
        mycursor.execute("Select * from mother")
        result = mycursor.fetchall()
        S_No = len(result) + 1
        query = 'insert into mother values({},{},"{}","{}","{}",{},"{}","{}");'.format(S_No,regno,Name,mname,mmail,mmob,mqua,mocc)
        print("mpther done")
        mycursor.execute(query)

        #inserting details into the academic table
        Name = request.POST.get("name")
        perc1 = request.POST.get("perc1")
        perc2 = request.POST.get("perc2")
        mycursor.execute("Select * from academic")
        result = mycursor.fetchall()
        S_No = len(result) + 1
        query = 'insert into academic values({},{},"{}",{},{});'.format(S_No,regno,Name,perc1,perc2)
        mycursor.execute(query)
        mycursor.execute('insert into Semester(Reg_no,Name) values({},"{}")'.format(regno,Name))
        result = True
        resultjs = dumps(result)
        request.session["resultjs"] = resultjs
        mycursor.execute("Select * from login")
        result1 = mycursor.fetchall()
        sno = len(result1) + 1
        password = ''.join(random.choices(string.ascii_letters, k=7))
        mycursor.execute("Insert into login values({},'{}','{}','{}','Mentee')".format(sno,Name,Email,password))
        mycursor.execute("Insert into Achievements(Regno,Name) values({},'{}')".format(regno,Name))
        return redirect(success)

    resultjs = dumps(result)
    setmentorlogin(True)
    return render(request,"form.html",{"resultjs":resultjs})

def success(request):
    setmentorlogin(True)
    resultjs = request.session["resultjs"]
    return render(request,"form.html",{"resultjs":resultjs})

   
def delete(request):
    setmentorlogin(True)
    if request.method == "POST":
        student = request.POST.get("student")
        student = int(student)
        resultdel = False
        mycursor.execute("Select * from personal")
        result = mycursor.fetchall()
        print(student)

        for l in result:
            if l[1] == student:
                email = l[4]
                resultdel = True
        
                mycursor.execute("Delete from personal where regno = '{}'".format(student))
                mycursor.execute("Delete from login where Email = '{}'".format(email))
                mycursor.execute("Delete from father where Reg_no = {}".format(student))
                mycursor.execute("Delete from mother where Reg_no = {}".format(student))
                mycursor.execute("Delete from academic where Reg_no = {}".format(student))
                mycursor.execute("Delete from Semester where Reg_no = {}".format(student))
                mycursor.execute("Delete from notes where Reg_no = {}".format(student))
                mycursor.execute("Delete from Achievements where Regno = {}".format(student))
                try:
                    f = open("answer.txt","r")
                    list1 = f.read().split("\n")
                    index = list1.index(str(student))
                    j = 0
                    result = []
                    while j < index and list1[j] != "":
                        result.append(list1[j])
                        j+= 1
                    f.close()
                    f= open("answer.txt","w")
                    for k in result:
                        f.write(k)
                        f.write("\n")
                    resultjs = dumps(resultdel)
                    request.session["delmentee"] = resultjs
                    return redirect(mentor)
                except:
                    pass
    resultjs = dumps(resultdel)
    request.session["delmentee"] = resultjs
    return redirect(mentor)

def achieve(request):
    if request.method == "POST":
        ach = request.POST.get("achieve")
        iss = request.POST.get("issue")
        regno = request.POST.get("regno")
        name = request.POST.get("name")
        email = request.POST.get("email")
        email_dict[email] = True
        sql = "select * from Achievements where Regno = {}".format(regno)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if result[0][2]:
            newval = result[0][2] + ";" +ach
        else:
            newval = ach
        if result[0][3]:
            newval1 = result[0][3] + ";" + iss
        else:
            newval1 = iss
        sql = "update Achievements set Achievement = '{}' , Issued = '{}' where Regno = {}".format(newval,newval1,regno)
        mycursor.execute(sql)
        return redirect(mentee)
    return render(request,"mentee.html")


def detail(request):
        setmentorlogin(True)
        regno = request.GET.get("sregno")
        if regno is None:
            try:
                result = request.session["schedulejs"]
            except:
                result = False
            try:
                deleted = request.session["deleted"]
            except:
                deleted = False
            regno = request.session["regno"]
        else:
            #sname = request.POST.get("sname")
            #request.session["sname"] = sname
            result = False
            deleted = True
        
        sql = "SELECT * from Achievements where Regno = {}".format(regno)
        mycursor.execute(sql)
        xres = mycursor.fetchall()
        if not xres:
            return render(request,"404.html",{"content":"Enter the correct registration number"})
        print(xres[0][2])
        achieve = None
        issued = None
        if xres[0][2]:
            achieve = xres[0][2].split(";")
        if xres[0][3]:
            issued = xres[0][3].split(";")
        if achieve and issued:
            combined = zip(achieve,issued)
        else:
            combined = None
        mycursor.execute("SELECT * from personal order by regno asc")
        result1 = mycursor.fetchall()
        print(result1)
        for j in result1:
            if int(regno) == j[1]:
                print(True)
                personal = {
                    "regno":j[1],
                    "name":j[2],
                    "mobile":j[3],
                    "email":j[4],
                    "add":j[5],
                    "g":j[6],
                    "bg":j[7],
                    "dob":j[8],
                    "dept":j[9]
                }
                request.session["emailsend"] = j[4]
                print(personal)
                break
        else:
            return render(request,"404.html",{"content":"Registration number entered is not found"})
        mycursor.execute("SELECT * from father")
        result2 = mycursor.fetchall()
        for k in result2:
            if int(regno) == k[1]:
                father = {
                    "na":k[2],
                    "em":k[3],
                    "mob":k[4],
                    "qua":k[5],
                    "occ":k[6]
                }
                break
        mycursor.execute("SELECT * FROM mother")
        result3 = mycursor.fetchall()
        for a in result3:
            if int(regno) == a[1]:
                mother = {
                    "name" : a[3],
                    "email":a[4],
                    "mobile":a[5],
                    "qua":a[6],
                    "occ":a[7]
                }
                break
        mycursor.execute("SELECT * FROM academic")
        result4 = mycursor.fetchall()
        for b in result4:
            if int(regno) == b[1]:
                academic = {
                    "high_s" : b[3],
                    "sec_s" : b[4]
                }
                break
        mycursor.execute("SELECT * FROM notes")
        result5 = mycursor.fetchall()
        note = ""
        note1 = None
        noteStack = Stack()
        temp = []
        if not noteStack:
            for y in result5:
                if int(regno) == y[1]:
                    note = y[2]
                    for k in y[2].split(".")[:-1]:
                        k = k + "."
                        noteStack.push(k)
                        temp.append(k)
                    break
        note1 = temp
        serialized_stack = json.dumps(noteStack, cls=StackEncoder)
        request.session["noteStack"] = serialized_stack
        request.session["note"] = note
        request.session["regno"] = regno
        resultjs = dumps(result)
        deletedjs = dumps(deleted)
        print(meeting)
        print(mentor_meeting)
        data1 = None
        date = datetime.datetime.now()
        print(date)
        for y in meeting:
            if y == regno:
                if datetime.datetime.strptime(meeting[y]["Date"], '%Y-%m-%d') >= date:
                    data1 = meeting[y]
        setmentorlogin(True)
        return render(request,"detail.html",{
                            "personal":personal,
                            "father":father,
                            "mother":mother,
                            "academic":academic,
                            "note":note1,
                            "resultjs":resultjs,
                            "data1":data1,
                            "deletedjs":deletedjs,
                            "combined":combined})
'''personal = request.session["personal"]
    father = request.session["father"]
    mother = request.session["mother"]
    academic = request.session["academic"]
    return render(request,"detail.html",{
                                    "personal":personal,
                                    "father":father,
                                    "mother":mother,
                                    "academic":academic,
                                    "note":note})'''
  

def note(request):
    '''view to handle POST request when mentor wants to add a note'''
    setmentorlogin(True)
    if request.method == "POST":
        date = str(datetime.datetime.now().date())
        print(date)
        notes = '[' + date + '] '
        notes += request.POST.get("notes")
        print(notes) 
        regno = request.session["regno"]
        mycursor.execute("SELECT * FROM notes")
        temp = mycursor.fetchall()
        for u in temp:
            if int(regno) == u[1]:
                if u[2]:
                    notes = u[2] + notes
                print("Updated notes:",notes)
                query = "update notes set Notes = '{}' where Reg_no = {}".format(notes,regno)
                mycursor.execute(query)
                break
        else:
            S_No = len(temp) + 1
            query = "insert into notes values({},{},'{}')".format(S_No,regno,notes)
            mycursor.execute(query)
        deleted = True
        request.session["deleted"] = deleted
        request.session["regno"] = regno
        print("In notes:",regno)
        scheduled = False
        request.session["schedulejs"] = False
        return redirect("notes")
    #return redirect(detail)

#view for the notes
def notes(request):
    if request.method == "GET":
        regno = request.session['regno']
        mycursor.execute("SELECT * FROM notes")
        result5 = mycursor.fetchall()
        note = ""
        note1 = None
        noteStack = Stack()
        temp = []
        if not noteStack:
            for y in result5:
                if int(regno) == y[1]:
                    note = y[2]
                    for k in y[2].split(".")[:-1]:
                        k = k + "."
                        noteStack.push(k)
                        temp.append(k)
                    break
        note1 = temp
        serialized_stack = json.dumps(noteStack, cls=StackEncoder)
        request.session["noteStack"] = serialized_stack
        request.session["note1"] = note1
        print("Notes:",note1)
    elif request.method == "POST":
        note = request.POST.get('note_value')
        regno = request.session['regno']
        note1 = request.session["note1"]
        note1.remove(note)
        deletestring = ""
        for i in note1:
            deletestring += i
        print("delete",deletestring)
        query = "update notes set Notes = '{}' where Reg_no = {}".format(deletestring,regno)
        mycursor.execute(query)
        return redirect("notes")
            
    return render(request,"note.html",{"note":note1})


def back(request):
    return redirect(mentor)

def schedule(request):
    if request.method == "POST":
        setmentorlogin(True)
        result = True
        deleted = True
        request.session["deleted"] = deleted
        request.session["result"] = result
        regno = request.session["regno"]
        subject = request.POST.get("subject")
        date = request.POST.get("date")
        time = request.POST.get("time")
        location = request.POST.get("location")
        email = request.session["emailsend"]
        event_details = f"Your mentor has scheduled a meeting on {date} at {time}."
        #sending mail
        from_email = "nbaggie2027@gmail.com"
        message = "Meeting scheduled"
        #setting parameters for the google calender
        start_datetime = f"{date.replace('-','')}T{time.replace(':','')}00Z"

        calendar_params = {
            "action" : "TEMPLATE",
            "text" : subject,
            "dates" : start_datetime,
            "details" : event_details,
            "location":location,
        }
        calender_link = f"https://www.google.com/calendar/render?{urlencode(calendar_params)}"

        html_message = f"""
        <html>
        <head>
        <style>
        body {{
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #4b79a1;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .meeting-details {{
            background-color: #f9f9f9;
            border-left: 4px solid #4b79a1;
            padding: 15px;
            margin: 20px 0;
        }}
        .meeting-details ul {{
            list-style-type: none;
            padding: 0;
            margin: 0;
        }}
        .meeting-details li {{
            margin-bottom: 10px;
        }}
        .meeting-details strong {{
            color: #4b79a1;
            margin-right: 10px;
        }}
        .calendar-link {{
            display: inline-block;
            background-color: #4b79a1;
            color: white;
            padding: 10px 15px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 15px;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
            text-align: center;
        }}
        </style>
        </head>
        <body>
            <h1>Meeting Scheduled</h1>
            <p>Your mentor has scheduled a meeting:</p>
            <ul>
                <li><strong>Date:</strong> {date}</li>
                <li><strong>Time:</strong> {time}</li>
                <li><strong>Place:</strong> {location}</li>
            </ul>
            <p>You can <a href="{calender_link}" target="_blank">add this meeting to your Google Calendar</a>.</p>
            <p>Please contact your mentor for more details.</p>
        </body>
        </html>
        """

        send_mail(subject, message,from_email, [email] , html_message=html_message)
        #messages.success(request, 'Successfully Sent The Message!')        
        return redirect(detail)

'''def edit(request):
    result = False
    request.session["result"] = result
    print(father)
    return render(request,"edit.html",{
                            "personal":personal,
                            "father":father,
                            "mother":mother,
                            "academic":academic,})'''


def semester(request):
    setmentorlogin(True)
    #final_table = "<table>\n<tr>{}</tr>\n{}</table>".format('\n'.join('<th>{}</th>'.format(i) for i in subjects[0]), '<tr>{}</tr>'.format('\n'.join('\n'.join(['<td>{}</td>'.format(b) for b in i]) for i in subjects[1:])))
    #table  = tabulate(subjects, headers="firstrow", tablefmt="html")
    if request.method == "GET":
        regno1 = request.GET.get("sturegno")
        dept = request.GET.get("studept")
        request.session["sturegno"] = regno1
        request.session["dept"] = dept
    else:
        regno1 = request.session["sturegno"]
        dept = request.session["dept"]
    result = False
    request.session["result"] = result
    request.session["deleted"] = True
    request.session["testemail"] = True
    request.session["schedulejs"] = False
    return render(request,"marks.html",{
        "Regno":regno1,
        "dept":dept,
        "subject":subjects
    })
    



def deletelatest(request):
        setmentorlogin(True)
        serialized_stack = request.session["noteStack"]
        deserialized_stack = json.loads(serialized_stack)
        if  not deserialized_stack:
             deleted = False
        else:
            deserialized_stack.pop()
            string = ""
            for j in deserialized_stack:
                string = string + j
            #sname = request.session["sname"]
            regno = request.session["regno"]
            sql = "update notes set Notes = '{}' where Reg_no = {} ".format(string,regno)
            mycursor.execute(sql)
            deleted = True
        result = False
        request.session["result"] = result
        request.session["deleted"] = deleted
        print(deleted)
        return redirect(detail)

def forgot(request):
    setmentorlogin(True)
    if request.method == "POST":
        email = request.POST.get("email")
        newpass = request.POST.get("newpass")
        mycursor.execute("SELECT * FROM login")
        result = mycursor.fetchall()
        for l in result:
            if l[2] == email:
                sql = "update login set Password = '{}' where Email = '{}'".format(newpass,email)
                mycursor.execute(sql)
                break
        print(newpass)
        return render(request,"forgot.html")
    return render(request,"forgot.html")



def enter(request):
    setmentorlogin(True)
    if request.method == "POST":
        schedule = request.session["schedulejs"]
        request.session["schedulejs"] = schedule
        result = False
        request.session["result"] = result
        request.session["deleted"] = True
        semesterno = request.POST.get("semester")
        regno = request.session["sturegno"]
        dept = request.session["dept"]
        course1 = request.POST.get("1")
        course2 = request.POST.get("2")
        course3 = request.POST.get("3")
        course4 = request.POST.get("4")
        course5 = request.POST.get("5")
        course6 = request.POST.get("6")
        course7 = request.POST.get("7")
        course8 = request.POST.get("8")
        cgpa = request.POST.get("cgpa")
        semester = "Semester_"+semesterno
        mark = ",".join([cgpa,course1,course2,course3,course4,course5,course6,course7,course8])
        sql = "update Semester set {} = '{}' where Reg_no = '{}'".format(semester,mark,regno)
        mycursor.execute(sql)
        return render(request,"marks.html",{
        "Regno":regno,
        "dept":dept,
        "subject":subjects
    })

def viewmarks(request):
    if request.method == "GET":
        setmentorlogin(True)
        result = False
        request.session["result"] = result
        request.session["deleted"] = True
        regno = request.session["sturegno"]
        dept = request.session["dept"]
        schedule = request.session["schedulejs"]
        request.session["schedulejs"] = schedule
        
            
        semester = request.GET.get("values")
        final = []
        mycursor.execute("Select * from Semester where Reg_no = '{}'".format(regno))
        result = mycursor.fetchall()
        semester1 = int(semester)
        print(result)
        string = result[0][semester1+1]
        print(string)
        
        if string:
            print(string)
            listofsem = string.split(',')
            mark_dict = {}
            print(listofsem)
            temp =  subjects[semester1]
            mark_dict["CGPA"] = listofsem[0]
            try:
                index = listofsem.index("0")
            except:
                index = len(listofsem)
            for i in range(1,index):
                mark_dict[temp[i]] = listofsem[i]
            final.append(subjects[i])
            final.append(listofsem)
            print(final)

            print(result)
            print(mark_dict)
            return render(request,"marks.html",{
                "Regno":regno,
                "dept":dept,
                "semester":semester,
                "result":mark_dict,
                "subject":subjects
            })
            
        elif string is None:
            return render(request,"404.html")
        else:
            return redirect(semester)

def postquestion(request):
    setmentorlogin(True)
    return render(request,"questions.html",{"range":range(1,11)})

def createquestion(request):
    setmentorlogin(True)
    if request.method == "POST":
        questionList = []
        for j in range(1, 11):
            temp = request.POST.get(str(j))
            if temp != "":
                questionList.append(temp)
        
        # Save questions to the file
        with open("question.txt", "w") as f:
            for i in questionList:
                f.write(i + "\n")

        # Clear answer file (if needed)
        with open("answer.txt", 'w') as file:
            pass
        
        # Send a JSON response to indicate success
        return JsonResponse({"success": True})

    return render(request, "mentor.html")

def answer(request):
    email = request.session["menteeemail"]
    email_dict[email] = True
    result = False
    regno_answered = False  # Flag to check if the user has answered already

    # Read questions from the file
    with open("question.txt", "r") as f:
        s = f.read()
    temp = s.split("\n")
    temp = temp[:-1]  # Removing the last empty element after splitting

    # Check if user has already answered
    regno = request.session.get("regno")
    with open("answer.txt", "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if lines[i].strip() == str(regno):
            regno_answered = True
            break  # Break once regno is found

    # Handling POST request to save answers
    if request.method == "POST" and not regno_answered:
        answerList = []

        # Collecting answers from the POST data
        for k in range(1, len(temp) + 1):
            temp1 = request.POST.get(str(k))
            answerList.append(temp1)

        # Write the updated content to the file
        with open("answer.txt", "a") as f:
            f.write(str(regno) + "\n")
            for l in answerList:
                f.write(l + "\n")
            f.write("\n")

        result = True

    # Send the updated question list to the template
    number = [i for i in range(1, 11)][:len(temp)]
    combined_list = list(zip(temp, number))  # Convert zip to list

    resultjs = dumps(result)
    return render(request, "answer.html", {"list": combined_list, "resultjs": resultjs, "regno_answered": regno_answered})


def viewans(request):
    setmentorlogin(True)
    dict = request.session["regnodict"]
    return render(request,"viewans.html",{"dict":dict})

def ans(request):
    if request.method == "GET":
        # Retrieve 'mentee' from the query parameters
        registration = request.GET.get("mentee")
        
        if not registration:
            return JsonResponse({"error": "Mentee ID not provided"}, status=400)

        # Read questions
        with open("question.txt", "r") as f:
            questions = f.read().split("\n")[:-1]

        # Read answers
        with open("answer.txt", "r") as f:
            answer_list = f.read().split("\n")

        try:
            # Find answers corresponding to the mentee ID
            index = answer_list.index(str(registration)) + 1
            result = []
            while index < len(answer_list) and answer_list[index] != "":
                result.append(answer_list[index])
                index += 1
        except ValueError:
            # Handle case where mentee ID is not found in answer list
            return render(request, "viewans.html", {"error": "No answers found for the given mentee ID."})

        # Combine questions and answers for rendering
        combined = zip(questions, result)
        dict = request.session["regnodict"]
        # Pass the result to the template
        return render(request, "viewans.html", {"resultlist": combined, "registeration": registration,"dict":dict})

    return JsonResponse({"error": "Invalid request method"}, status=405)

def log1(request):
    email = request.session["testemail"]
    try:
        emailone = request.session["menteeemail"]
        if emailone:
            email_dict[emailone] = False
    except:
        pass
    try:
        emailtwo = request.session["mentoremail"]
        if emailtwo:
            setmentorlogin(False)
    except:
        pass
    print(email)
    mycursor.execute("Select Role from login where Email = '{}'".format(email))
    result = mycursor.fetchall()
    print(result)
    #if email == "karthika@gmail.com":
     #   setmentorlogin(False)'''
    if email == "shahina@gmail.com":
        setmanagerlogin(False)
    return redirect(login)



def manager_view(request):
    if request.method == "GET":
        regno = request.GET.get("sregno")
        semester = request.GET.get("values")
        final = []
        mycursor.execute("Select * from Semester where Reg_no = '{}'".format(regno))
        result78 = mycursor.fetchall()
        semester1 = int(semester)
        print(result78)
        if result78 !=[] :
            string = result78[0][semester1+1]
        else:
            return render(request,"404.html",{"content":"Enter the correct registration number"})
        print(string)
        
        if string:
            print(string)
            listofsem = string.split(',')
            mark_dict = {}
            print(listofsem)
            temp =  subjects[semester1]
            mark_dict["CGPA"] = listofsem[0]
            try:
                index = listofsem.index("0")
            except:
                index = len(listofsem)
            for i in range(1,index):
                mark_dict[temp[i]] = listofsem[i]
            final.append(subjects[i])
            final.append(listofsem)
            print(final)

            print(mark_dict)
            return render(request,"manager.html",{
                "Regno":regno,
                "semester":semester,
                "result":mark_dict,
                "subject":subjects
            })
            
        elif string is None:
            return render(request,"404.html")
       

