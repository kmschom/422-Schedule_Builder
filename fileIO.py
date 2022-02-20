athleteList = [
{"id": 123,
"name": "kelly",
"lastname": "schombert",
"availability": [[10,11], [13,15], [10,11], [13,15], [16,17,18]],
"subjects": ["math", "econ"],
"hours": [8],
"required": True
},

{"id": 124,
"name": "mert",
"lastname": "yapucuoglu",
"availability": [[9,10], [16,17], [9,10], [16,17], [11,12]],
"subjects": ["trolling", "methodology"],
"hours": [2],
"required": False
},

{"id": 125,
"name": "brianna",
"lastname": "vago",
"availability": [[12,13], [7,8], [12,13], [7,8], [5,6]],
"subjects": ["math", "volleyball"],
"hours": [4],
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
"availability": [[10], [13], [10], [13], [16]],
"subjects": ["trolling", "methodology","econ","volleyball"],
"hours": [20],
},
]
class FileIO:
    def readFiles(self):
        # return [tutorInfo: List, athleteInfo: List]
        return (tutorList,athleteList)

    # tutorInfo = [personInfo1: List, personInfo2: List]
    # athleteInfo = [{name: here, classes: here, hours: here, grade: here, etc.: here}, athleteInfo2: List]

    def writeCSV(schedules):
        #add_cascade
        a=2
