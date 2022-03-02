import xlrd
from appointment import Appointment
from athlete import Athlete
from tutor import Tutor
# def __init__(self, time, tutor, athlete, subject, classroom):
import copy
import math
import random
loc = ("./betterData.xls")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

sheet.cell_value(0, 0)

print(sheet.nrows)

appts = []



apptList = []
for i in range((sheet.nrows)):

    allData = sheet.row_values(i)
    hour = allData[0]
    for dayIndex in [1,2,3,4,5]:
        dayData = allData[dayIndex]
        split = dayData.split("\n")
        elements = []
        for element in split:
            elements += element.split(" ")

        classInput = [False, False]
        tutorInput = [False, False]
        athleteInput = [True, False]
        athleteName = ""
        tutorName = ""
        subject = ""
        skip = False
        resetting = False
        for index,element in enumerate(elements):
            if element == "w/":
                continue
            if skip:
                skip = False
                continue
            elif resetting:
                try:
                    if elements[index+3] == "w/":
                        resetting = False
                    else:
                        continue
                except:
                    break
            elif element == "Staff":
                skip = True
                continue
            elif element == "Course:":
                classInput[0] = True

            elif classInput[0]:
                subject += element
                classInput[0] = False
                classInput[1] = True
            elif classInput[1]:
                subject += element
                classInput[1] = False
                apptList.append(Appointment([copy.deepcopy(hour),copy.deepcopy(dayIndex-1)],copy.deepcopy(tutorName),copy.deepcopy(athleteName),copy.deepcopy(subject),"100"))
                athleteInput = [True, False]
                athleteName = ""
                tutorName = ""
                subject = ""
                resetting = True
            elif tutorInput[1]:
                tutorName += " " +element
                tutorInput[1] = False
                classInput[0] = True
            elif tutorInput[0]:
                tutorName += element
                tutorInput[0] = False
                tutorInput[1] = True
            elif athleteInput[1]:
                athleteName += element
                athleteInput[1] = False
                tutorInput[0] = True
            elif athleteInput[0]:
                athleteName += element
                athleteInput[0] = False
                athleteInput[1] = True

# print(apptList[1])
deleted = 0
for a in apptList:
    try:
        print(a)
    except:
        apptList.remove(a)
        deleted += 1
tutorList = []
athleteList = []
id = 100
for a in apptList:

    if (a.tutor.split(" ")[0] == "Flowe") or (a.tutor.split(" ")[0] == "Flowe"):
        continue
    athleteExists = False
    tutorExists = False
    for tutor in tutorList:
        if (tutor.name == a.tutor.split(" ")[0] and tutor.lastname == a.tutor.split(" ")[1]):
            tutorExists = True
            if a.subject not in tutor.subjects:
                tutor.subjects.append(a.subject)

            if math.floor(int(a.time)) not in tutor.availability[a.day]:
                tutor.availability[a.day].append(math.floor(int(a.time)))
                tutor.hours += 1
    if not tutorExists:
        data = {
        "id": id,
        "name": a.tutor.split(" ")[0],
        "lastname": a.tutor.split(" ")[1],
        "availability": [[],[],[],[],[]],
        "subjects": [],
        "hours": 0
        }

        tutorList.append(Tutor(data))
        id += 1
    for athlete in athleteList:
        if (athlete.name == (a.athletes[0].split(","))[0] and athlete.lastname == (a.athletes[0].split(","))[1]):
            athleteExists = True
            if a.subject not in athlete.subjects:
                athlete.subjects.append(a.subject)

            if (athlete.hours == 8):
                athlete.required = True
            if math.floor(int(a.time)) not in athlete.availability[a.day]:
                athlete.availability[a.day].append(math.floor(int(a.time)))
                athlete.hours += 1
    if not athleteExists:
        try:
            data = {
            "id": id,
            "name": (a.athletes[0].split(","))[0],
            "lastname": (a.athletes[0].split(","))[1],
            "availability": [[],[],[],[],[]],
            "subjects": [],
            "hours": 0,
            "required": False
            }

            print(a.athletes[0].split(","))
            athleteList.append(Athlete(data))
            id += 1
        except:
            print("ba")
            deleted += 1


for ath in athleteList:
    if ath.hours == 0:
        athleteList.remove(ath)
    # else:
    #     print(ath, ath.hours, ath.subjects, ath.availability, ath.required)
# print("-------------------------------------")
for tut in tutorList:
    if tut.hours == 0:
        tutorList.remove(tut)
    # else:
    #     print(tut, tut.lastname, tut.hours, tut.subjects, tut.availability)

print(deleted)

gpa = []
year = []

for ath in athleteList:
    for ava in ath.availability:
        amount = random.randint(1, 3)
        while amount:
            time = random.randint(8, 20)
            if time in ava:
                continue
            else:
                ava.append(time)
                amount -= 1
        ava.sort()
    if ath.hours < 8:
        gpa.append(random.uniform(2,4))
        year.append(random.randint(2,4))
    else:
        coin = random.random()
        if coin < 0.33:
            gpa.append(random.uniform(0,2))
            year.append(random.randint(2,4))
        else:
            gpa.append(random.uniform(2,4))
            year.append(1)


for tut in tutorList:
    for ava in tut.availability:
        amount = random.randint(1, 3)
        while amount:
            time = random.randint(8, 20)
            if time in ava:
                continue
            else:
                ava.append(time)
                amount -= 1
        ava.sort()
    tut.hours += 2


athFile = open("bigAth.csv", "w")
athFile.write("First Name,Last Name,ID,GPA,Year,Hours Wanted,Subjects,Availability")
for index,ath in enumerate(athleteList):
    availabilityString = ""
    for ava in ath.availability:
        for time in ava:
            availabilityString += (str(time)+" ")
        availabilityString = availabilityString[:-1]
        availabilityString += "/"
    subjectString = ""
    for sub in ath.subjects:
        if sub[-1] == ",":
            sub = sub[:-1]
        subjectString += (sub+" ")
    subjectString = subjectString[:-1]
    availabilityString = availabilityString[:-1]
    line = f"{ath.name},{ath.lastname},{ath.id},{gpa[index]},{year[index]},{ath.hours},{subjectString},{availabilityString}\n"
    athFile.write(line)


tutFile = open("bigTut.csv", "w",encoding='utf-8-sig')
tutFile.write("﻿First Name,Last Name,ID,Hours Wanted,Subjects,Availability")
for index,tut in enumerate(tutorList):
    availabilityString = ""
    for ava in tut.availability:
        for time in ava:
            availabilityString += (str(time)+" ")
        availabilityString = availabilityString[:-1]
        availabilityString += "/"
    subjectString = ""
    for sub in tut.subjects:
        if sub[-1] == ",":
            sub = sub[:-1]
        subjectString += (sub+" ")
    subjectString = subjectString[:-1]
    availabilityString = availabilityString[:-1]
    line = f"{tut.name},{tut.lastname},{tut.id},{tut.hours},{subjectString},{availabilityString}\n"
    tutFile.write(line)
