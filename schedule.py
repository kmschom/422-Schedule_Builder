"""
Name: schedule.py
Purpose: Schedule class to contain the information about an individual scheduling variation, along with the algorithm to fill itself.

Creation Date: Feb. 12, 2022
Last Updated: Feb. 19, 2022
Authors: Mert Yapucuoğlu (my), Kelly Schombert (ks)

schedule.py is part of the Schedule_Builder software.
Called by:
    builder.py -


Modifications:
Created file    my 2/12/22

"""


import athlete
import tutor
import appointment
import random
from queue import PriorityQueue

class Schedule:
    def __init__(self, athleteList, tutorList, classrooms):
        self.a = 0
        self.athleteList = athleteList
        self.tutorList = tutorList
        self.classrooms = classrooms
        self.score = 0
        self.required = self._createRequired()
        self.optional = self._createOptional()

    def makeSchedule():
        self._scheduleRequired()
        self._scheduleOptional()

    def _scheduleRequired(self):
        return 0

    def _scheduleOptional(self):
        return 0

    def _createRequired(self):
        #Create prio queue
        reqQ = PriorityQueue()
        for ath in self.athleteList:
            if ath.required:
                x = (random.randint(0,999)) / 1000
                ath.hours += x
                reqQ.put((ath.hours, ath))

    def _createOptional(self):
        #Create prio queue
        optQ = PriorityQueue()
        for ath in self.athleteList:
            if not ath.required:
                x = (random.randint(0,999)) / 1000
                ath.hours += x
                optQ.put((ath.hours, ath))
