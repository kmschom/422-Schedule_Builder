"""
Name: appointment.py
Purpose: ???

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: ???

appointment.py is part of the All In a Week's Work (AWW) Schedule Building software which takes input on athlete and tutor
availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    ???

Modifications:
Created file                    my 2/12/22
???
Code documentation              ks 3/1/22
"""

class Appointment:
    def __init__(self, time, tutor, athletes, subject, classroom):
        self.classroom = classroom
        self.time = time[0]
        self.day = time[1]
        self.tutor = tutor
        self.athletes = athletes
        self.subject = subject

    def __repr__(self):
        athletes = ""
        for ath in self.athletes:
            athletes += f"{str(ath)}"
            athletes += "/"
        athletes = athletes[:-1]
        summary = athletes + ' ' + self.subject + " with:" + str(self.tutor) + " " + str(self.classroom)
        return summary

    def __str__(self):
        athletes = ""
        for ath in self.athletes:
            athletes += f"{str(ath)}"
            athletes += "/"
        athletes = athletes[:-1]
        summary = athletes + " " + str(self.time) + ' ' + str(self.day) + ' ' + self.subject + " " + str(self.tutor) + " " + str(self.classroom)
        return summary
