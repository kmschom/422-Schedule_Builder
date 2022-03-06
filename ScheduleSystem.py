"""
Name: ScheduleSystem.py
Purpose: Contains main execution flow and is responsible for being the interaction between the modules that make up the system

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: Mert Yapucuoğlu (my)

ScheduleSystem.py is part of the JTAS(JAQUA Tutor Appointment Scheduler) Schedule Building software which takes input on
athlete and tutor availability and builds a schedule of tutoring appointments for the entire group.
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

# Schedule System class; holds functions to create schedule objects, find the best schedule, and signal the schedule reading and writing
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

    # make numerous schedule objects to test many potential schedules
    def _createSchedules(self):
        for i in range(100):
            sch = Scheduler(copy.deepcopy(self.athleteDataList), copy.deepcopy(self.tutorDataList), classrooms)  # makes new schedule object to fill in as another schedule iteration
            sch.makeSchedule()
            self.schedules.append(sch)

    # compare the scores calculated for each schedule and compare to fine the highest scored schedule
    def getBestSchedule(self):
        bestScore = 0   # holds the score of the best schedule found
        # look at each schedule iteration in list of schedules
        for sch in self.schedules:
            # check if current schedule score is higher than the best score
            if sch.score > bestScore:
                # if so, reassign bestSchedule to current schedule and reassign bestScore to current schedule's score
                self.bestSchedule = sch.appointments
                bestScore = sch.score

    # print all appointments
    def showAppointments(self, schedule):
        for appt in schedule.appointments:
            print(appt)

    # receives file path from managerInterface and uses fileIO function readFiles to read those files; returns an error message or proceeds to creating schedules
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

    # read through all appointments, store the appointments that include the input "name" and write an individual schedule using fileIO
    def exportIndividual(self, name):
        individualApptList = [] # list of appointments assigned to an individual; initialized as empty
        print(name)
        # check and store format of inputted name
        try:
            first,last = name.split(" ")    # first and last name of inputted athlete name
        except:
            return "Invalid Format! Correct Format: First_name Last_name"

        # look through all appointments in the schedule
        for appt in self.bestSchedule:
            # look at every athlete assigned to an appointment
            for ath in appt.athletes:
                # if input name matches appointment name, append to list of individual appointments
                if ath.name == first and ath.lastname == last:
                    individualApptList.append(appt)

            # if input name matches appointment name, append to list of individual appointments
            if appt.tutor.name == first and appt.tutor.lastname == last:
                individualApptList.append(appt)

        # if inputted individual has any appointments, write appointments to a file using fileIO
        if len(individualApptList) > 0:
            self.fileIO.individualSchedule(individualApptList, f"{first}_{last}")
            return "Individual Schedule Created"
        else:
            return "Name not found" # currently returning name not found regardless if name exists or not (as of 1:08am 3/5)

    # reads in athlete and tutor data from a previously existing appointment list; adds this loaded data to a schedule object
    def readLoad(self):
        self.bestSchedule = []  # list of appointments that make up the best schedule iteration; initialized as empty
        # look at each appointment from loaded data
        for appt in self.loadData:
            athList = []    # list of athlete objects to be added to appointment object; initialized as empty
            # store athlete data from each appointment
            for ath in appt[0]:
                athList.append(Athlete({"id": None, "name":ath[0], "lastname":ath[1],
                "availability":[], "subjects": [], "hours":0,"required":False}))

            # store tutor data from each appointment
            tut = Tutor({"id": None, "name":appt[4][0], "lastname":appt[4][1],
            "availability":[], "subjects": [], "hours":0})  # tutor object to be added to appointment object

            # build Appointment object and add to a Schedule object
            self.bestSchedule.append(Appointment([appt[1],appt[2]],tut,athList,appt[3],appt[5][:-1]))

def main():
    system = ScheduleSystem() # Schedule System object

main()
