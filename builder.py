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
        self.bestSchedule = None
        self.scheduleExists = False #Replace with file check function once done
        self.UI = ManagerInterface(self.scheduleExists, self.signalSchedule, None, self.exportIndividual)

    def _createSchedules(self):
        for i in range(1):
            sch = Schedule( copy.deepcopy(self.athleteDataList), copy.deepcopy(self.tutorDataList), classrooms)
            sch.makeSchedule()
            self.schedules.append(sch)

    def getBestSchedule(self):
        bestScore = 0
        for sch in self.schedules:
            if sch.score > bestScore:
                self.bestSchedule = sch
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
        self.fileIO.writeCSV(self.bestSchedule.appointments)
        return (True, None)

    def exportIndividual(self, name):
        #individualApptList = []
        #print(name)
        # for appt in self.bestSchedule.appointments
        self.fileIO.individualSchedule(self.bestSchedule.appointments,name)


def main():
    builder = Builder()
    # builder.run()

main()
