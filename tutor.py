class Tutor:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.lastname = data["lastname"]
        self.availability = data["availability"]
        self.subjects = data["subjects"]
        self.hours = data["hours"]

    def __str__(self):
        return self.name

    def isAvailable(self, time, subject):
        #Return boolean if the tutor is avaiable at time and teaches the subject
