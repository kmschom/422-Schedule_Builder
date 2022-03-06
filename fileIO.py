"""
Name: fileIO.py
Purpose: To read and interpret the files that are imported into the system as well as write the schedules that want to
be exported.

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: Mert Yapucuoğlu (my), Brianna Vago (bv), Kassandra Morando (km)

fileIO.py is part of the All In a Week's Work (AWW) Schedule Building software which takes input on athlete and tutor
availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    builder.py -

Modifications:
Created file                      my 2/12/22
Implemented readFiles function    bv 2/23/22
Implemented writeCSV function     km 3/3/22
Implemented individualSchedule    km 3/2/22
Code title documentation          ks 3/1/22
Implemented writeSave function    km 2/26/22
Implemented readSave function     bv 3/3/22
Code documentation                km,bv
"""

import csv
import appointment
import pandas as pd
from datetime import date
import os

class FileIO:
    def readFiles(self, athFilePath, tutFilePath):
        """This function reads the athlete and tutor csv files and
        writes the proper information for each athlete and tutor into
        their own dictionary. It then returns a list of dictionaries
        for the athletes and for the tutors"""

        errorLog = [date.today()]

        """------------TESTING FILE EXTENSIONS------------"""
        if athFilePath[-3:] != "csv" or tutFilePath[-3:] != "csv":
            errorLog.append("ERROR! Files need to be in .csv format")
            return (errorLog,None,None)

        """------------TESTING FILE OPEN START------------"""
        try:
            testfile1 = open(athFilePath)
        except IOError:
            errorLog.append("ERROR! Cannot open athlete file")
            return (errorLog,None,None)

        try:
            testfile2 = open(tutFilePath)
        except IOError:
            errorLog.append("ERROR! Cannot open tutor file")
            return (errorLog,None,None)
        """------------TESTING FILE OPEN END------------"""

        headingsA = []      # holds the headings of the athlete file to check if file contents hold all information
        athlete_dict = []   # holds the dictionary of athletes
        headingsT = []      # holds the headings of the tutor file to check if file contents hold all information
        tutor_dict = []     # holds the dictionary of tutors

        # This section filters through the athlete list file which is file1
        with open(athFilePath, 'r') as athletes_list:
            # This takes the headings of athlete and puts them in a list.
            headingsA = athletes_list.readline()

            """------------TESTING HEADINGS ATHLETE START------------"""
            # Headings must be: "First Name,Last Name,ID,GPA,Year,Hours Wanted,Subjects,Availability" in this order.
            athleteTester = "first name,last name,id,gpa,year,hours wanted,subjects,availability"
            lheadA = headingsA.lower().strip()
            if athleteTester != lheadA:
                errorLog.append("ERROR! Athete file headers are wrong")
                return (errorLog,None,None)

            """------------TESTING HEADINGS ATHLETE END------------"""

            # This splits each athlete's info and sets required to false
            for index,row in enumerate(athletes_list):
                temp = row.split(",")                   # a list of information collected from file
                temp[6] = temp[6].split(" ")            # Classes
                temp[7] = temp[7].strip().split("/")    # Availability
                req = False                             # Boolean that says if hours are required or not

                """------------TESTING NAME START------------"""
                testerFirst = temp[0].isalpha()
                testerLast = temp[1].isalpha()
                if testerLast is False or testerFirst is False:
                    errorLog.append(f"Invalid name format at line {index+1} of athlete file")
                """------------TESTING NAME END------------"""

                """------------TESTING GPA, YEAR, ID, HOURS START------------"""
                try:
                    float(temp[3])  # GPA
                    float(temp[4])  # Year
                    float(temp[2])  # ID
                    float(temp[5])  # Hours
                except ValueError:
                    errorLog.append(f"Invalid GPA/YEAR/ID/HOUR format at line {index+1} of athlete file")

                if 0 >= float(temp[3]) or float(temp[3]) > 4:
                    # Check GPA input
                    errorLog.append(f"GPA can't below 0 ar above 4. {index+1} of athlete file")

                if 0 >= float(temp[4]) or float(temp[4]) > 4:
                    # Check Year input
                    errorLog.append(f"Year can't below 0 ar above 4. {index+1} of athlete file")

                if float(temp[5]) >= 8:
                    # Check Hour input
                    temp[5] = 8
                """------------TESTING GPA, YEAR, ID, HOURS END------------"""

                # Required testing for when to set to true
                # True if gpa is 2.99 or below.
                if float(temp[3]) <= 2.29 or float(temp[4]) == 1:
                    temp[5] = '8'
                    req = True
                elif 2.30 <= float(temp[3]) <= 2.59:
                    temp[5] = '6'
                    req = True
                elif 2.60 <= float(temp[3]) <= 2.99:
                    temp[5] = '4'
                    req = True

                # This makes the availability list of lists
                extra = []                       # used to make week list, time of each day will be placed here
                day = 0                          # day of the week
                week = [[], [], [], [], []]      # availability list for a whole week

                # This makes the availability a list of lists by adding each available
                # time into a week list
                for item in temp[7]:
                    if len(item) != 0:
                        extra = item.split(" ")
                        for time in extra:
                            week[day].append(int(time))
                    day = day + 1

                # This makes the athletes dictionary and appends it into a long list of dictionaries
                DictA = {"id": int(temp[2]), "name": temp[0], "lastname": temp[1],
                         "availability": week, "subjects": temp[6], "hours": int(temp[5]), "required": req}     # Dictionary of one athlete
                athlete_dict.append(DictA)

        # This section filters through the tutor list file called tutor.csv
        with open(tutFilePath, 'r') as tutor_list:
            # This takes the headings of tutor and puts them in a list.
            headingsT = tutor_list.readline()

            """------------TESTING HEADINGS TUTOR START------------"""
            # Headings must be: "First Name,Last Name,ID,Hours Wanted,Subjects,Availability" in this order.
            tutorTester = "first name,last name,id,hours wanted,subjects,availability"
            lheadT = headingsT.lower().strip()
            # if tutorTester != lheadT:
            #     return 0
            """------------TESTING HEADINGS TUTOR END------------"""

            # This splits each tutor's info
            for row in tutor_list:
                temp = row.split(",")                   # a list of information collected from file
                temp[4] = temp[4].split(" ")            # Classes
                temp[5] = temp[5].strip().split("/")    # Availability

                """------------TESTING NAME START------------"""
                testerFirst = temp[0].isalpha()
                testerLast = temp[1].isalpha()

                if testerLast is False or testerFirst is False:
                    errorLog.append(f"Invalid name format at line {index+1} of tutor file")

                """------------TESTING NAME END------------"""

                """------------TESTING ID, HOURS START------------"""
                try:
                    float(temp[2])  # ID
                    float(temp[3])  # Hours
                except ValueError:
                    errorLog.append(f"Invalid ID/HOUR format at line {index+1} of tutor file")

                if float(temp[3]) >= 25:
                    # Check Hour input
                    temp[3] = 25
                """------------TESTING ID, HOURS END------------"""

                # This makes the availability list of lists
                extra = []                      # used to make week list, time of each day will be placed here
                day = 0                         # day of the week
                week = [[], [], [], [], []]     # availability list for a whole week

                # This makes the availability a list of lists by adding each available
                # time into a week list
                for item in temp[5]:
                    if len(item) != 0:
                        extra = item.split(" ")
                        for time in extra:
                            week[day].append(int(time))
                    day = day + 1

                # This makes the tutors dictionary and appends it into a long list of dictionaries
                DictB = {"id": int(temp[2]), "name": temp[0], "lastname": temp[1], "availability": week,
                         "subjects": temp[4], "hours": int(temp[3])}    # Dictionary of one tutor
                tutor_dict.append(DictB)

        return (errorLog, tutor_dict, athlete_dict)


    def readSave(self):
        """This reads the appointment.txt file and writes the proper information for each appointment into
                their own dictionary. It then returns a list of dictionaries."""

        appts = []  # holds the dictionary of appointments
        # This opens and reads the appointment file
        try:
            full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Schedule")
            filename = "appointment.txt"
            new_path = os.path.join(full_path,filename)
            with open(new_path, "r") as file:
                # This splits the appointment info from the .txt file
                for row in file:
                    data = row.split(" ")
                    athletes = data[0].split("/")
                    athInfo = []
                    for ath in athletes:
                        athInfo.append(ath.split(","))
                    time = data[1]
                    day = data[2]
                    subject = data[3]
                    tutor = data[4].split(",")
                    classroom = data[5]

                    appts.append([athInfo, time, day, subject, tutor, classroom])
        except:
            return(False, None)



        return (True,appts)

    #writes a text file with all of apppointments from a list
    def writeSave(self,appointments):
        #assigns a variable to a text file
        appointment_f = "appointment.txt"
        new_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Schedule")
        new_dir = os.path.join(new_path,appointment_f)

        # opens and writes to the text file
        with open(new_dir,"w") as app_file:

            #loops through appointments list
            for i in range(0,len(appointments)):

                #assigns output to a string of a row in appointments
                output = str(appointments[i])

                #writes output and new line to the text file
                app_file.write(output)
                app_file.write('\n')

    #write a csv of all the appointments for the week using a list of appointments
    def writeCSV(self,appointments):

        #assigns filename to a csv file
        full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Schedule")
        filename = "schedule.csv"
        new_path = os.path.join(full_path,filename)
        if os.path.isdir(full_path)==False:
            os.mkdir(full_path)
        # 3D Array to keep list of appointments by day and hour
        appts = []
        for i in range(5):
            asd = []
            for j in range(24):
                asd.append([])
            appts.append(asd)

        # 2D Array to keep the number of appointments for each day/hour period
        lengthIndex = []
        for i in range(24):
            asd = []
            for j in range(5):
                asd.append(0)
            lengthIndex.append(asd)


        #elements that are needed for the first row of the csv file
        header = ['Time','Monday','Tuesday','Wednesday','Thursday','Friday']

        #opens and writes to the schedule.csv
        with open(new_path,"w",newline='') as finalSchedule:

            #loops through a list of appointments
            for app in appointments:

                # Create the info statement of each appointment and add it to the 3D list
                appts[int(app.day)][int(app.time)].append(repr(app))

                # Increment the number of appointments for that hour/day index
                lengthIndex[int(app.time)][int(app.day)] += 1


            # The list that will contain the
            timeColumn = []

            #Adds the times to the time column
            for time in range(8,24):
                maxlen = max(lengthIndex[time])
                for i in range(maxlen):
                    timeColumn.append(time)
                timeColumn.append("") # an empty row at the end of a hour period

            # Getting rid of the empty row at the very end
            timeColumn = timeColumn[:-1]

            # 2D list to keep day/hour list of appointments
            dayColumns = [[], [], [], [], []]

            # Goes through each day and hour
            for day in range(0,5):
                for time in range(8,24):
                    for a in appts[day][time]:
                        if a=="":
                            appts[day][time].remove(a)

                    # Gets the appointment list length of the hour with the highest amount of appointments
                    # for that hour period
                    maxLen = max(lengthIndex[time])
                    length = len(appts[day][time])

                    # Adds empty rows to the hourly appointment list it until it reaches the longest columnn
                    for i in range(length, maxLen):
                        appts[day][time].append("")

                # Adds all the hourly appointment lists together to get a daily appointment list
                for timeAppts in appts[day][8:]:
                    dayColumns[day].extend(timeAppts)
                    dayColumns[day].append("")

            #Create writer
            writer = csv.writer(finalSchedule)

            # Write the columns headers
            writer.writerow(header)

            # Rows to add each row to write
            rows = []

            # Go through indexes of the day with the most amount of appointments
            for i in range(len(timeColumn)):
                # Add the appointment lists for that hour of all days to the row
                rows.append([timeColumn[i],dayColumns[0][i],dayColumns[1][i],dayColumns[2][i],dayColumns[3][i],dayColumns[4][i]])

            #write to file
            writer.writerows(rows)

        #calls writeSave to create an appointment text file
        self.writeSave(appointments)
        #closes the file that was opened and written into
        finalSchedule.close()

    #writes a csv file of appointments for an individual athlete for the week using a list of appointments and an individuals name
    def individualSchedule(self,appointments,name):
        #elements that are needed for the first row of the csv file
        column = ['Time','Monday','Tuesday','Wednesday','Thursday','Friday']
        mine = [] #initializes the list that goes into a row in the csv
        filename = f"{name}.csv" #names the csv file

        new_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Schedule")
        new_dir = os.path.join(new_path,filename)

        # 3D Array to keep list of appointments by day and hour
        appts = []
        for i in range(5):
            asd = []
            for j in range(24):
                asd.append([])
            appts.append(asd)

        # 2D Array to keep the number of appointments for each day/hour period
        lengthIndex = []
        for i in range(24):
            asd = []
            for j in range(5):
                asd.append(0)
            lengthIndex.append(asd)


        #elements that are needed for the first row of the csv file
        header = ['Time','Monday','Tuesday','Wednesday','Thursday','Friday']

        #opens and writes to the schedule.csv
        with open(new_dir,"w",newline='') as individualSchedule:

            #loops through a list of appointments
            for app in appointments:

                # Create the info statement of each appointment and add it to the 3D list
                appts[int(app.day)][int(app.time)].append(repr(app))

                # Increment the number of appointments for that hour/day index
                lengthIndex[int(app.time)][int(app.day)] += 1


            # The list that will contain the
            timeColumn = []

            #Adds the times to the time column
            for time in range(8,24):
                maxlen = max(lengthIndex[time])
                for i in range(maxlen):
                    timeColumn.append(time)
                timeColumn.append("") # an empty row at the end of a hour period

            # Getting rid of the empty row at the very end
            timeColumn = timeColumn[:-1]

            # 2D list to keep day/hour list of appointments
            dayColumns = [[], [], [], [], []]

            # Goes through each day and hour
            for day in range(0,5):
                for time in range(8,24):
                    for a in appts[day][time]:
                        if a=="":
                            appts[day][time].remove(a)

                    # Gets the appointment list length of the hour with the highest amount of appointments
                    # for that hour period
                    maxLen = max(lengthIndex[time])
                    length = len(appts[day][time])

                    # Adds empty rows to the hourly appointment list it until it reaches the longest columnn
                    for i in range(length, maxLen):
                        appts[day][time].append("")

                # Adds all the hourly appointment lists together to get a daily appointment list
                for timeAppts in appts[day][8:]:
                    dayColumns[day].extend(timeAppts)
                    dayColumns[day].append("")

            #Create writer
            writer = csv.writer(individualSchedule)

            # Write the columns headers
            writer.writerow(header)

            # Rows to add each row to write
            rows = []

            # Go through indexes of the day with the most amount of appointments
            for i in range(len(timeColumn)):
                # Add the appointment lists for that hour of all days to the row
                rows.append([timeColumn[i],dayColumns[0][i],dayColumns[1][i],dayColumns[2][i],dayColumns[3][i],dayColumns[4][i]])

            #write to file
            writer.writerows(rows)

        #closes the file that was opened and written into
        individualSchedule.close()

    # Creates a txt file containing error lines
    def createErrorReport(self,errorLog):
        f = open("errorLog.txt", "w")

        for line in errorLog:
            f.write(line)

        f.close()
