class Appointment:
    def __init__(self, time, tutor, athlete, subject, classroom):
        self.classroom = classroom
        self.time = time[0]
        self.day = time[1]
        self.tutor = tutor
        self.athletes = [athlete]
        self.subject = subject

    def __repr__(self):
        summary = str(self.time) + ' ' + str(self.day) + ' ' + str(self.athletes) + ' ' + self.subject + " " + str(self.tutor)
        return summary
