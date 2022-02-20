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
        return self.name

    def shuffleTimes(self, availability):
        for day in availability:
            random.shuffle(day)
        return availability

    #def isAvailable(self, time, subject):
        #Return boolean if the tutor is avaiable at time and teaches the subject
