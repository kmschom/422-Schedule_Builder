
from managerInterface import ManagerInterface
from fileIO import FileIO

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
        # self.schedules = self._createSchedules()
        # self.UI = ManagerInterface(True,self.test)
        self.fileIO = FileIO()
        (self.tutorList, self.athleteList) = self.fileIO.readFiles()
        # print(self.tutorList)


    # def _createSchedules(self):
    #     for i in range(len(athleteList)!):
    #         schedules[i] = Schedule(self.athleteList, self.tutorList, classrooms)

    def test(self,path):
        print(path)

def main():
    builder = Builder()
    # builder.run()

main()
