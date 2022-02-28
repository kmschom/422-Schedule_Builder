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
        return self.name

    def __repr__(self):
        return self.name

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
            for index,sub in enumerate(subjectHours):
                subjectHours[index] = (sub[0], sub[1]+1)
            hoursLeft-=1

        return subjectHours
