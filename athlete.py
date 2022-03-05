"""
Name: athlete.py
Purpose: ???

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: ???

athlete.py is part of the All In a Week's Work (AWW) Schedule Building software which takes input on athlete and tutor
availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    ???

Modifications:
Created file                    my 2/12/22
???
Code documentation              ks 3/1/22
"""

import random

class Athlete:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.lastname = data["lastname"]
        self.availability = self.shuffleTimes(data["availability"])
        self.subjects = data["subjects"]
        random.shuffle(self.subjects)
        self.hours = data["hours"]
        self.required = data["required"]
        self.hoursLeft = self.createHours()

    def __str__(self):
        return f"{self.name},{self.lastname}"

    def __repr__(self):
        return f"{self.name},{self.lastname}"

    def shuffleTimes(self, availability):
        for day in availability:
            random.shuffle(day)
        return availability

    def createHours(self):
        subjectHours = []
        hoursLeft = self.hours
        for sub in self.subjects:
            if hoursLeft <= 0:
                break
            else:
                if hoursLeft % 2==0:
                    subjectHours.append((sub,2))
                    hoursLeft-=2
                else:
                    subjectHours.append((sub,1))
                    hoursLeft -= 1
        while hoursLeft:
            if len(self.subjects) == 0:
                break
            for index,sub in enumerate(subjectHours):
                subjectHours[index] = (sub[0], sub[1]+1)
            hoursLeft-=1

        return subjectHours
