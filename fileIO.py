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
Implemented writeCSV function     km
Code title documentation          ks 3/1/22
Implemented writeSave function    km
Implemented readSave function     bv 3/3/22
"""

import csv
import appointment

class FileIO:
    def readFiles(self, athFilePath, tutFilePath):
        """This function reads the athlete and tutor csv files and
        writes the proper information for each athlete and tutor into
        their own dictionary. It then returns a list of dictionaries
        for the athletes and for the tutors"""

        """------------TESTING FILE OPEN START------------"""
        try:
            testfile1 = open(athFilePath)
            testfile2 = open(tutFilePath)
        except IOError:
            return 0
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
                return 0
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
                # if testerLast is False or testerFirst is False:
                #     return 1
                """------------TESTING NAME END------------"""

                """------------TESTING GPA, YEAR, ID, HOURS START------------"""
                try:
                    float(temp[3])  # GPA
                    float(temp[4])  # Year
                    float(temp[2])  # ID
                    float(temp[5])  # Hours
                except ValueError:
                    return 2
                if 0 >= float(temp[3]) or float(temp[3]) > 4:
                    # Check GPA input
                    return 3
                if 0 >= float(temp[4]) or float(temp[4]) > 4:
                    # Check Year input
                    print("index:",index)
                    return 4
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
            #     print("ERROR")
            #     return
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
                    return 6
                """------------TESTING NAME END------------"""

                """------------TESTING ID, HOURS START------------"""
                try:
                    float(temp[2])  # ID
                    float(temp[3])  # Hours
                except ValueError:
                    return 7
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

        return(tutor_dict, athlete_dict)


    def readSave(self):
        return

    def writeSave(self,appointments):
        appointment_f = "appointment.txt"
        with open(appointment_f,"w") as app_file:
            for i in range(0,len(appointments)):
                output = str(appointments[i])
                app_file.write(output)
                app_file.write('\n')

    def writeCSV(self,appointments):
        #add_cascade
        #a=2

        #write a text file with all of the apppointments by row
        filename = "schedule.csv"
        column = ['Time','Monday','Tuesday','Wednesday','Thursday','Friday']
        data = []

        #writes a big file
        with open(filename,"w") as finalSchedule:
            for i in range(0,len(appointments)):
                app = str(appointments[i]).split(" ")
                #slips each line and assigns each element to variable
                time = app[0]
                day = app[1]
                athlete = app[2]
                subject = app[3]
                tutor = app[4]
                classroom = app[5]

                #assign the appointment to a certain day
                if (day == '0'):
                    col_num = 1
                elif (day == '1'):
                    col_num = 2
                elif (day == '2'):
                    col_num = 3
                elif (day == '3'):
                    col_num = 4
                elif (day == '4'):
                    col_num = 5
                data.append({column[0]:time,column[col_num]:[athlete,tutor,subject,classroom]})


            #write into a file csv file
            writer = csv.DictWriter(finalSchedule, fieldnames = column)

            #writes the column names
            writer.writeheader()

            #writes data into the rows
            writer.writerows(data)

        self.writeSave(appointments)
        self.individualSchedule(appointments,"Brianna")
        finalSchedule.close()
    def individualSchedule(self,appointments,name):
        column = ['Time','Monday','Tuesday','Wednesday','Thursday','Friday']
        mySchedule = []
        filename = "mySchedule.csv"
        with open(filename,"w") as mySchedule:
            for i in range(0,len(appointments)):
                app = str(appointments[i]).split(" ")
                name_doc = str(app[2])[:-1][1:]
                time = str(app[0])
                day = str(app[1])
                athlete = name
                subject = str(app[3])
                tutor = str(app[4])
                classroom = str(app[5])

                #assign the appointment to a certain day
                if (day == '0'):
                    col_num = 1
                elif (day == '1'):
                    col_num = 2
                elif (day == '2'):
                    col_num = 3
                elif (day == '3'):
                    col_num = 4
                elif (day == '4'):
                    col_num = 5

                if str(name_doc)==str(name):
                    mySchedule.append({column[0]:time,column[col_num]:[athlete,tutor,subject,classroom]})
            #write into a file csv file
            writer = csv.DictWriter(mySchedule, fieldnames = column)

            #writes the column names
            writer.writeheader()

            #writes data into the rows
            writer.writerows(mySchedule)
