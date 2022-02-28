
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
        self.a= 0

        # self.UI = ManagerInterface(True,self.test)
        self.fileIO = FileIO()
        (self.tutorDataList, self.athleteDataList) = self.fileIO.readFiles()
        # print(self.tutorList)
        print(self.tutorDataList)
        # self._createLists()
        self.schedules = self._createSchedules()
        self.bestSchedule = self.getBestSchedule()

        self.showAppointments(self.bestSchedule)
        print(self.bestSchedule.score)

    def _createSchedules(self):
        schedules = []
        for i in range(1):
            # print(self.athleteList, "asd")
            print(i)
            sch = Schedule( copy.deepcopy(self.athleteDataList), copy.deepcopy(self.tutorDataList), classrooms)
            sch.makeSchedule()

            schedules.append(sch)
        return schedules

    def _createLists(self):
        for tu in self.tutorDataList:
            self.tutorList.append(Tutor(tu))

        for ath in self.athleteDataList:
            self.athleteList.append(Athlete(ath))

    def getBestSchedule(self):
        bestSchedule = None
        bestScore = 0
        for sch in self.schedules:
            if sch.score > bestScore:
                bestSchedule = sch
                bestScore = sch.score
        return bestSchedule

    def showAppointments(self, schedule):
        i = 0
        for appt in schedule.appointments:
            print(appt)

def main():
    builder = Builder()
    # builder.run()

main()
