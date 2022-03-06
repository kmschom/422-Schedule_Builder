"""
Name: athlete.py
Purpose: Holds athletes attributes and differentiate hours per subject. 

Creation Date: Feb. 12, 2022
Last Updated: Mar. 1, 2022
Authors: Kelly Schombert(ks) and Mert Yapucuoğlu(my)

athlete.py is part of the All In a Week's Work (AWW) Schedule Building software which takes input on athlete and tutor
availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    ???

Modifications:
Created file                    my 2/12/22
Commented code                  km 3/6/22
Code documentation              ks 3/1/22
"""

import random

class Athlete:
    def __init__(self, data):
        self.id = data["id"] #used to get the id number of each student in the data list
        self.name = data["name"] #gets the firstname of each student in the data list
        self.lastname = data["lastname"] #gets the last name of each student in the data list
        self.availability = self.shuffleTimes(data["availability"]) # shuffles the availability in the data list
        self.subjects = data["subjects"] #get the subjects from the data list
        random.shuffle(self.subjects) # randomly shuffles the subjects
        self.hours = data["hours"] #gets the hour from the data list
        self.required = data["required"] #gets the required hours from the data list
        self.hoursLeft = self.createHours() #calls the createHours function to hours left
    #returns the first and last name
    def __str__(self):
        return f"{self.name},{self.lastname}"

    #returns the first and last name
    def __repr__(self):
        return f"{self.name},{self.lastname}"

    #randomly shuffles through the days
    def shuffleTimes(self, availability):
        # Loops through the days in availabilty
        for day in availability:
            random.shuffle(day)
        #returns the availability
        return availability

    def createHours(self):
        subjectHours = [] #creates a list names subjectHours
        hoursLeft = self.hours #gets the hours from init

        #assigns 2 hours to each subject until there are less than 2 hours left
        for sub in self.subjects:
            #if hours left is less than or equal to, doesn't do anything
            if hoursLeft <= 0:
                break
            else: 
                if hoursLeft % 2==0:
                    subjectHours.append((sub,2))
                    hoursLeft-=2
                else:
                    #assigns remaining to the current subject
                    subjectHours.append((sub,1))
                    hoursLeft -= 1

        while hoursLeft:
            #if there are no subject left, doesn't do anything
            if len(self.subjects) == 0:
                break
            #Looks at remaining hours and add those to existing subject distributions
            for index,sub in enumerate(subjectHours):
                subjectHours[index] = (sub[0], sub[1]+1)
            hoursLeft-=1

        #returns the subjectHours
        return subjectHours
