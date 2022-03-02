"""
Name: schedule.py
Purpose: Creates Schedule class to hold information on individual scheduling variations and run scheduling algorithms to
build appointments.

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: Mert Yapucuoğlu (my), Kelly Schombert (ks)

schedule.py is part of the All In a Week's Work (AWW) Schedule Building software which takes input on athlete and tutor
availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    builder.py - calls Schedule class 100 times within _createSchedules to make and score multiple schedule iterations

Modifications:
Created file                    my 2/12/22
Implemented required queue      ks, my 2/19/22
Implemented optional queue      ks 2/23/22
Implemented scoring system      my 2/24/22
Code documentation              ks 3/1/22
"""

from tutor import Tutor  # calls Tutor class to build tutor objects and add to tutorList
from athlete import Athlete  # calls Athlete class to build athlete objects and add to athleteList
from appointment import Appointment  # calls Appointment class to build and schedule appointment objects
import random  # used to determine athlete placement in priority queues
from queue import PriorityQueue  # calls PriorityQueue class to build required and optional athlete queues


# Schedule class; holds functions to create tutor and athlete lists, make priority queues, and run both scheduling algorithms
class Schedule:
    # initializes Schedule attributes passed to class from builder._createSchedules
    def __init__(self, athleteDataList, tutorDataList, classrooms):
        self.athleteList = []  # list of athlete objects; initialized as empty
        self.tutorList = []  # list of tutor objects; initialized as empty
        self._createLists(athleteDataList, tutorDataList)
        self.classrooms = classrooms  # list of classrooms
        self.score = 0  # schedule's effectiveness score; initialized as empty
        self.required = self._createRequired()  # queue of required hours; initialized with createRequired function
        self.optional = self._createOptional()  # queue of optional hours; initialized with createOptional function
        self.appointments = []  # list of appointment objects made; initialized as empty

    # takes list of athlete and tutor data, processes data into Athlete and Tutor objects and appends to athleteList and tutorList
    def _createLists(self, athleteDataList, tutorDataList):
        for tu in tutorDataList:
            self.tutorList.append(Tutor(tu))

        for ath in athleteDataList:
            self.athleteList.append(Athlete(ath))

    # calls scheduling algorithms and returns resulting schedule effectiveness score
    def makeSchedule(self):
        self._scheduleRequired()
        self._scheduleOptional()
        return self.score

    # scheduling algorithm to schedule all required athlete hours
    def _scheduleRequired(self):
        # while there are required athlete hours to be scheduled as individual appointments
        while not self.required.empty():
            scheduled = False  # indicator that athlete hasn't been scheduled on this pass; intialized as False
            currentDay = 0  # tracks the day being scheduled on; initialized as 0 referring to Monday
            ath = self.required.get()[1]  # holder for athlete object currently at top of priority queue
            # while this athlete's schedule is incomplete
            while not scheduled:
                availability = ath.availability[currentDay]  # list of athlete's available hours based on currentDay
                # look at every hour in athlete's availability list
                for time in availability:
                    # look at remaining hours needed for each subject
                    for (sub, hours) in ath.hoursLeft:
                        # if there are hours needing to be scheduled
                        if hours > 0:
                            # look at each tutor on tutorList
                            for tut in self.tutorList:
                                # if subject in tutor's list of offered subjects
                                if sub in tut.subjects:
                                    # if tutor is available at time in question
                                    # create Appointment object, update availability hours and schedule score
                                    if time in tut.availability[currentDay]:
                                        self.appointments.append(
                                            Appointment((time, currentDay), tut, ath, sub, self.classrooms[0]))
                                        ath.hours -= 1
                                        # if athlete has remaining hour(s) to schedule, reinsert to priority queue
                                        if ath.hours > 1:
                                            self.required.put((1 / ath.hours, ath, ath.hours))
                                        ath.availability[currentDay].remove(time)
                                        tut.availability[currentDay].remove(time)
                                        ath.hoursLeft.remove((sub, hours))
                                        self.score += 1000
                                        # if subject has remaining hour(s) to schedule, reinsert to list
                                        if (hours - 1 > 0):
                                            ath.hoursLeft.append((sub, hours - 1))
                                        scheduled = True
                                if scheduled:
                                    break
                        if scheduled:
                            break
                    if scheduled:
                        break

                # increment to look at next day of the week
                if currentDay < 4:
                    currentDay += 1
                # if all days of week have been looked at for individual appointments
                else:
                    currentDay = 0
                    # while this athlete's schedule is incomplete
                    while not scheduled:
                        availability = ath.availability[currentDay]
                        # look at all existing appointments on schedule
                        for appt in self.appointments:
                            # if appointments occur on currentDay
                            if currentDay == appt.day:
                                # look at every hour in athlete's availability list
                                for time in availability:
                                    # if athlete is available at same time as an existing appointment
                                    if time == appt.time:
                                        # look at remaining hours needed for each subject
                                        for sub, hours in ath.hoursLeft:
                                            # if there are hours needing to be scheduled
                                            if hours > 0:
                                                # if subject matches the appointment's subject
                                                if sub == appt.subject:
                                                    # if there are less than 3 athletes already in the appointment
                                                    # add athlete to appointment, update athlete availability and schedule score
                                                    if len(appt.athletes) < 3:
                                                        appt.athletes.append(ath)
                                                        ath.hours -= 1
                                                        # if athlete has remaining hour(s) to schedule, reinsert to priority queue
                                                        if ath.hours > 1:
                                                            self.required.put((1 / ath.hours, ath, ath.hours))
                                                        ath.availability[currentDay].remove(time)
                                                        ath.hoursLeft.remove((sub, hours))
                                                        # if subject has remaining hour(s) to schedule, reinsert to list
                                                        if (hours - 1 > 0):
                                                            ath.hoursLeft.append((sub, hours - 1))
                                                        scheduled = True
                                                        self.score += 500
                                            if scheduled:
                                                break
                                    if scheduled:
                                        break
                            if scheduled:
                                break

                        # increment to look at next day of the week
                        if currentDay < 4:
                            currentDay += 1
                        # as many required athlete hours as possible have been scheduled
                        else:
                            break
                    break

    # scheduling algorithm to schedule all optional athlete hours
    def _scheduleOptional(self):
        # while there are required athlete hours to be scheduled as individual appointments
        while not self.optional.empty():
            scheduled = False  # indicator that athlete hasn't been scheduled on this pass; initialized as False
            currentDay = 0  # tracks the day being scheduled on; initialized as 0 referring to Monday
            ath = self.optional.get()[1]  # holder for athlete object currently at top of priority queue
            # while this athlete's schedule is incomplete
            while not scheduled:
                availability = ath.availability[currentDay]  # list of athlete's available hours based on currentDay
                # look at every hour in athlete's availability list
                for time in availability:
                    # look at remaining hours needed for each subject
                    for (sub, hours) in ath.hoursLeft:
                        # if there are hours needing to be scheduled
                        if hours > 0:
                            # look at each tutor on tutorList
                            for tut in self.tutorList:
                                # if subject in tutor's list of offered subjects
                                if sub in tut.subjects:
                                    # if tutor is available at time in question
                                    # create Appointment object, update availability hours and schedule score
                                    if time in tut.availability[currentDay]:
                                        self.appointments.append(
                                            Appointment((time, currentDay), tut, ath, sub, self.classrooms[0]))
                                        ath.hours -= 1
                                        # if athlete has remaining hour(s) to schedule, reinsert to priority queue
                                        if ath.hours > 1:
                                            self.optional.put((1 / ath.hours, ath, ath.hours))
                                        ath.availability[currentDay].remove(time)
                                        tut.availability[currentDay].remove(time)
                                        ath.hoursLeft.remove((sub, hours))
                                        # if subject has remaining hour(s) to schedule, reinsert to list
                                        if (hours - 1 > 0):
                                            ath.hoursLeft.append((sub, hours - 1))
                                        scheduled = True
                                        self.score += 1
                                if scheduled:
                                    break
                        if scheduled:
                            break
                    if scheduled:
                        break

                # increment to look at next day of the week
                if currentDay < 4:
                    currentDay += 1
                # if all days of week have been looked at for individual appointments
                else:
                    currentDay = 0
                    # while this athlete's schedule is incomplete
                    while not scheduled:
                        availability = ath.availability[currentDay]
                        # look at all existing appointments on schedule
                        for appt in self.appointments:
                            # if appointments occur on currentDay
                            if currentDay == appt.day:
                                # look at every hour in athlete's availability list
                                for time in availability:
                                    # if athlete is available at same time as an existing appointment
                                    if time == appt.time:
                                        # look at remaining hours needed for each subject
                                        for sub, hours in ath.hoursLeft:
                                            # look at remaining hours needed for each subject
                                            if hours > 0:
                                                # if subject matches the appointment's subject
                                                if sub == appt.subject:
                                                    # if there are less than 3 athletes already in the appointment
                                                    # add athlete to appointment, update athlete availability and schedule score
                                                    if len(appt.athletes) < 3:
                                                        appt.athletes.append(ath)
                                                        # print("Added athlete to an appointment\n")
                                                        ath.hours -= 1
                                                        # if athlete has remaining hour(s) to schedule, reinsert to priority queue
                                                        if ath.hours > 1:
                                                            self.optional.put((1 / ath.hours, ath, ath.hours))
                                                        ath.availability[currentDay].remove(time)
                                                        scheduled = True
                                                        self.score += 1
                                                        ath.hoursLeft.remove((sub, hours))
                                                        # if subject has remaining hour(s) to schedule, reinsert to list
                                                        if (hours - 1 > 0):
                                                            ath.hoursLeft.append((sub, hours - 1))
                                            if scheduled:
                                                break
                                    if scheduled:
                                        break
                            if scheduled:
                                break

                        # increment to look at next day of the week
                        if currentDay < 4:
                            currentDay += 1
                        # as many required athlete hours as possible have been scheduled
                        else:
                            break
                    break

    # Creates priority queue of athlete hours that must be scheduled
    def _createRequired(self):
        decimals = []  # list of values used to determine athlete place in queue; initialized as empty
        # creates a list of 1000 numbers to be chosen randomly from
        for i in range(1000):
            decimals.append(i)
        rangee = 999  # upper bound to random list index range; decremented with each athlete on queue
        reqQ = PriorityQueue()  # priority queue to order athlete objects
        # for each athlete in athleteList, give priority value based on hours needed and random decimal value
        for ath in self.athleteList:
            # add only required athlete hours to required priority queue
            if ath.required:
                x = (random.randint(0, rangee))  # randomly chosen list index
                ath.hours += decimals[x] / 1000
                decimals.remove(decimals[x])
                rangee -= 1
                reqQ.put((1 / ath.hours, ath, ath.hours))
        return reqQ

    # Creates priority queue of athlete hours that might be scheduled
    def _createOptional(self):
        # Create priority queue
        decimals = []  # list of values used to determine athlete place in queue; initialized as empty
        # creates a list of 1000 numbers to be chosen randomly from
        for i in range(1000):
            decimals.append(i)
        rangee = 999  # upper bound to random list index range; decremented with each athlete on queue
        optQ = PriorityQueue()  # priority queue to order athlete objects
        # for each athlete in athleteList, give priority value based on hours needed and random decimal value
        for ath in self.athleteList:
            # add only non-required athlete hours to optional priority queue
            if not ath.required:
                x = (random.randint(0, rangee))  # randomly chosen list index
                ath.hours += decimals[x] / 1000
                decimals.remove(decimals[x])
                rangee -= 1
                optQ.put((1 / ath.hours, ath, ath.hours))
        return optQ
