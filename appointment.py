"""
Name: appointment.py
Purpose: Contains information about each tutoring appointment that is made by the scheduling algorithm.

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: Mert Yapucuoğlu (my), Kelly Schombert (ks)

appointment.py is part of the JTAS(JAQUA Tutor Appointment Scheduler) Schedule Building software which takes input on
athlete and tutor availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    scheduler.py - imports Appointment class to create appointment objects
    ScheduleSystem.py - imports Appointment class to create appointment objects

Modifications:
Created file                                        my 2/12/22
Wrote Skeleton code                                 my 2/16/22
Added _repr_ functionality                          ks 2/20/22
Removed hasOpening and fitsRequirements functions   ks 2/23/22
Code documentation                                  ks 3/1/22
Added _str_ functionality                           my 3/4/22
"""

# Appointment class; holds appointment attributes
class Appointment:
    def __init__(self, time, tutor, athletes, subject, classroom):
        self.classroom = classroom  # appointment classroom
        self.time = time[0] # appointment time
        self.day = time[1]  # appointment day
        self.tutor = tutor  # tutor assigned to an appointment
        self.athletes = athletes    # athletes assigned to an appointment
        self.subject = subject  # subject assigned to an appointment

    # formats presentation of appointment data
    def __repr__(self):
        athletes = ""
        for ath in self.athletes:
            athletes += f"{str(ath)}"
            athletes += "/"
        athletes = athletes[:-1]
        summary = athletes + ' ' + self.subject + " with:" + str(self.tutor) + " " + str(self.classroom)
        return summary

    # prints appointment data
    def __str__(self):
        athletes = ""
        for ath in self.athletes:
            athletes += f"{str(ath)}"
            athletes += "/"
        athletes = athletes[:-1]
        summary = athletes + " " + str(self.time) + ' ' + str(self.day) + ' ' + self.subject + " " + str(self.tutor) + " " + str(self.classroom)
        return summary
