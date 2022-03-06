"""
Name: builder.py
Purpose: ?

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: ???

builder.py is part of the All In a Week's Work (AWW) Schedule Building software which takes input on athlete and tutor
availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    ???

Modifications:
Created file                    my 2/12/22
???
Code documentation              ks 3/1/22
"""

from managerInterface import ManagerInterface
from fileIO import FileIO
from schedule import Schedule
from tutor import Tutor
from athlete import Athlete
from appointment import Appointment
import copy

classrooms =[
"201","202","203","204",
"205","206","207","208",
"209","210","211","212",
"213","214","215","301",
"302","303","304","305",
"306","307","308","309",
"310","311","312","313",
"314","315","316","317",
]

class Builder:
    def __init__(self):
        self.fileIO = FileIO()
        self.tutorDataList = []
        self.athleteDataList = []
        self.schedules = []
        (self.scheduleExists, self.loadData) = self.fileIO.readSave()
        if self.scheduleExists:
            self.readLoad()

        self.UI = ManagerInterface(self.scheduleExists, self.signalSchedule, self.exportIndividual)

    def _createSchedules(self):
        for i in range(1):
            sch = Schedule( copy.deepcopy(self.athleteDataList), copy.deepcopy(self.tutorDataList), classrooms)
            sch.makeSchedule()
            self.schedules.append(sch)

    def getBestSchedule(self):
        bestScore = 0
        for sch in self.schedules:
            if sch.score > bestScore:
                self.bestSchedule = sch.appointments
                bestScore = sch.score

    def showAppointments(self, schedule):
        i = 0
        for appt in schedule.appointments:
            print(appt)

    def signalSchedule(self, athletePath, tutorPath):

        (self.errorLog, self.tutorDataList, self.athleteDataList) = self.fileIO.readFiles(athletePath,tutorPath)

        if len(self.errorLog) == 2:
            return (False, self.errorLog[1])
        if len(self.errorLog) > 2:
            self.fileIO.createErrorReport(self.errorLog)
            return (False, "ERROR! Please look into errorLog.txt for details")

        self._createSchedules()
        self.getBestSchedule()
        # self.showAppointments(self.bestSchedule)
        self.fileIO.writeCSV(self.bestSchedule)
        return (True, "Format: Name Lastname")

    def exportIndividual(self, name):
        individualApptList = []
        print(name)
        try:
            last,first = name.split(" ")
        except:
            return "Invalid Format! Correct Format: Name Lastname"
        for appt in self.bestSchedule:
            for ath in appt.athletes:
                if ath.name == first and ath.lastname == last:
                    individualApptList.append(appt)




        if len(individualApptList) > 0:
            self.fileIO.individualSchedule(individualApptList, f"{first}_{last}")
            return "Individual Schedule Created"
        else:
            return "Name not found"                         # currently returning name not found regardless if name exists or not (as of 1:08am 3/5)

    def readLoad(self):
        self.bestSchedule = []
        for appt in self.loadData:
            athList = []
            for ath in appt[0]:
                athList.append(Athlete({"id": None, "name":ath[0], "lastname":ath[1],
                "availability":[], "subjects": [], "hours":0,"required":False}))

            tut = Tutor({"id": None, "name":appt[4][0], "lastname":appt[4][1],
            "availability":[], "subjects": [], "hours":0})

            self.bestSchedule.append(Appointment([appt[1],appt[2]],tut,athList,appt[3],appt[5][:-1]))

def main():
    builder = Builder()
    # builder.run()

main()
