import sched
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from os.path import exists
from tkinter import simpledialog

class ManagerInterface:
    def __init__(self, scheduleExists, signalSchedule):
        self.scheduleExists = scheduleExists
        self.signalSchedule = signalSchedule
        self._createDisplay()

    def _createDisplay(self):
        #Initialize tkinter window and set its properties
        self.root = Tk()
        self.root.geometry("1260x640")
        self.root.minsize(1260,640)
        self.root.maxsize(1260,640)

        '''Menu Setup'''
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
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

            canvas = Canvas(self.root, width = 500, height = 400)
            canvas.pack()
            target = Entry(self.root)
            targetName = target.get()

            canvas.create_window(250, 200, window=target)           # change from entry box to scroll dropdown list OR have auto-complete name from dynamic drop menu on familiar names

            findName = Button(text="Generate", command=None)           # tie command to necessary funct in builder/appointment?
            canvas.create_window(250, 240, window=findName)

        else:
            print("no")

            noLabel = Label(self.root, text = "No schedule found: To create a schedule, please navigate to\n File -> Import Files ", bg = None, fg = "black", font = ("Arial", 30))  # make font size dynamic relative to window size
            noLabel.place(x = 70, y = 90)
            # noLabel.pack()

        print("updated")
        self.root.mainloop()

    def _startScheduling(self, filePath1, filePath2):
        #Will be called when the file input is done
        self.scheduleExists = self.signalSchedule(filePath1, filePath2)
        self._updateDisplay()

    def importAction(self):
        '''Obtain a user-selected file for import'''
        if messagebox.askokcancel("Import", "Please select the necessary files in the following order:\n 1) Athlete List\n 2) Tutor List"):

            file1 = filedialog.askopenfilename()
            # filename = os.path.basename(file1)
            # print(file1)
            file2 = filedialog.askopenfilename()
            self._startScheduling(file1, file2)
