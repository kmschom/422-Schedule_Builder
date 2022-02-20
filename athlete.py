import random

class Athlete:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.lastname = data["lastname"]
        self.availability = random.shuffle(data["availability"])
        self.subjects = data["subjects"]
        self.hours = data["hours"]
        self.required = data["required"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def nextAvailability(self, currentTime):
        #Find the next available time given the last checked available time "currentTime"
        return 0
