"""
Name: managerInterface.py
Purpose: Create a user-friendly interface to facilitate operation accessibility and navigation for the product user.

Creation Date: Feb. 12, 2022
Last Updated: Mar. 4, 2022
Authors: David Han (dh), Mert Yapucuoğlu (my)

managerInterface.py is part of the JTAS (JAQUA Tutor Appointment Scheduler) Schedule Building software which takes input on athlete and tutor
availability and builds a schedule of tutoring appointments for the entire group.
Called by:
    ScheduleSystem.py - initializes the managerInterface GUI through call

Modifications:
Created file                                                 my 2/12/22
Rough Window, Menu Creation                                  dh 2/13/22
Implemented File Import Compatability                        dh 2/18/22
Created Display Creation + Update                            dh 2/21/22
Finalized Widget Functionality                               dh 2/25/22
Created functioning communication with ScheduleSystem.py     dh 2/28/22
Final Draft of Code                                          dh 3/1/22
Code Documentation                                           dh 3/4/22
"""

from tkinter import *                                       # used to generate the graphic interface of the software
from tkinter import filedialog                              # enables file directory selection for importing
from tkinter import messagebox                              # generates pop-up message prompts to alert the user of important notices and/or information

'''The ManagerInterface class'''
class ManagerInterface:

    '''The __init__() method initializes the attributes of ManagerInterface'''
    def __init__(self, scheduleExists, signalSchedule, exportIndividual):

        """Initialize ManagerInferface attributes"""
        self.scheduleExists = scheduleExists            # bool; used to verify the existence of a fully generated schedule of all athlete and tutor appointments, or the full schedule, in the program files
        self.signalSchedule = signalSchedule            # function with two arguments; a ScheduleSystem.py function declared in managerInterface to initiate the scheduling creation process from the UI
        self.mainFrame = None                           # Nonetype; declaration for the main Frame widget used to organize the subwidgets that display information on the program window
        self.exportIndividual = exportIndividual        # function with one argument; a ScheduleStstem.py function declared in managerInterface to intiate the individual schedule file export process from the UI

        '''Determine displayed status message based on if an existing full schedule exists in the program files'''
        if self.scheduleExists:                         # a full schedule exists; print default status message for the individual schedule creation Frame
            self.statusMessage = "Awaiting Action"
        else:                                           # a full schedule does not exist; print the default status message for the full schedule creation Frame
            self.statusMessage = "No schedule found: To create a schedule,\n please begin by importing the required files"
        
        self._createDisplay()                           # initiate display creation method

    '''The _createDisplay() method initializes the tkinter-based user interface window and sets its main properties'''
    def _createDisplay(self):

        """Window Setup"""
        self.root = Tk()                                # create tkinter window
        self.root.title("AWW Schedule Builder")         # set the window title
        self.root.geometry("1260x640")                  # set the size of the window
        self.root.minsize(1260,640)                     # set the fixed minimum adjustable size of the window
        self.root.maxsize(1260,640)                     # set the fixed maximum adjustable size of the window
        self.root.grid_propagate(False)                 # disables widget grid propagation in order to enable forced widget sizes

        '''Menu Setup'''
        menubar = Menu(self.root)                       # intialize a toolbar menu option in the window
        self.root.config(menu=menubar)                  # bind Menu menubar to the window
        fileMenu = Menu(menubar, tearoff=False)         # initialize a File option to the window menubar

        '''Menu: Import File'''
        fileMenu.add_command(
            label='Import Files',
            command=lambda:self.importAction(),
        ) # initialize an file import option for creating a new full schedule through the menubar

        '''Menu: Exit'''
        fileMenu.add_separator()                         # add a line separating all preceding File menu options from the Exit option
        fileMenu.add_command(
            label='Exit',
            command=lambda:self.root.destroy()
        ) # initialize an exit program option used to shut down the JTAS program and window

        '''Menu: Cascade Functionality'''
        menubar.add_cascade(
            label="File",
            menu=fileMenu,
            underline=0
        ) # adds a feature where the File menu option will hide its featured menu options by default and display its options in a dropdown menu manner when selected

        # Update the display
        self._updateDisplay()

    '''The _updateDisplay method updates the JTAS GUI window with new and/or updated information on execution'''
    def _updateDisplay(self):

        if self.scheduleExists:                 # Clause: Full schedule exists
            
            '''scheduleExists Frame Initialization'''
            self.mainFrame = Frame(self.root, width=1260, height=640, bg="green")       # set Frame dimensions and color
            self.mainFrame.grid(row=0, column=0)                                        # set Frame grid orientation
            self.mainFrame["borderwidth"] = 5                                           # set Frame border width
            self.mainFrame.pack()                                                       # pack Frame position relative to window

            '''Image Initialization'''
            imageFrame = Canvas(self.mainFrame, width=1260, height=100, bg="dark green", bd=0, relief="ridge")  # set Canvas dimensions and color to place image in
            imageFrame.place(relx=0.5, rely=0, anchor="center")                                                 # set Canvas position in window
            img = PhotoImage(file="UO_logo.png")                                                                # set the image to an img variable
            imageFrame.create_image(100, 75, image=img)                                                         # initialize the image in the Canvas

            '''Label Initialization'''
            yesLabel = Label(self.mainFrame, text = "Schedule Found/Made: Please Enter a Name Below", bg="green", fg="white", font=("Helvetica 30 bold"))   # initialize scheduleExists main message to prompt a name input
            yesLabel["highlightbackground"] = "yellow"                                                                                                      # set label border color
            yesLabel["highlightthickness"] = 1                                                                                                              # set label border width
            yesLabel["relief"] = "groove"                                                                                                                   # set label style
            yesLabel.place(relx=.5, rely=.3, anchor="center")                                                                                               # set label position

            '''Entry Box Initialization'''
            canvas = Canvas(self.mainFrame, width=300, height=30)                                               # set Canvas dimensions and color to place entry box in               
            canvas.place(relx=.45, rely=.55, anchor="center")                                                   # set Canvas position in window
            self.nameInputBox = Entry(self.mainFrame, font=("Helvetica", 15))                                   # intialize entry box to receive a name as a user str inputs
            canvas.create_window(150, 15, width=300, height=30, anchor="center" , window=self.nameInputBox)     # initalize entry box in the Canvas

            '''Button Initialization'''
            yesButton = Button(text="Generate", font=("Helvetica", 13) ,command=self.generateIndividual)        # create Button used to intialize an individual athlete/tutor schedule based on the name inputed in the entry box
            yesButton.place(relx=.62, rely=.55, anchor="center")                                                # set Button position in window

            '''Status Initialization'''
            status = Label(self.mainFrame, text=self.statusMessage, bg="green", fg="white", font=("Helvetica 15 bold"))    # create status message Label display to inform user of the current status of the JTAS program's operations
            status.place(relx=.48, rely=.8, anchor="center")                                                               # set status message Label position

        else:                 # Clause: Full schedule does not exist

            '''Not scheduleExists Frame initialization'''
            self.mainFrame = Frame(self.root, width=1260, height=640, bg="green")       # set Frame dimensions and color
            self.mainFrame.grid(row=0, column=0)                                        # set Frame grid orientation
            self.mainFrame["borderwidth"] = 5                                           # set Frame border width
            self.mainFrame.pack()                                                       # set Frame position relative to window

            #Image
            imageFrame = Canvas(self.mainFrame, width=1260, height=100, bg="dark green", bd=0, relief="ridge")  # set Canvas dimensions and color to place image in
            imageFrame.place(relx=0.5, rely=0, anchor="center")                                                 # set Canvas position in window
            img = PhotoImage(file="UO_logo.png")                                                                # set the image to an img variable
            imageFrame.create_image(100, 75, image=img)                                                         # initialize the image in the Canvas

            #Label
            noLabel = Label(self.mainFrame, text = self.statusMessage, bg="green", fg="white", font=("Helvetica 30 bold"))  # initialize Not scheduleExists main message to prompt a name input
            noLabel["highlightbackground"] = "yellow"                                                                       # set label border color  
            noLabel["highlightthickness"] = 3                                                                               # set label border width
            noLabel["relief"] = "groove"                                                                                    # set label style
            noLabel.place(relx=.5, rely=.4, anchor="center")                                                                # set label position

            #Button
            noButton = Button(text="Import Files", font=("Helvetica", 20) ,command=lambda:self.importAction())  # create Button used to intialize the file selection process to begin full schedule creation
            noButton["highlightbackground"] = "yellow"                                                          # set Button border color
            noButton["highlightthickness"] = 5                                                                  # set Button border thickness
            noButton["relief"] = "groove"                                                                       # set Button style
            noButton.place(relx=.5, rely=.6, anchor="center")                                                   # set Button position

        self.root.mainloop()                                                                                    # establish mainloop of window

    '''The _startScheduling() method initializes the creation of the full schedule through communicating with the ScheduleSystem.py component'''
    def _startScheduling(self, filePath1, filePath2):

        (self.scheduleExists, self.statusMessage) = self.signalSchedule(filePath1, filePath2)   # set the values of the scheduleExists and statusMessage class attributes based on the return values of the signalSchedule() function in ScheduleSystem.py
        self.frameDestroy()                                                                     # destroy main Frame to be updated through recreation
        self._updateDisplay()                                                                   # update display

    '''The importAction() method obtains a user-selected file for import'''
    def importAction(self):
        
        '''
        Prompt a pop-up message with instructions for the required import files to create a 
        full schedule and the order in which the files need to be selected.
        '''
        if messagebox.askokcancel("Import", "Please select the necessary files in the following order:\n 1) Athlete List\n 2) Tutor List"): # Clause: The user selects the yes option in the message box
            file1 = filedialog.askopenfilename()            # opens the user's computer file explorer to prompt the selection of the first import file (A .csv file with the neessary Athlete information)
            if file1:                                       # Clause: a file was selected
                file2 = filedialog.askopenfilename()        # opens the user's computer file explorer to prompt the selection of the second import file (A .csv file with the neessary Tutor information)
                if file2:                                   # Clause: a file was selected
                    self._startScheduling(file1, file2)     # initialize the full schedule creation function in ScheduleSystem.py

    '''The generateIndividual() method intiializes the creation of an individual athlete schedule or tutor schedule relative to a user-inputted name through communication with the ScheduleSystem.py component'''
    def generateIndividual(self):

        requestedName = self.nameInputBox.get()                         # obtain the user-inputted name in the windows's entry box
        self.statusMessage = self.exportIndividual(requestedName)       # update the status message based on the return str value of the exportIndividual() function in ScheduleSystem.py
        self.frameDestroy()                                             # destroy main Frame to be updated through recreation
        self._updateDisplay()                                           # update display

    '''The frameDestroy() method destroy's the JTAS window's current Frame and properties in preparation for the display update'''
    def frameDestroy(self):
        self.mainFrame.destroy()                                        # destroy the current Frame and all its subwidget properties
