import tkinter as tk
from tkinter import Menu
import tkinter.scrolledtext as st
from tkinter.filedialog import askopenfilename, asksaveasfilename
import serial
from serial.tools import list_ports
# importing the choosecolor package
from tkinter import colorchooser
from tkinter import ttk
import keyboard
import time
import threading
from typing import List
import pyautogui
import json
from functools import partial
import MacroToHid
import KeyboardLayout
import copy



class Controls(tk.Frame):
    BUTTON_WIDTH = 15

    def __init__(self, parent):
        super().__init__(parent)

        self.dataInitialize()
        self.jsonData = json.dumps(self.data,indent=4)
        self.selectedPort = None
        self.parent = parent
        self.create_btns_frame()
        self.create_new_macro_frame()
        self.parent.title("2800 Team Project")
        self.ListPortsInitially()
        self.filename = ""  # initialize filename
        self.protocol = "0000000000"

    def dataInitialize(self):
        self.data = {}
        self.data["initial delay"] = "0500"
        self.data["repeat delay"] = "0100"
        self.data["brightness"] = "00"
        for num in range(1,11):
            self.data[f"macro {num}"] = {"macro name": f"macro {num}",
                                         "macro": [""],
                                         "colour": [0,0,0]}

    def create_btns_frame(self):
        # Define button font
        button_font = ("Berlin Sans FB Demi", 25)
        other_button_font = ("Berlin Sans FB Demi", 15)
        enter_btn_font = ("Berlin Sans FB Demi", 17)
        auto_font = ("Berlin Sans FB Demi", 15)
        button_fg_color = "white"
        bg_colour = "light blue"
        repeatBtnWidth = 20
        repeatEntryWidth = 5

        # Frame all the components on the left of the main
        # screen will be situated in
        self.btnsFrame = tk.Frame(self.parent)

        # Repeat delay and Repeat rate frame
        self.repeatFrame = tk.Frame(self.btnsFrame, highlightbackground="black", highlightthickness=1,
                                    bg=bg_colour)
        self.repeatFrame.pack(fill=tk.X, ipady=90)

        #
        self.repeatFrame1 = tk.Frame(self.repeatFrame,
                                     bg=bg_colour)
        self.repeatFrame1.pack(expand=True, fill=tk.BOTH, anchor=tk.S)

        self.repeatFrame2 = tk.Frame(self.repeatFrame,
                                     bg=bg_colour)
        self.repeatFrame2.pack(expand=True, fill=tk.BOTH)

        self.initialDelayLabel = tk.Label(self.repeatFrame1, text="Initial Repeat Delay: ",

                                          bg=bg_colour,
                                          font=other_button_font,
                                          fg=button_fg_color)
        self.initialDelayLabel.pack(side=tk.LEFT, expand=True, anchor=tk.SE)
        self.initialDelayLenCheck = self.register(self.delayLenCheck)
        self.initialDelayEntry = tk.Entry(self.repeatFrame1, validate="key",
                                          validatecommand=(self.initialDelayLenCheck, "%P"),
                                          font=other_button_font,
                                          width=repeatEntryWidth)
        self.initialDelayEntry.bind("<Return>", lambda event: self.enterRepeat())
        self.initialDelayEntry.pack(side=tk.LEFT, expand=True, anchor=tk.SW)
        self.initialDelayEntry.insert(0, str(int(self.data["initial delay"])))
        self.repeatRateLabel = tk.Label(self.repeatFrame2, text="Repeat Rate: ",

                                        bg=bg_colour,
                                        font=other_button_font,
                                        fg=button_fg_color)
        self.repeatRateLabel.pack(side=tk.LEFT, expand=True, anchor=tk.E)
        self.repeatRateLenCheck = self.register(self.delayLenCheck)
        self.repeatRateEntry = tk.Entry(self.repeatFrame2, validate="key",
                                        validatecommand=(self.repeatRateLenCheck, "%P"),
                                        font=other_button_font,
                                        width=repeatEntryWidth)
        self.repeatRateEntry.bind("<Return>", lambda event: self.enterRepeat())
        self.repeatRateEntry.pack(side=tk.LEFT, expand=True, anchor=tk.W)
        self.delayErrorLabel = tk.Label(self.repeatFrame, text="",
                                        bg=bg_colour,
                                        font=other_button_font,
                                        fg="#ff0000")
        self.delayErrorLabel.pack(anchor=tk.S)
        self.repeatRateEntry.insert(0, str(int(self.data["repeat delay"])))
        self.repeatEnterBtn = tk.Button(self.repeatFrame, text="Enter",
                                        command=self.enterRepeat,
                                        font=enter_btn_font)
        self.repeatEnterBtn.pack(anchor=tk.S, ipadx=40)

        brightnessFrame = tk.Frame(self.btnsFrame, highlightbackground="black", highlightthickness=1)
        self.brightnessLabel = tk.Label(brightnessFrame, text="Brightness: ",
                                        width=self.BUTTON_WIDTH,
                                        bg=bg_colour,
                                        font=button_font,
                                        fg=button_fg_color)
        self.brightnessLabel.pack(expand=True, anchor=tk.S)
        brightnessFrame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        brightnessFrame.config(bg="light blue")
        self.btnsFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.brightnessValueLabel = tk.Label(brightnessFrame, text=str(int(self.data["brightness"])),
                                             width=self.BUTTON_WIDTH,
                                             bg=bg_colour,
                                             font=button_font,
                                             fg=button_fg_color)
        self.brightnessValueLabel.pack(expand=True, anchor=tk.S)
        # Create a Scale widget
        self.slider = tk.Scale(brightnessFrame, command=self.saveBrightness,
                               from_=0,
                               to=11,
                               orient="horizontal",
                               length=300)
        self.slider.set(int(self.data["brightness"]))
        self.slider.pack(expand=True, side=tk.TOP, anchor=tk.N)

    def enterRepeat(self):
        savedBrightness = self.protocol[:2]
        initialDelay = self.initialDelayEntry.get()
        repeatDelay = self.repeatRateEntry.get()
        if (not initialDelay.isdigit() or not repeatDelay.isdigit()) and initialDelay != "":
            self.delayErrorLabel.config(text="Please enter only number")
        elif initialDelay == "" or int(initialDelay) <= 50 or int(repeatDelay) <= 50:
            self.delayErrorLabel.config(text="The minimum time period is 51(ms)")
        else:
            """initialDelay = f"{int(initialDelay):04}"
            repeatDelay = f"{int(repeatDelay):04}" """
            self.delayErrorLabel.config(text="")
            # Check if the length of the initial repeat delay is less than 4
            if len(initialDelay) < 4:
                # Calculate the number of zeros needed to make the stored value of length 4 for the protocol
                zeros_needed = 4 - len(initialDelay)
                # Add the zeros in front of the number
                initialDelay = "0" * zeros_needed + initialDelay

            if len(repeatDelay) < 4:
                # Calculate the number of zeros needed to make the stored value of length 4 for the protocol
                zeros_needed = 4 - len(repeatDelay)
                # Add the zeros in front of the number
                repeatDelay = "0" * zeros_needed + repeatDelay

            try:
                f = open(self.filename, 'r')
                self.jsonData = json.load(f)
                f.close()
                self.data = self.jsonData
                if "initial delay" in self.data:
                    del self.data["initial delay"]
                self.data["initial delay: "] = initialDelay
                if "repeat delay" in self.data:
                    del self.data["repeat delay"]
                self.data["repeat delay"] = repeatDelay
                self.jsonData = json.dumps(self.data, indent=4)
                CopyD = copy.deepcopy(self.data)
                self.dataInHid = MacroToHid.create_data(CopyD)
                f = open(self.filename, 'w')
                f.write(f"{self.jsonData}")
                f.close()
            except FileNotFoundError:
                if "initial delay" in self.data:
                    del self.data["initial delay"]
                self.data["initial delay"] = initialDelay
                if "repeat delay: " in self.data:
                    del self.data["repeat delay"]
                self.data["repeat delay"] = repeatDelay
                self.jsonData = json.dumps(self.data, indent=4)
                CopyD = copy.deepcopy(self.data)
                self.dataInHid = MacroToHid.create_data(CopyD)
            self.protocol = savedBrightness + initialDelay + repeatDelay
            print(self.protocol)

    def create_new_macro_frame(self):
        BUTTON_WIDTH = 13
        KEY_WIDTH = 5
        TITLE_FONT = ("Berlin Sans FB Demi", 40)
        button_font = ("Berlin Sans FB Demi", 14)
        button_fg_color = "white"
        bg_colour = "light blue"
        keyFont = ("Berlin Sans FB Demi", 20)

        # Frame to hold the DEMO 1 entry/label widgets
        self.entryFrame = tk.Frame(self.parent)

        self.titleLabel = tk.Label(self.entryFrame, text="Macrolyze", font=TITLE_FONT)
        self.titleLabel.pack()

        self.macroLabel = tk.Label(self.entryFrame, text="Macro Name:",
                                   font=button_font)
        self.macroLabel.pack(side=tk.LEFT)

        self.macroEntry = tk.Entry(self.entryFrame,
                                   font=button_font)
        self.macroEntry.pack(side=tk.LEFT)

        self.capMacro = tk.Label(self.entryFrame, text="Capitalised macro",
                                 font=button_font)
        self.capMacro.pack(side=tk.LEFT)

        self.entryFrame.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER, padx=50)

        # Frame to hold the DEMO 1 entry/label widgets
        self.buttonFrame = tk.Frame(self.parent)
        self.readBtn = tk.Button(self.buttonFrame, text="Read", width=BUTTON_WIDTH, command=self.readBtnPress,
                                 bg=bg_colour,
                                 font=button_font,
                                 fg=button_fg_color)
        self.readBtn.pack()
        self.writeBtn = tk.Button(self.buttonFrame, text="Write", width=BUTTON_WIDTH, command=self.writeBtnPress,
                                  bg=bg_colour,
                                  font=button_font,
                                  fg=button_fg_color)
        self.writeBtn.pack()
        self.buttonFrame.pack(fill=tk.BOTH, expand=True, padx=190)

        # Frame to hold port connection and keyboard
        self.keyAndPortFrame = tk.Frame(self.parent)
        self.keyAndPortFrame.pack(fill=tk.BOTH, expand=True)

        ########################################################################

        # Frame to hold keyboard button
        self.keyboardFrame = tk.Frame(self.keyAndPortFrame)
        self.keyboardFrame.pack(side=tk.LEFT, expand=True)

        buttons = []
        self.keys = {}
        count = 0
        for row in range(3):
            button_row = []
            for col in range(4):
                count += 1
                if row == 2 and (col == 2 or col == 3):
                    button = tk.Button(self.keyboardFrame,
                                       font=keyFont,
                                       width=KEY_WIDTH,
                                       height=1,
                                       bg="white")
                    button.grid(row=row, column=col, padx=5, pady=5)
                    button_row.append(button)
                    self.keys[count] = button
                else:
                    button = tk.Button(self.keyboardFrame, text=str(count),
                                       font=keyFont,
                                       command=partial(self.keyPress, count),
                                       width=KEY_WIDTH,
                                       height=1,
                                       bg="white")
                    button.grid(row=row, column=col, padx=5, pady=5)
                    button_row.append(button)
                    self.keys[count] = button
            buttons.append(button_row)

        # Frame to hold port functionality
        self.SerialFrame = tk.Frame(self.keyAndPortFrame)

        self.Portlabel = tk.Label(self.SerialFrame, text="Select a port:",
                                  font=button_font)
        self.Portlabel.pack(anchor=tk.S, expand=True)
        self.portCombobox = ttk.Combobox(self.SerialFrame)
        self.portCombobox.pack(anchor=tk.N, side=tk.TOP, expand=True)
        self.SerialFrame.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER, padx=50)

        self.PortsBtnFrame = tk.Frame(self.keyAndPortFrame)
        self.refreshBtn = tk.Button(self.PortsBtnFrame, text="Refresh", width=BUTTON_WIDTH,
                                    command=self.PortsRefreshing,
                                    bg=bg_colour,
                                    font=button_font,
                                    fg=button_fg_color)
        self.refreshBtn.pack()
        self.connectBtn = tk.Button(self.PortsBtnFrame, text="Connect", width=BUTTON_WIDTH,
                                    command=self.PortsConnecting,
                                    bg=bg_colour,
                                    font=button_font,
                                    fg=button_fg_color)
        self.connectBtn.pack()
        self.PortsBtnFrame.pack(fill=tk.BOTH, expand=True, padx=50)

        menubar = Menu(self.parent)
        root.config(menu=menubar)
        file_menu = Menu(menubar)
        file_menu.add_command(label='Open',
                              command=self.fileRead)
        file_menu.add_command(label='Save As',
                              command=self.fileWrite)
        file_menu.add_command(label='Exit',
                              command=root.destroy)
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

    def keyPress(self, num: any):
        BUTTON_WIDTH = 13
        KEY_WIDTH = 5
        label_font = ("Berlin Sans FB Demi", 20)
        button_font = ("Berlin Sans FB Demi", 30)
        small_button_font = ("Berlin Sans FB Demi", 17)
        button_fg_color = "white"
        bg_colour = "light blue"
        keyFont = ("Berlin Sans FB Demi", 20)

        self.clear_buttons()
        self.backBtnCreate()

        # Previous macro frame
        previousFrame = tk.Frame(self.parent, bg=bg_colour)
        previousFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor=tk.CENTER)

        previousLabel = tk.Label(previousFrame, text="Previous Macro Configuration", font=label_font)
        previousLabel.pack()

        self.macroNameLabel = tk.Label(previousFrame, text="Macro Name: ", font=label_font, wraplength=600)
        self.macroNameLabel.pack()

        macroSequenceLabel = tk.Label(previousFrame, text="Macro Sequence: ", font=label_font)
        macroSequenceLabel.pack()

        self.text_area = st.ScrolledText(previousFrame,
                                         width=40,
                                         height=8,
                                         font=("Times New Roman",
                                               15))

        self.text_area.pack()

        actions = ""
        for i in range(1, 22):
            action = "\taction " + str(i)
            actions += action + "\n"

        # Inserting Text which is read only
        self.text_area.insert(tk.INSERT, actions)
        self.text_area.configure(state='disabled')

        self.RGBColourLabel = tk.Label(previousFrame, text="Colour: ", font=label_font)
        self.RGBColourLabel.pack()

        userFrame = tk.Frame(self.parent)
        userFrame.pack(side=tk.LEFT, expand=True)

        # Frame for entry labels
        macroNameFrame = tk.Frame(userFrame)
        macroNameFrame.pack(side=tk.TOP, anchor=tk.W, expand=True)
        errorFrame = tk.Frame(userFrame)
        errorFrame.pack(side=tk.TOP, anchor=tk.W, expand=True)
        macroFrame = tk.Frame(userFrame)
        macroFrame.pack(side=tk.TOP, anchor=tk.W, expand=True)
        colourFrame = tk.Frame(userFrame)
        colourFrame.pack(side=tk.TOP, anchor=tk.W, expand=True)

        self.MacroNameLabel = tk.Label(macroNameFrame, text="Macro Name: ", font=label_font)
        self.MacroNameLabel.pack(side=tk.LEFT)
        MacroSeqLabel = tk.Label(macroFrame, text="Macro Sequence:            ", font=label_font)
        MacroSeqLabel.pack(side=tk.LEFT,pady=20)
        RGBLabel = tk.Label(colourFrame, text="Colour:                                  ", font=label_font)
        RGBLabel.pack(side=tk.LEFT)

        # initialize macro
        self.macro = []
        # Frame for entry widgets
        self.macroNameLenCheck = self.register(self.NameLenCheck)
        self.macroNameEntry = tk.Entry(macroNameFrame, validate="key", validatecommand=(self.macroNameLenCheck, "%P"),
                                       font=label_font)
        self.macroNameEntry.bind("<Return>", lambda n=num: self.macroCreate(n))
        self.macroNameEntry.pack()
        self.macroNameErrorLabel = tk.Label(errorFrame, text="                              ",
                                            font=small_button_font,
                                            fg="#ff0000")
        self.macroNameErrorLabel.pack(side=tk.TOP)
        macroEditBtnFrame = tk.Frame(macroFrame)
        macroEditBtnFrame.pack(side=tk.TOP, anchor=tk.S, expand=True)
        MacroRecordBtn = tk.Button(macroEditBtnFrame, width=BUTTON_WIDTH,
                                   text="Record macro",
                                   command=lambda n=num: self.keyRecordTread(n),
                                   font=small_button_font,
                                   bg=bg_colour,
                                   fg=button_fg_color)
        MacroRecordBtn.pack()
        StopBtn = tk.Button(macroEditBtnFrame, width=BUTTON_WIDTH,
                            text="Stop recording",
                            command=self.stopRecording,
                            font=small_button_font,
                            bg=bg_colour,
                            fg=button_fg_color)
        StopBtn.pack()

        self.RGBChooseBtn = tk.Button(colourFrame, width=self.BUTTON_WIDTH,
                                      bg="white",
                                      command=lambda: self.ChooseColour(num),
                                      pady=9)
        self.RGBChooseBtn.pack(pady=60)

        ''' initialize data
            if the file has been opened, data will be read from the file
            else data should be a null dictionary 
        '''
        if self.filename != "":
            f = open(self.filename, 'r')
            self.data = json.load(f)
            f.close()
        CopyD = copy.deepcopy(self.data)
        self.dataInHid = MacroToHid.create_data(CopyD)
        print(self.data)
        if f"macro {num}" in self.data:
            # notice that here self.colour is a tuple, but after converting into json, it will be an array
            self.colour = tuple(self.data[f"macro {num}"]["colour"])
            self.macroName = self.data[f"macro {num}"]["macro name"]
            self.macro = self.data[f"macro {num}"]["macro"]
            if self.macroNameEntry.get() == "":
                self.macroNameEntry.insert(0, self.macroName)
            self.colourHex = f"#{self.colour[0]:02X}{self.colour[1]:02X}{self.colour[2]:02X}"
            self.RGBChooseBtn.configure(bg=self.colourHex)
            self.macroNameLabel.config(text="Macro Name: " + self.macroName)
            self.RGBColourLabel.config(text="Colour: " + f"{self.colour}")
            self.updateAction()

        # Create macro button
        createMacroBtn = tk.Button(userFrame, text="Create Macro",
                                   command=partial(self.macroCreate, num),
                                   font=button_font,
                                   bg=bg_colour,
                                   fg=button_fg_color,)
        createMacroBtn.pack(side=tk.BOTTOM)

    # Check if the length of macro name more than 30 chars
    def NameLenCheck(self,macro_name):
        if len(macro_name) <= 30:
            return True
        else:
            return False

    def delayLenCheck(self,delay):
        if len(delay) <= 4:
            return True
        else:
            return False

    # make a thread to avoid interrupting by the keyboard module
    def keyRecordTread(self,num):
        self.is_recording = True
        self.macro = []
        self.recording_thread = threading.Thread(target=lambda n=num: self.keyRecord(n))
        self.recording_thread.start()
        self.createKeyboard(num)

    ''' the main loop of key recording:
        keyboard.read_event() is to get the action and when this function works, the program will wait for it to run.
        Then use self.act to obtain the action.
        Use macroPressLimit function to check if the action is legal.
        Also, when pressing stop record or after record 20 keys (macroNumLimit function), self.is_recording will be
        False. Then keyRecord will be over. 
        If the action is legal, the action should be displayed on the text box and then appended into an array where
        store the macro.
        Lastly, checkReleasing function just release all keys that haven't been released.
        (By the way, in stopRecording function, keyboard press function from another module pyautogui is used
        to create an action (this action will not be recorded) for keyboard.read_event() to end this loop. This is
        because keyboard.read_event() cannot be skipped (though stop button is pressed, stop button cannot stop
        the current loop).)
    '''

    def keyRecord(self,num):
        while self.is_recording:
            # when recording, macro name can't be written
            self.macroNameEntry.config(state="disabled")
            event = keyboard.read_event()
            self.act = f"{event.name} {event.event_type}"
            self.macroPressLimit()
            if self.is_recording and not self.repeat and self.isNotReleased < 7 and self.isPressed:
                print(self.isNotReleased)
                self.macro.append(self.act)
                self.updateAction()
            self.macroNumLimit()
        self.macroNameEntry.config(state="normal")
        self.checkReleasing()
        self.macroCreate(num)

    def checkReleasing(self):
        """for i in range(0, len(self.macro)):
            downPosition = self.macro[i].rfind("down")
            if downPosition != -1:
                eventName = self.macro[i][0: downPosition - 1]
                isReleased = False
                for j in range(i, len(self.macro)):
                    if eventName in self.macro[j] and self.macro[j].endswith("up"):
                        isReleased = True
                if not isReleased:
                    self.macro.append(f"{eventName} up")
                    self.updateAction() """
        release_all_position = len(self.macro) - 1
        while release_all_position >= 0:
            if self.macro[release_all_position] == "release all":
                release_all_position += 1
                break
            release_all_position -= 1
        # if release_all_position < len(self.macro):
        for i in range(release_all_position,len(self.macro)):
            downPosition = self.macro[i].rfind("down")
            if downPosition != -1:
                eventName = self.macro[i][0: downPosition - 1]
                isReleased = False
                for j in range(i, len(self.macro)):
                    if eventName in self.macro[j] and self.macro[j].endswith("up"):
                        isReleased = True
                if not isReleased:
                    self.macro.append(f"release all")
                    self.updateAction()
                    break

    # check if the number of macro actions is out of limitation
    def macroNumLimit(self):
        if len(self.macro) >= 20:
            self.is_recording = False

    # check if the number of key pressed in the same time is out of limitation
    def macroPressLimit(self):
        # check if there is a repeat action
        self.repeat = False
        self.isPressed = False
        for i in range(0, len(self.macro)):
            if self.macro[i].endswith("down"):
                downPosition = self.macro[i].rfind("down")
                eventName = self.macro[i][0: downPosition - 1]
                isReleased = False
                for j in range(i, len(self.macro)):
                    if eventName in self.macro[j] and self.macro[j].endswith("up") or self.macro[j] == "release all":
                        isReleased = True
                    elif f"{eventName} up" == self.act:
                        self.isPressed = True
                if not isReleased and self.macro[i] == self.act:
                    self.repeat = True
            if self.macro[i].endswith("up"):
                upPosition = self.macro[i].rfind("up")
                eventName = self.macro[i][0:upPosition - 1]
                isHolding = False
                for j in range(i, len(self.macro)):
                    if eventName in self.macro[j] and self.macro[j].endswith("down"):
                        isHolding = True
                if not isHolding and self.macro[i] == self.act:
                    self.repeat = True
        if self.act.endswith("down"):
            self.isPressed = True
        if self.act == "release all":
            self.isPressed = True  # This is an special condition
        # check how many keys are pressed in the same time
        numPressed = 0
        numReleased = 0
        releasePosition = 0
        releasePositionCheck = len(self.macro) - 1
        while releasePositionCheck >= 0:
            if self.macro[releasePositionCheck] == "release all":
                releasePosition = releasePositionCheck + 1
                break
            releasePositionCheck = releasePositionCheck - 1
        print(f"release: {releasePosition}")
        for i in range(releasePosition, len(self.macro)):
            if self.macro[i].endswith("down"):
                numPressed += 1
        for i in range(releasePosition, len(self.macro)):
            if self.macro[i].endswith("up"):
                numReleased += 1
        if self.act.endswith("up"):
            numReleased += 1
        if self.act.endswith("down"):
            numPressed += 1
        self.isNotReleased = numPressed - numReleased

    def updateAction(self):
        self.text_area.config(state="normal")
        self.text_area.delete(1.0, tk.END)
        actions = ""
        if self.macro != [""]:
            for i in range(1, len(self.macro) + 1):
                if i <= 21:
                    print(f"macro: {self.macro[i-1]}")
                    action = "\taction " + str(i) + ": " + self.macro[i - 1]
                    print(action)
                    actions += action + "\n"
                else:
                    action = "\t           " + self.macro[i - 1]
                    print(action)
                    actions += action + "\n"
        self.text_area.insert(tk.END, actions)
        self.text_area.yview_moveto(1.0)
        self.text_area.config(state="disabled")

    def macroCreate(self, num: any):
        self.macroName = self.macroNameEntry.get()
        includeUsChar = True
        for i,char in enumerate(self.macroName):
            print(ord(char))
            if ord(char) < 32 or ord(char) > 126:
                includeUsChar = False
                break
        print(includeUsChar)
        if len(self.macroName) == 0:
            self.macroNameErrorLabel.config(text="Macro name must be between 1 and 30 characters")
        elif includeUsChar == False:
            self.macroNameErrorLabel.config(text="Macro name must be characters in US keyboard")
        else:
            self.macroNameErrorLabel.config(text="")
            self.macros = self.macro
            if f"macro {num}" in self.data:
                del self.data[f"macro {num}"]
            self.data[f"macro {num}"] = {"macro name": self.macroName,
                                         "colour": list(self.colour),
                                         "macro": self.macros}
            # Though there's no file, jsonData will be saved before GUI is closed
            self.jsonData = json.dumps(self.data, indent=4)
            DataCopy = copy.deepcopy(self.data)
            print(self.data)
            self.dataInHid = MacroToHid.create_data(DataCopy)
            print(f"data: {self.data}")
            print(self.dataInHid)
            print(self.jsonData)
            self.colour = tuple(self.data[f"macro {num}"]["colour"])
            self.macroName = self.data[f"macro {num}"]["macro name"]
            self.macro = self.data[f"macro {num}"]["macro"]
            self.colourHex = f"#{self.colour[0]:02X}{self.colour[1]:02X}{self.colour[2]:02X}"
            self.RGBChooseBtn.configure(bg=self.colourHex)
            self.macroNameLabel.config(text="Macro Name: " + self.macroName)
            self.RGBColourLabel.config(text="Colour: " + f"{self.colour}")
            if self.filename != "":
                f = open(self.filename, 'w')
                f.write(f"{self.jsonData}")
                f.close()

    def stopRecording(self):
        self.is_recording = False
        pyautogui.press('esc')
        if self.virtualKeyboard:
            self.virtualKeyboard.destroy()

    def saveBrightness(self, level):
        protLevel = level
        value = int(level)

        if len(protLevel) < 2:
            # Calculate the number of zeros needed to make the stored value of length 2 for the protocol
            zeros_needed = 2 - len(protLevel)
            # Add the zeros in front of the number
            protLevel = "0" * zeros_needed + str(protLevel)

        repeatData = self.protocol[2:10]
        self.protocol = str(protLevel) + repeatData
        print(self.protocol)

        if value == 11:
            self.brightnessValueLabel.configure(text="AUTO")
        else:
            self.brightnessValueLabel.configure(text=str(value))
        try:
            f = open(self.filename, 'r')
            self.jsonData = json.load(f)
            f.close()
            self.data = self.jsonData
            if "brightness" in self.data:
                del self.data["brightness"]
            self.data["brightness"] = protLevel
            self.jsonData = json.dumps(self.data, indent=4)
            CopyD = copy.deepcopy(self.data)
            self.dataInHid = MacroToHid.create_data(CopyD)
            f = open(self.filename, 'w')
            f.write(f"{self.jsonData}")
            f.close()
        except FileNotFoundError:
            if "brightness" in self.data:
                del self.data["brightness"]
            self.data["brightness"] = protLevel
            self.jsonData = json.dumps(self.data, indent=4)
            CopyD = copy.deepcopy(self.data)
            self.dataInHid = MacroToHid.create_data(CopyD)

    # Create a function to handle button click events
    def button_click(self, row, col):
        print(f"Button clicked: Row {row}, Column {col}")

    def fileWrite(self):
        self.filename = asksaveasfilename(defaultextension=".json",
                                          filetypes=[("Text Files", "*.json"), ("All Files", "*.*")])
        f = open(self.filename, 'w')
        f.write(f"{self.jsonData}")
        print(self.filename)
        print("File written")
        f.close()

    def fileRead(self):
        self.filename = askopenfilename()
        self.initialDelayEntry.delete(0,"end")
        self.repeatRateEntry.delete(0,"end")
        if self.filename != "":
            f = open(self.filename, 'r')
            d = json.load(f)
            f.close()
        else:
            d = copy.deepcopy(self.data)
        self.initialDelayEntry.insert(0,d["initial delay"])
        self.repeatRateEntry.insert(0,d["repeat delay"])
        self.slider.set(int(d["brightness"]))
        print(self.filename)
        print("File Read")

    def ListPortsInitially(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.portCombobox['values'] = ports

    def PortsRefreshing(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.portCombobox['values'] = ports

    def PortsConnecting(self):
        self.selectedPort = self.portCombobox.get()
        self.serialSet = serial.Serial(self.selectedPort, 57600, timeout=1)

    def readBtnPress(self):
        macroName = self.macroEntry.get() + '\n'  # Get the entered macro name
        self.serialSet.write(macroName.encode())
        self.brightnessLabel.config(text=f"Brightness: {self.slider.get()}")
        brightnessLevel = self.brightnessLabel.cget("text")
        print("Read pressed for macro:", macroName, "Brightness level:", brightnessLevel)
        print(self.serialSet.in_waiting)

    def writeBtnPress(self):

        print(self.filename)

        # Using readlines()
        file = open(self.filename, 'r')
        data = file.read()
        data += "\r"
        print("BEFORE SENDING: " + data)

        self.protocol += "\n\r"

        # str = "Hello"
        self.serialSet.write(self.protocol.encode())
        # print("Read pressed for macro:", macroName, "Brightness level:", brightnessLevel)
        print(self.serialSet.in_waiting)

        try:
            data_bytes = self.serialSet.readline()  # Read data as bytes
            print("DATA BYTES ARE:")
            print(data_bytes)
            if data_bytes:
                new_text = data_bytes.decode('utf-8', errors='replace')  # Decode as UTF-8
                print("DATA RECEIVED: " + new_text)
            else:
                print("No data received from the serial port.")
        except UnicodeDecodeError as e:
            print("Error decoding serial data:", e)

        """try:
            data_bytes = self.serialSet.readline().strip()  # Read data as bytes
            if data_bytes:
                new_text = data_bytes.decode('utf-8', errors='replace')  # Decode as UTF-8
                self.capMacro.config(text=new_text)  # Change the text of the label
            else:
                print("No data received from the serial port.")
        except UnicodeDecodeError as e:
            print("Error decoding serial data:", e)"""

    def backBtnPress(self):

        self.clear_buttons()

        self.create_btns_frame()
        self.create_new_macro_frame()

    def backBtnCreate(self):
        button_font = ("Berlin Sans FB Demi", 15)
        self.backBtn = tk.Button(self.parent, text="Back", width=self.BUTTON_WIDTH,
                                 font=button_font,
                                 command=self.backBtnPress)
        self.backBtn.pack(side=tk.BOTTOM, anchor=tk.W)

    def existingMacroPress(self):
        self.clear_buttons()
        self.backBtnCreate()

        mainFrame = tk.Frame(self.parent)

        macroBtnFrame = tk.Frame(mainFrame)
        self.macroBtns = {}  # each button will be stored in here. LATER CHANGE TO DICT AND STORE INSTRUCTIONS
        for i in range(1, 11):
            macro = self.newMacroBtn(macroBtnFrame, str(i))
            self.macroBtns[i] = macro
        macroBtnFrame.pack(side=tk.LEFT, anchor=tk.CENTER)

        for i in self.macroBtns.keys():
            print(str(i) + " => " + self.macroBtns[i])

        RGBFrame = tk.Frame(mainFrame)
        self.RGBBtns = {}
        numbers = [i for i in range(1, 11)]
        for x in numbers:
            self.RGBBtns[x] = tk.Button(RGBFrame, width=self.BUTTON_WIDTH,
                                        bg="white",
                                        command=lambda y=x: self.chooseColour(y),
                                        pady=9)
            self.RGBBtns[x].pack()
        RGBFrame.pack(side=tk.LEFT, anchor=tk.CENTER)
        print("end of loop")
        for i in self.RGBBtns.keys():
            print(str(i) + " => " + str(self.RGBBtns[i]))
        mainFrame.pack()

    def ChooseColour(self, num):
        self.colorCode = colorchooser.askcolor(title="Choose color")
        print(self.colorCode[0])
        if self.colorCode[1] is not None:
            self.RGBChooseBtn.configure(bg=f"{self.colorCode[1]}")
        print(num)
        self.colour = self.colorCode[0]
        self.macroCreate(num)

    def chooseColour(self, number):
        color_code = colorchooser.askcolor(title="Choose color")
        print(color_code[0])
        self.RGBBtns[number].configure(bg=color_code[1])
        print(number)

    def newMacroBtn(self, frame, number):
        button_font = ("Berlin Sans FB Demi", 15)
        self.macroBtn = tk.Button(frame, text="Macro " + number, width=self.BUTTON_WIDTH,
                                  command=self.macroInstructions,
                                  font=button_font)
        self.macroBtn.pack()
        return self.macroBtn.config('text')[-1]

    def macroInstructions(self):
        self.clear_buttons()
        self.backBtnCreate()

        actions = ""
        macroInstructionsFrame = tk.Frame(self.parent)
        macroInstructionsFrame.pack()
        for i in range(1, 21):
            action = "action " + str(i)
            macroInstructionsLabel = tk.Label(macroInstructionsFrame, text=action)
            macroInstructionsLabel.pack()
            actions += action + " -> "
        lastAction = "action 21"
        macroInstructionsLabel = tk.Label(macroInstructionsFrame, text=lastAction)
        macroInstructionsLabel.pack()
        actions += lastAction

        macroInstructionsFrame = tk.Frame(self.parent)
        macroInstructionsFrame.pack()

    def clear_buttons(self):
        for widgets in self.parent.winfo_children():
            widgets.destroy()

    def createKeyboard(self,num):
        self.keyBtn = []  # initialize keyBtn
        self.keyState = []
        self.virtualKeyboard = tk.Toplevel(self.parent)
        self.virtualKeyboard.title("Virtual Keyboard")
        self.virtualKeyboard.geometry("1338x405")
        self.virtualKeyboard.geometry("+500+500")
        self.virtualKeyboard.resizable(False, False)  # not allow users to adjust the window size
        for row in range(len(KeyboardLayout.text)):
            self.keyBtn.append([])  # initialize keyBtn[row]
            self.keyState.append([])
            for col in range(len(KeyboardLayout.text[row])):
                self.keyState[row].append(False)
                self.keyBtn[row].append(tk.Button(self.virtualKeyboard,
                                                  width=KeyboardLayout.width[row][col],
                                                  height=KeyboardLayout.height[row][col],
                                                  text=KeyboardLayout.text[row][col],
                                                  command=lambda r=row, c=col, n=num: self.KeyboardAction(r, c, n),
                                                  bg="#FFFFFF")
                                        )
                self.keyBtn[row][col].place(x=KeyboardLayout.x[row][col], y=KeyboardLayout.y[row][col])

    def KeyboardAction(self, row, col, num):
        self.keyState[row][col] = not self.keyState[row][col]
        if row == 5 and col == 12:
            self.keyboardAct = "release all"
            for r in range(len(KeyboardLayout.text)):
                for c in range(len(KeyboardLayout.text[row])):
                    self.keyBtn[r][c].configure(bg="#FFFFFF")
                    self.keyState[r][c] = False
        elif self.keyState[row][col]:
            self.keyboardAct = f"{KeyboardLayout.event[row][col]} down"
            self.keyBtn[row][col].configure(bg="#808080")  # set to gray stands for "hold pressing"
        else :
            self.keyboardAct = f"{KeyboardLayout.event[row][col]} up"
            self.keyBtn[row][col].configure(bg="#FFFFFF")  # set to white stands for "no pressing currently"
        self.keyboardRecord(num)

    # almost same as keyRecord function.
    def keyboardRecord(self,num):
        if self.is_recording:
            self.act = self.keyboardAct
            self.macroPressLimit()
            if self.is_recording and not self.repeat and self.isNotReleased < 7 and self.isPressed:
                print(self.isNotReleased)
                self.macro.append(self.act)
                self.updateAction()
            self.macroNumLimit()
        if not self.is_recording:
            self.checkReleasing()
            self.macroCreate(num)
    # YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY!
    # Bugs to fix tmr: 1 sometimes the max press key number larger than 6 when using both real and virtual keyboard
    # 2 shouldn't allow to record two up action repeatedly
    # 3 try to return 0 after close during record
    # 4 scrolling the tex area
    # 5 make a default data like if i haven't enter repeat delay, it should be the default value
    # 6 synchronize the label after pressing create
    # 7 make a new line when the macro name is too long
    # 8 after stopping record, just close keyboard
    # 9 set the maximum number of repeat delay and initial delay
    # 10 avoid record button for twice without stop button 防止重复按记录按钮
    # 11 the last action cannot come out until I press the stop button
    # 12 if users change the file content to illegal one, the file should not be read

class GameApp(object):

    def __init__(self, master):
        BUTTON_WIDTH = 15
        button_font = ("Berlin Sans FB Demi", 15)
        button_fg_color = "white"
        bg_colour = "light blue"

        master.title("2800 Team Project")

        controls = Controls(master)
        controls.pack(side=tk.LEFT, fill=tk.Y)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1350x700")
    # root.configure(bg="white")
    app = GameApp(root)
    root.mainloop()