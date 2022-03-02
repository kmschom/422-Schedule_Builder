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
Created file                    my 2/12/22
Implemented required queue      ks, my 2/19/22
Implemented optional queue      ks 2/23/22

"""

from tutor import Tutor
from athlete import Athlete
from appointment import Appointment
import random
from queue import PriorityQueue


class Schedule:
    def __init__(self, athleteDataList, tutorDataList, classrooms):
        self.a = 0
        self.athleteList = []
        # print(athleteList)
        self.tutorList = []
        self._createLists(athleteDataList, tutorDataList)
        self.classrooms = classrooms
        self.score = 0
        self.required = self._createRequired()
        self.optional = self._createOptional()
        self.appointments = []
        self.score = 0


    def _createLists(self, athleteDataList, tutorDataList):
        for tu in tutorDataList:
            self.tutorList.append(Tutor(tu))

        for ath in athleteDataList:
            self.athleteList.append(Athlete(ath))
        # print("lengths are", (self.athleteList[0].availability))

    def makeSchedule(self):
        self._scheduleRequired()
        self._scheduleOptional()
        # print(self.required)
        return self.score

    def _scheduleRequired(self):
        # print("I'M HERE\n")
        # print(self.required)
        while not self.required.empty():
            # print("In queue\n")
            scheduled = False
            currentDay = 0
            ath = self.required.get()[1]
            # print(ath)
            while not scheduled:
                # print("In scheduled\n")
                # print(ath.availability)
                availability = ath.availability[currentDay]
                for time in availability:
                    for (sub,hours) in ath.hoursLeft:
                        if hours > 0:
                            for tut in self.tutorList:
                                if sub in tut.subjects:
                                    if time in tut.availability[currentDay]:
                                        self.appointments.append(
                                            Appointment((time, currentDay), tut, ath, sub, self.classrooms[0]))
                                        # print("Made an appt\n")
                                        ath.hours -= 1
                                        if ath.hours > 1:
                                            self.required.put((1 / ath.hours, ath, ath.hours))
                                        ath.availability[currentDay].remove(time)
                                        tut.availability[currentDay].remove(time)
                                        ath.hoursLeft.remove((sub,hours))
                                        self.score+=1000
                                        if (hours - 1 > 0):
                                            ath.hoursLeft.append((sub, hours-1))


                                        scheduled = True
                                if scheduled:
                                    break
                        if scheduled:
                            break
                    if scheduled:
                        break

                if currentDay < 4:
                    currentDay += 1
                else:
                    currentDay = 0
                    while not scheduled:
                        availability = ath.availability[currentDay]
                        # check for existing appointments
                        for appt in self.appointments:
                            if currentDay == appt.day:
                                for time in availability:
                                    if time == appt.time:
                                        for sub,hours in ath.hoursLeft:
                                            if hours> 0:
                                                if sub == appt.subject:
                                                    if len(appt.athletes) < 3:
                                                        appt.athletes.append(ath)
                                                        # print("Added athlete to an appointment\n")
                                                        ath.hours -= 1
                                                        if ath.hours > 1:
                                                            self.required.put((1 / ath.hours, ath, ath.hours))
                                                        ath.availability[currentDay].remove(time)
                                                        ath.hoursLeft.remove((sub,hours))
                                                        if (hours - 1 > 0):
                                                            ath.hoursLeft.append((sub, hours-1))
                                                        scheduled = True
                                                        self.score+=1000
                                            if scheduled:
                                                break
                                    if scheduled:
                                        break
                            if scheduled:
                                break

                        if currentDay < 4:
                            currentDay += 1
                        else:
                            break
                    break
        # print(self.appointments, len(self.appointments))

    def _scheduleOptional(self):
        # print("In optional scheduling\n")
        # print(self.optional)
        while not self.optional.empty():
            scheduled = False
            currentDay = 0
            ath = self.optional.get()[1]
            # print(ath)
            while not scheduled:
                # print("In scheduled\n")
                # print(ath.availability)
                availability = ath.availability[currentDay]
                for time in availability:
                    for (sub,hours) in ath.hoursLeft:
                        if hours > 0:
                            for tut in self.tutorList:
                                if sub in tut.subjects:
                                    if time in tut.availability[currentDay]:
                                        self.appointments.append(Appointment((time, currentDay), tut, ath, sub, self.classrooms[0]))
                                        # print("Made an appt\n")
                                        ath.hours -= 1
                                        if ath.hours > 1:
                                            self.optional.put((1 / ath.hours, ath, ath.hours))
                                        ath.availability[currentDay].remove(time)
                                        tut.availability[currentDay].remove(time)
                                        ath.hoursLeft.remove((sub,hours))
                                        if (hours - 1 > 0):
                                            ath.hoursLeft.append((sub, hours-1))
                                        scheduled = True
                                        self.score +=1
                                if scheduled:
                                    break
                        if scheduled:
                            break
                    if scheduled:
                        break
                if currentDay < 4:
                    currentDay += 1
                else:
                    currentDay = 0
                    while not scheduled:
                        availability = ath.availability[currentDay]
                        # check for existing appointments
                        for appt in self.appointments:
                            if currentDay == appt.day:
                                for time in availability:
                                    if time == appt.time:
                                        for sub,hours in ath.hoursLeft:
                                            if hours > 0:
                                                if sub == appt.subject:
                                                    if len(appt.athletes) < 3:
                                                        appt.athletes.append(ath)
                                                        # print("Added athlete to an appointment\n")
                                                        ath.hours -= 1
                                                        if ath.hours > 1:
                                                            self.optional.put((1 / ath.hours, ath, ath.hours))
                                                        ath.availability[currentDay].remove(time)
                                                        scheduled = True
                                                        self.score += 1
                                                        ath.hoursLeft.remove((sub,hours))
                                                        if (hours - 1 > 0):
                                                            ath.hoursLeft.append((sub, hours-1))
                                            if scheduled:
                                                break
                                    if scheduled:
                                        break
                            if scheduled:
                                break
                        if currentDay < 4:
                            currentDay += 1
                        else:
                            break
                    break
        # print(self.appointments, len(self.appointments))

    def _createRequired(self):
        # Create prio queue

        decimals = []
        for i in range(1000):
            decimals.append(i)
        rangee = 999
        reqQ = PriorityQueue()
        for ath in self.athleteList:
            if ath.required:
                # print(ath)
                x = (random.randint(0, rangee))
                ath.hours += decimals[x]/ 1000
                decimals.remove(decimals[x])
                rangee -= 1
                reqQ.put((1 / ath.hours, ath, ath.hours))
        # while not reqQ.empty():
        #     next_item = reqQ.get()
        #     print(next_item)
        return reqQ

    def _createOptional(self):
        # Create prio queue
        decimals = []
        for i in range(1000):
            decimals.append(i)
        rangee = 999
        optQ = PriorityQueue()
        for ath in self.athleteList:
            if not ath.required:
                # print(ath)
                x = (random.randint(0, rangee))
                ath.hours += decimals[x]/ 1000
                decimals.remove(decimals[x])
                rangee -= 1
                # print(ath.name, ath.lastname)
                optQ.put((1 / ath.hours, ath, ath.hours))
        # while not optQ.empty():
        #    next_item = optQ.get()
        #    print(next_item)
        return optQ
