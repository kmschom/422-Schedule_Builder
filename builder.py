"""
Name: builder.py
Purpose: ???

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
"100",
"101",
"102",
"103",
"104",
"105",
]

class Builder:
    def __init__(self):

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
        #POSSIBLY CHECK FOR VALIDITY
        self.fileIO = FileIO()
        print(athletePath, tutorPath)
        (self.tutorDataList, self.athleteDataList) = self.fileIO.readFiles(athletePath,tutorPath)
        # print(self.fileIO.readFiles(athletePath,tutorPath))
        self._createSchedules()
        self.getBestSchedule()
        self.showAppointments(self.bestSchedule)
        self.fileIO.writeCSV(self.bestSchedule.appointments)

        return True

    def exportIndividual(self, name):
        individualApptList = []
        print(name)
        # for appt in self.bestSchedule.appointments:


def main():
    builder = Builder()
    # builder.run()

main()
