
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
        self.UI = ManagerInterface(self.scheduleExists, self.signalSchedule)

    def _createSchedules(self):
        for i in range(100):
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
        (self.tutorDataList, self.athleteDataList) = self.fileIO.readFiles()
        self._createSchedules()
        self.getBestSchedule()
        self.showAppointments(self.bestSchedule)
        return True

    # def extractIndividual(self, name):
    #     individualApptList = []
    #     for appt in self.bestSchedule.appointments:


def main():
    builder = Builder()
    # builder.run()

main()
