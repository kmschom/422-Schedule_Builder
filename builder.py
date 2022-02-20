# import fileIO as *
# import schedule
from managerInterface import ManagerInterface
#The main of our program
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
        self.UI = ManagerInterface(True,self.test)

    # def getImport():
    #     #Use fileIO functions
    #     #imports = fileIO.readFiles
    #     #self.athleteList = import[0]
    #     #self.tutorList = import[1]
    #     self.b = 0

    # def _createSchedules(self):
    #     for i in range(len(athleteList)!):
    #         schedules[i] = Schedule(self.athleteList, self.tutorList, classrooms)

    def test(self,path):
        print(path)

def main():
    builder = Builder()
    # builder.run()

main()