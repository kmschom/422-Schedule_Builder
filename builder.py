
from managerInterface import ManagerInterface
from fileIO import FileIO
from schedule import Schedule
from tutor import Tutor
from athlete import Athlete

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

        self.tutorList = []
        self.athleteList = []
        self._createLists()
        self.schedules = self._createSchedules()

    def _createSchedules(self):
        for i in range(3):
            schedules[i] = Schedule(self.athleteList, self.tutorList, classrooms)

    def _createLists(self):
        for tu in self.tutorDataList:
            self.tutorList.append(Tutor(tu))

        for ath in self.athleteDataList:
            self.athleteList.append(Athlete(ath))

    def test(self,path):
        print(path)

def main():
    builder = Builder()
    # builder.run()

main()
