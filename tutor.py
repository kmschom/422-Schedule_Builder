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

import random #used to shuffles the day 

class Tutor:
    def __init__(self, data):
        self.id = data["id"] #used to get the id number of each student in the data list
        self.name = data["name"] #gets the firstname of each student in the data list
        self.lastname = data["lastname"] #gets the last name of each student in the data list 
        self.availability = self.shuffleTimes(data["availability"]) # shuffles the availability in the data list
        self.subjects = data["subjects"] #get the subjects from the data list
        random.shuffle(self.subjects) # randomly shuffles the subjects
        self.hours = data["hours"] #gets the hour from the data list

    #returns the first and last name
    def __str__(self):
        return f"{self.name},{self.lastname}"

    #randomly shuffles through the days
    def shuffleTimes(self, availability):
        # Loops through the days in availabilty
        for day in availability:
            random.shuffle(day)
        #returns the availability
        return availability
