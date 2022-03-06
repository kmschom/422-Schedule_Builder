"""
Name: ScheduleSystem.py
Purpose: Contains main execution flow and is responsible for being the interaction between the modules that make up the system

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: Mert Yapucuoğlu (my)

ScheduleSystem.py is part of the All In a Week's Work (AWW) Schedule Building software which takes input on athlete and tutor
availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    None

Modifications:
Created file                                                    my 2/12/22
Wrote skeleton code                                             my 2/16/22
Implemented _createSchedules and getBestSchedule functions      my 2/24/22
Code documentation                                              ks 3/1/22
Implemented writeCSV function                                   my 3/2/22
Implemented exportIndividual function                           km 3/3/22
Reworked exportIndividual function and added readLoad function  my 3/4/22
"""

from managerInterface import ManagerInterface       # calls Manager Interface to update user interface with new scheduling information
from fileIO import FileIO                           # calls fileIO to access read and write functions
from scheduler import Scheduler                     # calls schedule to create initial schedule objects
from tutor import Tutor                             # calls Tutor class to build tutor objects and insert to appointment object
from athlete import Athlete                         # calls Athlete class to build athlete objects and insert to appointment object
from appointment import Appointment                 # calls Appointment to make and append appointment objects to bestSchedule
import copy                                         # imports copy to deepcopy

# list of all classrooms available for tutoring
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

class ScheduleSystem:
    def __init__(self):
        self.fileIO = FileIO()          # FileIO object
        self.tutorDataList = []         # list of tutor data; filled in signalSchedule function; initialized as empty
        self.athleteDataList = []       # list of athlete data; filled in signalSchedule function; initialized as empty
        self.schedules = []             # list of schedule objects; initialized as empty

        # if appointment.txt file exists, self.scheduleExists = True and self.loadData will hold list of appointments
        (self.scheduleExists, self.loadData) = self.fileIO.readSave()
        # check if a schedule has been created
        if self.scheduleExists:
            # writes appointments to self.bestSchedule
            self.readLoad()
        # update manager interface with new prompts now that a schedule has been created
        self.UI = ManagerInterface(self.scheduleExists, self.signalSchedule, self.exportIndividual)

    def _createSchedules(self):
        for i in range(1):
            sch = Scheduler(copy.deepcopy(self.athleteDataList), copy.deepcopy(self.tutorDataList), classrooms)  # makes new schedule object to fill in as another schedule iteration
            sch.makeSchedule()
            self.schedules.append(sch)

    def getBestSchedule(self):
        bestScore = 0   # holds the score of the best schedule found
        # look at each schedule iteration in list of schedules
        for sch in self.schedules:
            # check if current schedule score is higher than the best score
            if sch.score > bestScore:
                # if so, reassign bestSchedule to current schedule and reassign bestScore to current schedule's score
                self.bestSchedule = sch.appointments
                bestScore = sch.score

    def showAppointments(self, schedule):
        for appt in schedule.appointments:
            print(appt)

    def signalSchedule(self, athletePath, tutorPath):
        # tuple holding the error log, tutor data, and athlete data returned from the input files read in fileIO
        (self.errorLog, self.tutorDataList, self.athleteDataList) = self.fileIO.readFiles(athletePath,tutorPath)

        # check error log status
        if len(self.errorLog) == 2:
            return (False, self.errorLog[1])
        if len(self.errorLog) > 2:
            self.fileIO.createErrorReport(self.errorLog)
            return (False, "ERROR! Please look into errorLog.txt for details")

        self._createSchedules()
        self.getBestSchedule()
        # self.showAppointments(self.bestSchedule)
        self.fileIO.writeFiles(self.bestSchedule)
        return (True, "Format: Name Lastname")

    def exportIndividual(self, name):
        individualApptList = [] # list of appointments assigned to an individual; initialized as empty
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
            return "Name not found" # currently returning name not found regardless if name exists or not (as of 1:08am 3/5)

    def readLoad(self):
        self.bestSchedule = []  # list of appointments that make up the best schedule iteration; initialized as empty
        for appt in self.loadData:
            athList = []    # list of athlete objects to be added to appointment object; initialized as empty
            for ath in appt[0]:
                athList.append(Athlete({"id": None, "name":ath[0], "lastname":ath[1],
                "availability":[], "subjects": [], "hours":0,"required":False}))

            tut = Tutor({"id": None, "name":appt[4][0], "lastname":appt[4][1],
            "availability":[], "subjects": [], "hours":0})  # tutor object to be added to appointment object

            self.bestSchedule.append(Appointment([appt[1],appt[2]],tut,athList,appt[3],appt[5][:-1]))

def main():
    system = ScheduleSystem() # Schedule System object

main()

