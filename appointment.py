class Appointment:
    def __init__(self, time, tutor, athlete, subject, classroom):
        self.classroom = classroom
        self.time = time[0]
        self.day = time[1]
        self.tutor = tutor
        self.athletes = [athlete]
        self.subject = subject

    def __repr__(self):
        summary = str(self.time) + ' ' + str(self.day) + ' ' + str(self.athletes) + ' ' + self.subject
        return summary

    def hasOpening(self):
        #Return true if the athletes array has less than 3 athletes
        return 0

    def fitsRequirements(self, time, subject):
        #Return true if the appointment is at the same time with the same subject.
        return 0
