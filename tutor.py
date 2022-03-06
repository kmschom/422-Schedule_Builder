"""
Name: tutor.py
Purpose: Holds tutor attributes.

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: Kelly Schombert(ks) and Mert Yapucuoğlu(my)

tutor.py is part of JTAS(JAQUA Tutor Appointment Scheduler) Schedule Building software which takes input on athlete and tutor
availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    ScheduleSystem.py

Modifications:
Created file                    my 2/12/22
Commented code                  km 3/5/22
Code documentation              ks 3/1/22
"""

import random

class Tutor:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.lastname = data["lastname"]
        self.availability = self.shuffleTimes(data["availability"])
        self.subjects = data["subjects"]
        random.shuffle(self.subjects)
        self.hours = data["hours"]

    def __str__(self):
        return f"{self.name},{self.lastname}"

    def shuffleTimes(self, availability):
        for day in availability:
            random.shuffle(day)
        return availability
