"""athleteList = [
{"id": 123,
"name": "thomas",
"lastname": "schombert",
"availability": [[10,11], [13,15], [10,11], [13,15], [16,17,18]],
"subjects": ["math", "econ"],
"hours": 8,
"required": True
},

{"id": 124,
"name": "mert",
"lastname": "yapucuoglu",
"availability": [[9,10], [16,17], [9,10], [16,17], [11,12]],
"subjects": ["trolling", "methodology"],
"hours": 2,
"required": True
},

{"id": 125,
"name": "brianna",
"lastname": "vago",
"availability": [[12,13], [7,8], [12,13], [7,8], [5,6]],
"subjects": ["math", "volleyball"],
"hours": 4,
"required": True
},
#
# {"id": ,
# "name": "",
# "lastname": "",
# "availability": [],
# "subjects": [],
# "hours": [],
# "required": True
# },
#
# {"id": ,
# "name": "",
# "lastname": "",
# "availability": [],
# "subjects": [],
# "hours": [],
# "required": True
# },


]

tutorList = [
{"id": 123,
"name": "kelly",
"lastname": "schombert",
"availability": [[10, 12, 13], [13, 16, 8, 17, 7, 15], [10, 11, 13, 12], [13, 16, 8, 17, 15], [16, 12, 6, 18, 11, 5]],
"subjects": ["trolling", "methodology","econ","volleyball"],
"hours": 20,
},
]"""
class FileIO:
    def readFiles(self):
        """This function reads the athlete and tutor csv files and
        writes the proper information for each athlete and tutor into
        their own dictionary. It then returns a list of dictionaries
        for the athletes and for the tutors"""
        # make the file names and initialize the heading and rows list
        file1 = "athlete.csv"
        file2 = "tutor.csv"
        headingsA = []
        athlete_dict = []
        headingsT = []
        tutor_dict = []

        # This section filters through the athlete list file called athlete.csv
        with open(file1, 'r') as athletes_list:
            # This takes the headings of athlete and puts them in a list.
            # Headings must be: "First Name,Last Name,ID,GPA,Year,Hours Wanted,Subjects,Availability" in this order.
            # Uppercase or lowercase doesn't matter
            headingsA = athletes_list.readline()

            # This splits each athlete's info and sets required to false
            for row in athletes_list:
                temp = row.split(",")
                temp[6] = temp[6].split(" ")
                temp[7] = temp[7].strip().split("/")
                req = False

                # Required testing for when to set to true
                if float(temp[3]) <= 2.29 or float(temp[4]) == 1:
                    temp[5] = '8'
                    req = True
                elif 2.30 <= float(temp[3]) <= 2.59:
                    temp[5] = '6'
                    req = True
                elif 2.60 <= float(temp[3]) <= 2.99:
                    temp[5] = '4'
                    req = True

                # This makes the availability list of lists
                extra = []
                day = 0
                week = [[], [], [], [], []]
                for item in temp[7]:
                    if len(item) != 0:
                        extra = item.split(" ")
                        for time in extra:
                            week[day].append(int(time))
                    day = day + 1

                # This makes the athletes dictionary and appends it into a long list of dictionaries
                DictA = {"id": int(temp[2]), "name": temp[0], "lastname": temp[1],
                         "availability": week, "subjects": temp[6], "hours": int(temp[5]), "required": req}
                athlete_dict.append(DictA)

        # This section filters through the tutor list file called tutor.csv
        with open(file2, 'r') as tutor_list:
            # This takes the headings of tutor and puts them in a list.
            # Headings must be: "First Name,Last Name,ID,Hours Wanted,Subjects,Availability" in this order.
            # Uppercase or lowercase doesn't matter
            headingsT = tutor_list.readline()

            # This splits each tutor's info
            for row in tutor_list:
                temp = row.split(",")
                temp[4] = temp[4].split(" ")
                temp[5] = temp[5].strip().split("/")

                # This makes the availability list of lists
                extra = []
                day = 0
                week = [[], [], [], [], []]
                for item in temp[5]:
                    if len(item) != 0:
                        extra = item.split(" ")
                        for time in extra:
                            week[day].append(int(time))
                    day = day + 1

                # This makes the tutors dictionary and appends it into a long list of dictionaries
                DictB = {"id": int(temp[2]), "name": temp[0], "lastname": temp[1], "availability": week,
                         "subjects": temp[4], "hours": int(temp[3])}
                tutor_dict.append(DictB)
        return tutor_dict, athlete_dict

    def writeCSV(schedules):
        #add_cascade
        a=2
