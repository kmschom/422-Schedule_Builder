import sched
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from os.path import exists

class ManagerInterface:
    def __init__(self, scheduleExists, signalSchedule):
        self.scheduleExists = scheduleExists
        self.signalSchedule = signalSchedule
        self._createDisplay()

    def _createDisplay(self):
        #Initialize tkinter window and set its properties
        print("mret gay")
        self.root = Tk()
        self.root.geometry("1260x640")

        '''Menu Setup'''
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        #Creating a menu drop down for user input
        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_command(
            label='Import Lists',
            command=lambda:self.importAction(),
        )
        # file_menu.add_separator()
        # file_menu.add_command(
        #     label='Exit',
        #     # command=root.destroy,
        #     command=lambda:on_closing(),
        # )   
        menubar.add_cascade(
            label="File",
            menu=file_menu,
            underline=0
        )
        self._updateDisplay()
    

    def _updateDisplay(self):
        #Will be called by inside code to delete everything and re-add them to
        #tkinter window

        if self.scheduleExists:
            print("yes")

            yesLabel = Label(self.root, text = "Yes", bg = "Green", fg = "white", padx = 30, relief  = RAISED, width =10, font = ("Arial", 12))
            yesLabel.pack()
            # yesLabel.grid(row = 1, column = 1, padx = 5, pady = 5)

        else:
            print("no")

        print("updated")
        self.root.mainloop()

    def _startScheduling(self, filePath1, filePath2):
        #Will be called when the file input is done
        self.signalSchedule(filePath1, filePath2)

    def importAction(self):
        '''Obtain a user-selected file for import'''
        if messagebox.askokcancel("Import", "Please select the necessary files in the following order:\n 1) Athlete List\n 2) Tutor List"):

            file1 = filedialog.askopenfilename()
            # filename = os.path.basename(file1)
            # print(file1)
            file2 = filedialog.askopenfilename()
            self._startScheduling(file1, file2)
