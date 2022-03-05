from calendar import c
from platform import architecture, release
import sched
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from os.path import exists
from tkinter import simpledialog
from xml.dom.expatbuilder import FragmentBuilder
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap

class ManagerInterface:
    def __init__(self, scheduleExists, signalSchedule, mainFrame, exportIndividual):
        """Init type shit idk"""
        self.scheduleExists = scheduleExists
        self.signalSchedule = signalSchedule
        self.mainFrame = None
        self.exportIndividual = exportIndividual
        self.statusMessage = "No schedule found: To create a schedule, please navigate to\n File -> Import Files"
        self._createDisplay()

    def _createDisplay(self):
        #Initialize tkinter window and set its properties

        """Window Setup"""
        self.root = Tk()
        self.root.title("Insret cool scheduler name here")
        self.root.geometry("1260x640")
        self.root.minsize(1260,640)
        self.root.maxsize(1260,640)
        # self.root.configure(bg="green")                                   # Frames take up whole root display, so bg defined there
        self.root.grid_propagate(False)                                     # Not entirely sure what this does; saw it on a lot of examples

        '''File Menu Setup'''
        menubar = Menu(self.root)
                # menubar = Menu(self.root, font=("Helvetica", 20))         # font doesnt change anything
        self.root.config(menu=menubar)
        fileMenu = Menu(menubar, tearoff=False)
        #Import File
        fileMenu.add_command(
            label='Import Files',
            command=lambda:self.importAction(),
        )

        #User Documentation

        #Programmer Documentation

        #Separator/Exit
        fileMenu.add_separator()
        fileMenu.add_command(
            label='Exit',
            # command=root.destroy,
            # command=lambda:on_closing(),
            command=lambda:self.root.destroy()
        )

        #Cascade Functionality
        menubar.add_cascade(
            label="File",
            menu=fileMenu,
            underline=0
        )

        #Update
        self._updateDisplay()


    def _updateDisplay(self):
        #Will be called by inside code to delete everything and re-add them to
        #tkinter window

        if self.scheduleExists:
            """Schedule Found"""
            #Frame
            self.mainFrame = Frame(self.root, width=1260, height=640, bg="green")
            self.mainFrame.grid(row=0, column=0)
            self.mainFrame["borderwidth"] = 5
            self.mainFrame.pack()

            #Image (Optional)

            #Label
            yesLabel = Label(self.mainFrame, text = "Schedule Found: Please Enter a Name Below", bg="white", fg="black", font=("Helvetica", 30))
            yesLabel["highlightbackground"] = "yellow"
            yesLabel["highlightthickness"] = 3
            yesLabel["relief"] = "groove"
            yesLabel.place(relx=.5, rely=.4, anchor="center")

            #timeLabel

            #Canvas
            canvas = Canvas(self.mainFrame, width=300, height=30)
            canvas.place(relx=.45, rely=.6, anchor="center")

            #Entry
            self.nameInputBox = Entry(self.mainFrame, font=("Helvetica", 15))
            canvas.create_window(150, 15, width=300, height=30, anchor="center" , window=self.nameInputBox)        #Entry window is slightly smaller than canvas

            #Button
            yesButton = Button(text="Generate", font=("Helvetica", 13) ,command=self.generateIndividual)                   # change None to proper command
            yesButton.place(relx=.62, rely=.6, anchor="center")

        else:
            """No Schedule Found"""                                                                     #Possibly instead of everything contained in 1 big frame, could instead have a unique frame for each widget
            #Frame
            self.mainFrame = Frame(self.root, width=1260, height=640, bg="green")                       #or just replace noFrame call w self.root
            self.mainFrame.grid(row=0, column=0)
            self.mainFrame["borderwidth"] = 5
            self.mainFrame.pack()

            # #Image
            # imageFrame = Frame(noFrame, width=200, height=200)
            # img = PhotoImage(file="images/UO_logo.jpg")
            # noImage = Label(imageFrame, image=img)
            # noImage.place(relx=.5, rely=.2, anchor="center")

            #Label
            noLabel = Label(self.mainFrame, text = self.statusMessage, bg="white", fg="black", font=("Helvetica", 30))
            noLabel["highlightbackground"] = "yellow"
            noLabel["highlightthickness"] = 5
            noLabel["relief"] = "groove"
            noLabel.place(relx=.5, rely=.4, anchor="center")

            #Button
            noButton = Button(text="Import Files", font=("Helvetica", 20) ,command=lambda:self.importAction())
            noButton["highlightbackground"] = "yellow"      # not adding border atm?
            noButton["highlightthickness"] = 5
            noButton["relief"] = "groove"
            noButton.place(relx=.5, rely=.6, anchor="center")

            #Status

        print("updated")
        self.root.mainloop()

    def _startScheduling(self, filePath1, filePath2):
        #Will be called when the file input is done
        (self.scheduleExists, self.statusMessage) = self.signalSchedule(filePath1, filePath2)
        self.frameDestroy()
        self._updateDisplay()
        #Success Message box

    def importAction(self):
        '''Obtain a user-selected file for import'''
        if messagebox.askokcancel("Import", "Please select the necessary files in the following order:\n 1) Athlete List\n 2) Tutor List"):
            file1 = filedialog.askopenfilename()
            if file1:
                file2 = filedialog.askopenfilename()
                if file2:
                    self._startScheduling(file1, file2)

    def generateIndividual(self):
        requestedName = self.nameInputBox.get()
        self.statusMessage = self.exportIndividual(requestedName)


    def frameDestroy(self):
        self.mainFrame.destroy()
